local M = {}
local Popup = require("nui.popup")
local Layout = require('nui.layout')
local cmp = require('cmp')
local icons = require('nvim-web-devicons')
local ListUpdater = require("pieces.list_updater")
local relevance = require("pieces.copilot.relevance_table")
local uv = vim.loop

local function get_closest_buff_path()
    local buff_path = "/"
    local buffers = vim.api.nvim_list_bufs()
    for _, buffer in ipairs(buffers) do
        if vim.api.nvim_buf_is_loaded(buffer) then
            if vim.api.nvim_buf_get_name(buffer) ~= "" then
                buff_path = vim.api.nvim_buf_get_name(buffer)
            end
        end
    end
    return buff_path
end
local function get_paths(path)
    local items = {}
    local dir = path:match("(.*/)")
    if not dir then
        dir = "./"
    end

    local handle = uv.fs_scandir(dir)
    if handle then
        while true do
            local name, type = uv.fs_scandir_next(handle)
            if not name then break end
            local full_path = dir .. name
            if type == "directory" then
                table.insert(items, { label = full_path .. "/", kind = cmp.lsp.CompletionItemKind.Folder })
            else
                local extension = full_path:match("^.+%.(.+)$")
                for _,v in ipairs(relevance) do
                    if extension == v then
                        table.insert(items, { label = full_path, kind = cmp.lsp.CompletionItemKind.File })
                        goto continue
                    end
                end
                ::continue::
            end
        end
    end

    return items
end



local function setup_source()
    local source = {}
    source.new = function()
        return setmetatable({}, { __index = source })
    end

    source.complete = function(self, request, callback)
        local line = request.context.cursor_before_line
        local path = line:match("^(/%S*)")

        if path then
            local items = get_paths(path)
            callback({ items = items, isIncomplete = true })
        else
            -- Provide an empty result if no input
            callback({ items = {}, isIncomplete = true })
        end
    end

    cmp.register_source('pieces_file_path', source)
end

setup_source()

M.setup_buffer = function(bufnr)
    cmp.setup.buffer({
        sources = {
            { name = 'pieces_file_path' }
        },
    }, bufnr)
    vim.api.nvim_buf_set_option(bufnr, 'omnifunc', 'v:lua.vim.lsp.omnifunc')
end

local function build_result_layout(input,items,type)
    local results_popup = Popup({
        relative = "editor",
        position = "50%",
        size = {
            width = "60%",
            height = #items + 1,
        },
        border = {
            style = "rounded",
            text = {
                top = " " .. type .. " ",
                top_align = "left",
            },
        },
        win_options = {
            winhighlight = "Normal:Normal,FloatBorder:FloatBorder",
        },
    })
    local updater = ListUpdater:new(results_popup,
    1, items,
    function (item)
        if type == "Files" then
            local icon = icons.get_icon(item)
            icon = icon or ""
            return icon .. "  " .. item
        else
            return  '📁 ' .. item
        end
    end,
    function (item)
        return ""
    end,
    function (item) end)
    local layout = Layout({
            relative = "editor",
            position = "50%",
            size = {
                width = "60%",
                height = #items + 4,
            },
        },
        Layout.Box({
            Layout.Box({
                Layout.Box(results_popup, { size = "90%" }),
                Layout.Box(input, { size = "10%" }),
            }, { dir = "col", size = "100%" }),}
        ))
    layout:mount()
    updater:setup()
end

function M.setup(item)
    local context = require("pieces.copilot.context").context
    local popup_options = {
        relative = "editor",
        position = "50%",
        size = {
            height=1,
            width=60
        },
        border = {
            style = "rounded",
            text = {
                top = " Choose a " .. item .. " ",
                top_align = "left",
            },
        },
        win_options = {
            winhighlight = "Normal:Normal",
        },
    }
    local input = Popup(popup_options)
    vim.api.nvim_buf_set_lines(input.bufnr, -1, -1, false, { get_closest_buff_path() })
    print(vim.inspect(context))
    if item == "Folders" and next(context["folders"]) ~= nil then
        build_result_layout(input,context["folders"],"Folders")
    elseif item == "Files" and next(context["files"]) ~= nil then
        build_result_layout(input,context["files"],"Files")
    else
        input:mount()
    end
    vim.api.nvim_set_current_win(input.winid)

    vim.keymap.set({ "n","i" }, "<Enter>", function()
        vim.fn.PiecesAddContext(vim.api.nvim_buf_get_lines(input.bufnr, 0, 1, false)[1],nil)
        input:unmount()
    end, { buffer = input.bufnr })
    M.setup_buffer(input.bufnr)
end


return M

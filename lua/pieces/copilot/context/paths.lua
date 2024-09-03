local M = {}
local Popup = require("nui.popup")
local uv = vim.loop
local Layout = require('nui.layout')
local cmp = require('cmp')
local ListUpdater = require("pieces.list_updater")
local icons = require('nvim-web-devicons')

M.context = {
    files={},
    folders={},
    snippets={}
}
local function get_closest_buff_path()
    local buff_path = ""
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
                table.insert(items, { label = full_path, kind = cmp.lsp.CompletionItemKind.File })
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

local function build_result_layout(input,items)
    local results_popup = Popup({
        relative = "editor",
        position = "50%",
        size = {
            width = "60%",
            height = "50%",
        },
        border = {
            style = "rounded",
            text = {
                top = " Conversations ",
                top_align = "center",
            },
        },
        win_options = {
            winhighlight = "Normal:Normal,FloatBorder:FloatBorder",
        },
    })
    local updater = ListUpdater:new(results_popup,
    1, items,
    function (item)
        local icon = icons.get_icon(item)
        icon = icon or ""
        return icon .. "  " .. item
    end,
    function (item)
    end,
    function (item) end)
    local layout = Layout({
            relative = "editor",
            position = "50%",
            size = {
                width = "90%",
                height = "80%",
            },
        },
        Layout.Box({
            Layout.Box({
                Layout.Box(results_popup, { size = "90%" }),
                Layout.Box(input, { size = "10%" }),
            }, { dir = "col", size = "60%" }),}
        ))
    layout.mount()
    updater:setup()
end

function M.setup(item)
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
    if item == "Folder" and M.context["folders"] ~= {} then
        build_result_layout(input,M.context["folders"])
    elseif item == "File" and M.context["files"] ~= {} then
        build_result_layout(input,M.context["files"])
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

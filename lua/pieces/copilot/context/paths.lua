local M = {}
local Popup = require("nui.popup")
local uv = vim.loop
local cmp = require('cmp')
local relevance_table = require("pieces.copilot.relevance_table")

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

local function get_items(path, item_type)
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
            if (item_type == "file" and type == "file") or
               (item_type == "directory" and type == "directory") then
                local item = {
                    label = full_path
                }
                if item_type == "directory" then
                    item.label = full_path .. "/"
                    item.kind = cmp.lsp.CompletionItemKind.Folder
                else
                    local ext = name:match("^.+(%..+)$")
                    if ext and not relevance_table[ext] then
                        goto continue  -- Skip files with invalid extensions
                    end
                    item.kind = cmp.lsp.CompletionItemKind.File
                end
                table.insert(items, item)
            end
            ::continue::
        end
    end

    return items
end

local function setup_source(name, item_type)
    local source = {}
    source.new = function()
        return setmetatable({}, { __index = source })
    end

    source.complete = function(self, request, callback)
        local line = request.context.cursor_before_line
        local path = line:match("^(/%S*)")

        if path then
            local items = get_items(path, item_type)
            callback({ items = items, isIncomplete = true })
        else
            -- Provide an empty result if no input
            callback({ items = {}, isIncomplete = true })
        end
    end

    cmp.register_source(name, source)
end

-- Register sources for files and folders
setup_source('pieces_file', 'file')
setup_source('pieces_folder', 'directory')


M.setup_buffer = function(bufnr,name)
    cmp.setup.buffer({
        sources = {
            { name = name }
        },
    }, bufnr)
    vim.api.nvim_buf_set_option(bufnr, 'omnifunc', 'v:lua.vim.lsp.omnifunc')
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
    input:mount()
    vim.api.nvim_set_current_win(input.winid)
    vim.keymap.set({ "n","i" }, "<Enter>", function()
        vim.fn.PiecesAddContext(vim.api.nvim_buf_get_lines(input.bufnr, 0, 1, false),nil)
        input:unmount()
    end, { buffer = input.bufnr })
    local name
    if item == "Folder" then
        name = "pieces_folder"
    else
        name = "pieces_file"
    end
    M.setup_buffer(input.bufnr,name)
end

return M

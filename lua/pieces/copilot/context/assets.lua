local Popup = require('nui.popup')
local snippets = require('pieces.assets.assets')
local icons = require('nvim-web-devicons')
local make_buffer_read_only = require("pieces.utils").make_buffer_read_only
local ListUpdater = require("pieces.list_updater")
local results_popup
local M = {}
local updater
updater = ListUpdater:new(results_popup,1,snippets.snippets,
    function(snippet)
        local icon = icons.get_icon("dummy", snippet.language)
        icon = icon or ""
        return icon .. "  " .. snippet.name
    end,
    function(snippet)
        return snippet.annotation:gsub("\n", " ")
    end,
    function (item)
        updater:toggle_selection()
        vim.fn.PiecesAddContext(nil,item.id)
    end,
    function (item) end,
    function (updater) end,true)

function M.setup()
    -- Create the results popup
    results_popup = Popup({
        relative = "editor",
        position = "50%",
        size = {
            width = "80%",
            height = "40%",
        },
        border = {
            style = "rounded",
            text = {
                top = " Add a Snippet ",
                top_align = "center",
            },
        },
        win_options = {
            winhighlight = "Normal:Normal,FloatBorder:FloatBorder",
        },
    })
    make_buffer_read_only(results_popup.bufnr)
    updater.results_popup = results_popup -- Update the new result popup
    updater:mount()
end

return M

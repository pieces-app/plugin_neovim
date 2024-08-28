local Popup = require('nui.popup')
local Layout = require('nui.layout')
local event = require('nui.utils.autocmd').event
local snippets = require('pieces.assets.assets')
local icons = require('nvim-web-devicons')
local edit_asset = require('pieces.assets.edit').edit_asset
local delete_asset = require('pieces.assets.edit').delete_asset
local make_buffer_read_only = require("pieces.utils").make_buffer_read_only
local ListUpdater = require("pieces.list_updater")
local results_popup,preview_popup,input_popup,layout
local M = {}
local snippets_search_results = snippets.snippets

local updater = ListUpdater:new(results_popup,1,snippets_search_results,
	function(snippet)
        local icon = icons.get_icon("dummy", snippet.language)
        icon = icon or ""
        return icon .. "  " .. snippet.name
    end,
    function(snippet)
        return snippet.annotation:gsub("\n", " ")
	end,
	function (item)
		layout:unmount()
		edit_asset(item)
	end,
	function (item)
		delete_asset(item)
	end,
	function (updater)
		if results_popup and preview_popup and
		type(results_popup.bufnr) == "number" and
		type(preview_popup.bufnr) == "number" and
		vim.api.nvim_buf_is_valid(preview_popup.bufnr) then
			local snippet = updater.items[updater.current_index]
			-- Split snippet.raw into lines
			local lines = {}
			for line in snippet.raw:gmatch("[^\r\n]+") do
				table.insert(lines, line)
			end

			vim.api.nvim_buf_set_lines(preview_popup.bufnr, 0, -1, false, lines)
			-- Set the syntax highlighting for the buffer
			vim.api.nvim_buf_set_option(preview_popup.bufnr, 'filetype', snippet.filetype)
			preview_popup.border:set_text("top", snippet.name, "center")
		end
	end)

-- Handle search and preview logic
local function on_input(input)
	snippets_search_results = snippets.search(input)
	-- Update the results popup with search results
	-- You can use a Nui Text component to display the results
	local lines = {}
	for _, result in ipairs(snippets_search_results) do
		local icon = icons.get_icon("dummy", result.language)
		icon = icon or ""
		table.insert(lines, icon .. " " .. result.name)
	end
	vim.api.nvim_buf_set_lines(results_popup.bufnr, 0, -1, false, lines)

	updater.current_index = 1
	-- Highlight common characters
	for i, result in ipairs(snippets_search_results) do
		local start_idx, end_idx = result.name:lower():find(input:lower())
		if start_idx and end_idx then
			vim.api.nvim_buf_add_highlight(results_popup.bufnr, -1, 'Search', i - 1, start_idx - 1,
				end_idx)
		end
	end
end

function M.setup()
	-- Create the search input popup
	input_popup = Popup({
		position = "50%",
		size = {
			width = "80%",
			height = 1,
		},
		border = {
			style = "rounded",
			text = {
				top = " Search ",
				top_align = "center",
			},
		},
		win_options = {
			winhighlight = "Normal:Normal,FloatBorder:FloatBorder",
		},
	})

	-- Create the results popup
	results_popup = Popup({
		position = "50%",
		size = {
			width = "80%",
			height = "40%",
		},
		border = {
			style = "rounded",
			text = {
				top = " Results ",
				top_align = "center",
			},
		},
		win_options = {
			winhighlight = "Normal:Normal,FloatBorder:FloatBorder",
		},
	})

	-- Create the preview popup
	preview_popup = Popup({
		position = "50%",
		size = {
			width = "80%",
			height = "40%",
		},
		border = {
			style = "rounded",
			text = {
				top = " Preview ",
				top_align = "center",
			},
		},
		win_options = {
			winhighlight = "Normal:Normal,FloatBorder:FloatBorder",
		},
	})

	make_buffer_read_only(results_popup.bufnr)
	make_buffer_read_only(preview_popup.bufnr)
	layout = Layout({
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
				Layout.Box(input_popup, { size = "10%" }),
			}, { dir = "col", size = "60%" }),
			Layout.Box(preview_popup, { size = "40%" }),
		}, { dir = "row" }
		))

	-- Handle input changes
	input_popup:on(event.TextChangedI, function()
		local input = vim.api.nvim_get_current_line()
		on_input(input)
		updater.items = snippets_search_results
	end)

	make_buffer_read_only(results_popup.bufnr)
	updater.results_popup = results_popup -- Update the new result popup
	layout:mount()
	vim.api.nvim_set_current_win(results_popup.winid)
	updater:setup()
end

function M.update()
	if results_popup and type(results_popup.bufnr) == "number" and preview_popup and type(preview_popup.bufnr) == "number" then
		updater:update()
	end
end

return M

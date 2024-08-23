local Popup = require('nui.popup')
local Layout = require('nui.layout')
local event = require('nui.utils.autocmd').event
local snippets = require('pieces_assets.assets')
local icons = require('nvim-web-devicons')
local edit_asset = require('pieces_assets.edit').edit_asset
local delete_asset = require('pieces_assets.edit').delete_asset
local make_buffer_read_only = require("pieces_utils").make_buffer_read_only

local M = {}
local current_index = 1
local snippets_search_results = snippets.snippets

function M.setup()
	-- Create the search input popup
	local input_popup = Popup({
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
	local results_popup = Popup({
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
	local preview_popup = Popup({
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
				Layout.Box(input_popup, { size = "10%" }),
			}, { dir = "col", size = "60%" }),
			Layout.Box(preview_popup, { size = "40%" }),
		}, { dir = "row" }
		))


	-- Function to update the list popup
	local function update_list()
	    local lines = {}
	    local end_col, start_col, annotation_index

	    for i, snippet in ipairs(snippets_search_results) do
	        local icon = icons.get_icon("dummy", snippet.language)
	        icon = icon or ""
	        local base_name = icon .. "  " .. snippet.name
	        if i == current_index then
	            -- Highlighted line (current selection)
	            local highlighted_line = "> " .. base_name .. " "
				local snippet_annotation = snippet.annotation:gsub("\n", " ")
	            start_col = #highlighted_line
	            highlighted_line = highlighted_line .. snippet_annotation
	            end_col = start_col + #snippet.annotation
	            annotation_index = i - 1 -- Convert to 0-based index for highlighting
	            table.insert(lines, highlighted_line)
	        else
	            table.insert(lines, " " .. base_name)
	        end
	    end

	    vim.api.nvim_buf_set_lines(results_popup.bufnr, 0, -1, false, lines)

	    -- Apply the highlight if annotation_index is valid
	    if annotation_index then
	        vim.api.nvim_buf_add_highlight(results_popup.bufnr, -1, "PiecesAnnotation", annotation_index, start_col, end_col)
	    end

	    local win_height = vim.api.nvim_win_get_height(results_popup.winid) - 5 -- Removing the borders
	    local cursor_line = current_index - 1 -- Convert to 0-based index for nvim_win_set_cursor
	    if cursor_line >= win_height or cursor_line - win_height < 0 then
	        vim.api.nvim_win_set_cursor(results_popup.winid, { current_index, 0 })
	    end
	end


	-- Function to update the preview popup
	local function update_preview()
		local snippet = snippets_search_results[current_index]
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

	local function down_keymap()
		if current_index < #snippets_search_results then
			current_index = current_index + 1
			update_list()
			update_preview()
		end
	end

	local function up_keymap()
		if current_index > 1 then
			current_index = current_index - 1
			update_list()
			update_preview()
		end
	end
	local function enter_keymap()
		layout:unmount()
		edit_asset(snippets_search_results[current_index])
	end
	local function delete_asset_keymap()
		delete_asset(snippets_search_results[current_index])
		update_list()
		update_preview()
	end
	-- Key mappings for navigation
	local keymaps = {
		["<Up>"] = up_keymap,
		["<Down>"] = down_keymap,
		["<esc>"] = function() layout:unmount() end,
		["<enter>"] = enter_keymap,
		["<Del>"] = delete_asset_keymap,
		["<kDel>"] = delete_asset_keymap,
		["<BS>"] = delete_asset_keymap  -- Add this line for macOS
 	}
	local modes = { "i", "n" }

	for key, func in pairs(keymaps) do
		for _, mode in ipairs(modes) do
			results_popup:map(mode, key, func, { noremap = true })
			input_popup:map(mode, key, func, { noremap = true })
		end
	end



	-- Mount the layout
	layout:mount()
	update_list()
	update_preview()

	vim.api.nvim_set_current_win(input_popup.winid)

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

		current_index = 1
		-- Highlight common characters
		for i, result in ipairs(snippets_search_results) do
			local start_idx, end_idx = result.name:lower():find(input:lower())
			if start_idx and end_idx then
				vim.api.nvim_buf_add_highlight(results_popup.bufnr, -1, 'Search', i - 1, start_idx - 1,
					end_idx)
			end
		end
	end

	-- Handle input changes
	input_popup:on(event.TextChangedI, function()
		local input = vim.api.nvim_get_current_line()
		on_input(input)
	end)
end

return M

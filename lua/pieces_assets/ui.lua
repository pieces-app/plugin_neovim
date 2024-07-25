local Popup = require('nui.popup')
local Layout = require('nui.layout')
local event = require('nui.utils.autocmd').event
local snippets = require('pieces_assets.assets')
local icons = require('nvim-web-devicons')


local M = {}
local current_index = 1
local displayed_snippets = snippets.snippets

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

	local layout = Layout({
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
		for i, snippet in ipairs(displayed_snippets) do
			local icon = icons.get_icon("dummy", snippet.language)
			local base_name = icon .. "  " .. snippet.name
			if i == current_index then
				-- Highlighted line (current selection)
				local highlighted_line = "> " .. base_name .. " "
				-- local tag_start_col = #highlighted_line + 1
				-- highlighted_line = highlighted_line .. snippet.annotation
				table.insert(lines, highlighted_line)

				-- local ns_id = vim.api.nvim_create_namespace('Pieces')
				-- vim.api.nvim_buf_add_highlight(results_popup.bufnr, ns_id, "PiecesAnnotation", i - 1, tag_start_col, -1)
			else
				table.insert(lines, " " .. base_name)
			end
		end

		vim.api.nvim_buf_set_lines(results_popup.bufnr, 0, -1, false, lines)

        local win_height = vim.api.nvim_win_get_height(results_popup.winid)
        local cursor_line = current_index - 1 -- Convert to 0-based index for nvim_win_set_cursor

        -- Calculate if cursor_line is near the bottom of the window
        if cursor_line >= win_height then
            vim.api.nvim_win_set_cursor(results_popup.winid, { current_index, 0 })
        end

        -- Calculate if the cursor_line is near the top of the window
        if cursor_line < 0 then
            vim.api.nvim_win_set_cursor(results_popup.winid, { current_index - win_height + 1, 0 })
        end

	end

	-- Function to update the preview popup
	local function update_preview()
		local snippet = displayed_snippets[current_index]
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
		if current_index < #displayed_snippets then
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

    -- Key mappings for navigation
    local keymaps = { ["<Up>"] = up_keymap, ["<Down>"] = down_keymap, ["<esc>"] = function() layout:unmount() end }
    local modes = {"i", "n"}

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
		local results = snippets.search(input)
		-- Update the results popup with search results
		-- You can use a Nui Text component to display the results
		local lines = {}
		displayed_snippets = {}
		for _, result in ipairs(results) do
			table.insert(displayed_snippets, result)
			table.insert(lines, result.name)
		end
		vim.api.nvim_buf_set_lines(results_popup.bufnr, 0, -1, false, lines)

        current_index = 1
		-- Highlight common characters
		for i, result in ipairs(results) do
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

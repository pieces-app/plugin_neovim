local NuiPopup  = require('nui.popup')
local NuiLayout = require('nui.layout')
local NuiSplit  = require('nui.split')
local make_buffer_read_only = require("pieces.utils").make_buffer_read_only

-- Function to create an input popup
local function create_input_popup(on_submit,win_id)
	local popup_options = {
		relative = {
		  type = "win",
		  winid = win_id,
		},
		position = {
			row = "100%",
			col = 0,
		},
		size = {
			width = "100%",
			height = "20%",
		},
		border = {
			style = "rounded",
			text = {
				top = " Input ",
				top_align = "center",
			},
		},
		win_options = {
			winblend = 10,
			winhighlight = "Normal:Normal,FloatBorder:FloatBorder",
		},
		buf_options = {
			bufhidden = "wipe"
		},
		enter = true,
	}

	local input = NuiPopup(popup_options)

	vim.keymap.set({ "i" }, "<Enter>", function()
		vim.api.nvim_buf_set_lines(input.bufnr, -1, -1, false, { "" })
		vim.api.nvim_win_set_cursor(0, { vim.api.nvim_buf_line_count(input.bufnr), 0 })
	end, { buffer = input.bufnr })

	vim.keymap.set({ "n" }, "<Enter>", function()
		local num_lines = vim.api.nvim_buf_line_count(input.bufnr)
		local lines = vim.api.nvim_buf_get_lines(input.bufnr, 0, num_lines, false)
		on_submit(lines)
	end, { buffer = input.bufnr })
	return input
end
local function get_split()
	local split = NuiSplit({
		relative = "editor",
		position = "right",
		size = "30%",
		win_options = {
			wrap = true,
			linebreak = true,
			foldcolumn = "1",
			winhighlight = "Normal:Normal,FloatBorder:FloatBorder",
			number = false,
			relativenumber = false
		},
		buf_options = {
			filetype = "markdown"
		}
	})
	make_buffer_read_only(split.bufnr)
	return split
end

local function get_layout(split,input_popup,chat_popup)
	local layout = NuiLayout(
		split,
		NuiLayout.Box({
			NuiLayout.Box({
				NuiLayout.Box(chat_popup, { grow = 1 }),
				NuiLayout.Box(input_popup, { size = 5 }),
			}, { dir = "col", size = "100%" }),
		})
	)
	return layout
end


return {
	create_input_popup = create_input_popup,
	get_split = get_split,
	layout = get_layout,
}

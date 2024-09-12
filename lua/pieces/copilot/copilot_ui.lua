local NuiPopup  = require('nui.popup')
local NuiLayout = require('nui.layout')
local NuiSplit  = require('nui.split')
local conversation = require("pieces.copilot.conversations")
local make_buffer_read_only = require("pieces.utils").make_buffer_read_only
local layout

local function create_chat_popup()
	local popup = NuiPopup({
		border = {
			highlight = "FloatBorder",
			style = "rounded",
			text = {
				top = " Pieces Copilot ",
			},
		},
		win_options = {
			wrap = true,
			linebreak = true,
			foldcolumn = "1",
			winhighlight = "Normal:Normal,FloatBorder:FloatBorder",
		},
		buf_options = {
			filetype = "markdown"
		}
	})

  make_buffer_read_only(popup.bufnr)
  return popup
end

-- Function to create an input popup
local function create_input_popup(on_submit)
	local prompt = "> "
	local popup_options = {
		relative = "window",
		position = {
			row = 1,
			col = 0,
		},
		size = 20,
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
	}

	local input = NuiPopup(popup_options, {
		prompt = prompt,
		on_close = function()
			layout:unmount()
			conversation.set_conversation()
		end,

	})

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

local function get_layout(chat_popup,input_popup)
	-- Create a vertical layout with chat_popup and input_popup
	layout = NuiLayout(
		NuiSplit({
			relative = "editor",
			position = "right",
			size = "30%",
		}),

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
	create_chat_popup = create_chat_popup,
	layout=get_layout
}

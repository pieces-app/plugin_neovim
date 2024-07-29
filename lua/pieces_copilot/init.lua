local NuiPopup     = require('nui.popup')
local NuiLayout    = require('nui.layout')
local NuiSplit     = require('nui.split')
local NuiLine      = require('nui.line')
local NuiInput     = require('nui.input')

local input_popup, layout, chat_popup
local current_line = -1
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
	-- Create an autogroup
	local group = vim.api.nvim_create_augroup("PreventInsertMode", { clear = true })

	-- Add autocommands to the group for the new buffer
	vim.api.nvim_create_autocmd({ "InsertEnter", "InsertCharPre" }, {
		group = group,
		buffer = popup.bufnr,
		callback = function()
			vim.cmd("stopinsert")
		end,
	})
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
			filetype = "markdown"
		},
	}

	local input = NuiInput(popup_options, {
		prompt = prompt,
		on_close = function()
			chat_popup = nil
		end

	})
	vim.keymap.set({ "n", "i" }, "<CR>", function()
		local value = string.sub(vim.api.nvim_get_current_line(), vim.fn.strwidth(prompt) + 1)
		on_submit(value)
	end, { buffer = input.bufnr })
	return input
end

local function append_to_chat(text)
	local bufnr = chat_popup.bufnr
	current_line = current_line + 2
	vim.api.nvim_buf_set_lines(bufnr, current_line, -1, false, { text })
end


local function setup()
	chat_popup = create_chat_popup()

	local function on_submit(value)
		if value:match("^%s*$") then
			return
		end
		vim.fn.PiecesCopilotSendQuestion(value)
		vim.api.nvim_buf_set_lines(input_popup.bufnr, 0, -1, false, { "" })
		append_to_chat(value)
	end


	-- Initial creation of the input popup
	input_popup = create_input_popup(on_submit)

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
	layout:mount()
	vim.o.statusline = "Pieces Copilot" -- TODO display the model name also

	vim.api.nvim_set_current_win(input_popup.winid)
	vim.fn.mode("i")
end

return {
	setup = setup,
	append_to_chat = append_to_chat
}

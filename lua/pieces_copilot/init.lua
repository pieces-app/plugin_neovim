local NuiLayout          = require('nui.layout')
local NuiSplit           = require('nui.split')
local copilot_ui         = require("pieces_copilot.ui")

local create_input_popup = copilot_ui.create_input_popup
local create_chat_popup  = copilot_ui.create_chat_popup

local input_popup, layout, chat_popup, previous_role, whole_text,completed,current_line

local function append_to_chat(character, role)
	local bufnr = chat_popup.bufnr

	-- Initialize `whole_text` if the role changes
	if role ~= previous_role then
		current_line = vim.api.nvim_buf_line_count(bufnr)
		if current_line == 1 then
		    current_line = current_line + 1
		else
		    current_line = current_line + 2
		end

		vim.api.nvim_buf_set_lines(bufnr, -1, -1, false, { "","" })
		previous_role = role
		whole_text = {role .. ": "}
	end

	if type(character) == "table" then
	    whole_text = character
	elseif string.find(character, "\n") ~= nil then
	    local lines = vim.split(character, "\n", true)
	    for i, line in ipairs(lines) do
	        if i == 1 then
	            whole_text[#whole_text] = whole_text[#whole_text] .. line
	        else
	            table.insert(whole_text, line)
	        end
	    end
	else
	    -- Append character to the last element of `whole_text`
	    whole_text[#whole_text] = whole_text[#whole_text] .. character
	end


	-- Set the lines in the buffer
	vim.api.nvim_buf_set_lines(bufnr, current_line, -1, false, whole_text)
end




local function setup()
	if chat_popup then
		return
	end

	chat_popup = create_chat_popup()

	local function on_submit(value)
		local has_non_space_string = false
		local lines = {}
		local content = ""
		for _, v in ipairs(value) do
			v = v:sub(3) -- Remove the prompt
			content = content .. "\n" .. v
			table.insert(lines, v)
			if v:match("%S") then
				has_non_space_string = true
			end
		end

		if not has_non_space_string and completed == true then
			return
		end
		vim.fn.PiecesCopilotSendQuestion(content)
		completed = false
		vim.api.nvim_buf_set_lines(input_popup.bufnr, 0, -1, false, { "" })
		append_to_chat(lines,"User")
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
	append_to_chat = append_to_chat,
	completed = function(value) completed = value end,
}

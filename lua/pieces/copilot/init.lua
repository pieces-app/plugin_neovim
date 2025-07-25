local copilot_ui         = require("pieces.copilot.copilot_ui")
local slash_commands     = require("pieces.copilot.slash_commands")
local conversations      = require("pieces.copilot.conversations")
local NuiPopup           = require('nui.popup')

local create_input_popup = copilot_ui.create_input_popup
local get_split  = copilot_ui.get_split
local get_layout = copilot_ui.layout
local input_popup, layout, chat_popup, previous_role, whole_text,completed,beginning_line,split


local function add_line()
	table.insert(whole_text, "")
end

vim.api.nvim_create_autocmd("WinClosed", {
    callback = function(args)
        local closed_window_id = tonumber(args.match)
        if split ~= nil and layout ~= nil and closed_window_id == split.winid then
        	layout:unmount()
        end
        if layout ~= nil and split ~= nil and (
        	closed_window_id == layout.winid or
        	closed_window_id == input_popup.winid or
        	closed_window_id == chat_popup.winid) then
        	-- Check if any window is closed to close the split view
        	split:unmount()
        end
    end
})

local function append_to_chat(character, role)
	local bufnr = chat_popup.bufnr

	-- Initialize `whole_text` if the role changes
	if role ~= previous_role then
		beginning_line = vim.api.nvim_buf_line_count(bufnr)
		if beginning_line == 1 then
		    vim.api.nvim_buf_set_lines(bufnr, -1, -1, false, {})
		else
		    beginning_line = beginning_line + 1
		    vim.api.nvim_buf_set_lines(bufnr, -1, -1, false, { "" })
		end

		previous_role = role
		whole_text = {role .. ": "}
		end
	if type(character) == "table" then
		whole_text = character
		table.insert(whole_text, 1, role .. ": " .. table.remove(whole_text, 1))
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
	vim.api.nvim_buf_set_lines(bufnr, beginning_line, -1, false, whole_text)


	local line_count = vim.api.nvim_buf_line_count(bufnr)
    vim.api.nvim_win_set_cursor(chat_popup.winid, {line_count, 0})
end

local function update_status_bar()
	if split ~= nil and type(split.winid) == "number" and vim.api.nvim_win_is_valid(split.winid) == true then
		local success, model_name = pcall(vim.fn.PiecesGetModel)
		if success and model_name then
			local status_success, _ = pcall(vim.api.nvim_win_set_option, split.winid, 'statusline', 'Pieces Model: ' .. model_name)
			if not status_success then
				print("Failed to set statusline option")
			end
		end
	else
		print("Failed to get model name")
	end
end

local function setup()
	if layout ~= nil then
		layout:unmount()
		split:unmount()
	end

	split = get_split()
	chat_popup = NuiPopup({buf_options = {filetype = "markdown"}})
	conversations.set_conversation()
	local function on_submit(value)
		local has_non_space_string = false
		local content = ""
		for _, v in ipairs(value) do
			if v:match("%S") then
				content = content .. "\n" .. v
				has_non_space_string = true
			end
		end
		if not has_non_space_string and completed == false then
			return
		end
		completed = false

		vim.api.nvim_buf_set_lines(input_popup.bufnr, 0, -1, false, { "" })
		local slash = slash_commands.handle_slash(value[1])
		if slash==false then
			vim.fn.PiecesCopilotSendQuestion(content)
			append_to_chat(value,"USER")
		elseif slash == nil then
			return
		else
			append_to_chat({slash,""},"SYSTEM")
		end
	end

	input_popup = create_input_popup(on_submit,chat_popup.winid)
	layout = get_layout(split,input_popup,chat_popup)
	layout:mount()

	update_status_bar()
	vim.api.nvim_create_autocmd("ModeChanged", {
	  pattern = "*",
	  callback = update_status_bar,
	})
	slash_commands.setup_buffer(vim.api.nvim_get_current_buf())
end



return {
	setup = setup,
	add_line=add_line,
	append_to_chat = append_to_chat,
	completed = function(value) completed = value end
}

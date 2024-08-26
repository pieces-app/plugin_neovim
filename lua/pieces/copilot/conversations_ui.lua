local Popup = require('nui.popup')
local conversations_module = require('pieces.copilot.conversations')
local copilot_module = require('pieces.copilot')
local M = {}
local current_index = 1
local conversations = conversations_module.conversations
local results_popup

local function update_list()
	if not vim.api.nvim_buf_is_valid(results_popup.bufnr) then
		return
	end
    local lines = {}
    local end_col, start_col, annotation_index

    for i, conversation in ipairs(conversations) do
        local base_name = conversation.name:gsub("\n", "\\n")
        if i == current_index then
            local highlighted_line = "> " .. base_name .. " "
            start_col = #highlighted_line
            highlighted_line = highlighted_line .. conversation.annotation
            end_col = start_col + #conversation.annotation
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
function M.update()
	if results_popup then
		update_list()
	end
end


function M.setup()
	-- Create the results popup
	results_popup = Popup({
		relative = "editor",
		position = "50%",
		size = {
			width = "60%",
			height = "50%",
		},
		border = {
			style = "rounded",
			text = {
				top = " Conversations ",
				top_align = "center",
			},
		},
		win_options = {
			winhighlight = "Normal:Normal,FloatBorder:FloatBorder",
		},
	})


	local function down_keymap()
		if current_index < #conversations then
			current_index = current_index + 1
			update_list()
		end
	end

	local function up_keymap()
		if current_index > 1 then
			current_index = current_index - 1
			update_list()
		end
	end
	local function enter_keymap()
		results_popup:unmount()
		copilot_module.setup() -- reset the copilot view
		for k,v in pairs(conversations[current_index].messages) do
			if v == -1 then -- message is deleted
				goto continue
			end

			local table_str = vim.fn.PiecesGetMessage(k)
			local func, err = load("return " .. table_str)
			if not func then
			    print("Error loading string:", err)
			    return
			end
			local message = func()
			copilot_module.append_to_chat(message.raw,message.role)

			::continue::
		end
		vim.fn.PiecesSetConversation(conversations[current_index].id)
	end
	local function delete_keymap()
		conversations_module.delete(conversations[current_index].id)
	end
	-- Key mappings for navigation
	local keymaps = {
		["<Up>"] = up_keymap,
		["<Down>"] = down_keymap,
		["<esc>"] = function() results_popup:unmount() end,
		["<enter>"] = enter_keymap,
		["<Del>"] = delete_keymap,
		["<kDel>"] = delete_keymap,
		["<BS>"] = delete_keymap
	}
	local modes = { "i", "n" }

	for key, func in pairs(keymaps) do
		for _, mode in ipairs(modes) do
			results_popup:map(mode, key, func, { noremap = true })
		end
	end



	-- Mount the layout
	results_popup:mount()
	update_list()

	vim.api.nvim_set_current_win(results_popup.winid)

end

return M

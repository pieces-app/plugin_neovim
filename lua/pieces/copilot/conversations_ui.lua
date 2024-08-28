local Popup = require('nui.popup')
local conversations_module = require('pieces.copilot.conversations')
local copilot_module = require('pieces.copilot')
local ListUpdater = require("pieces.list_updater")
local make_buffer_read_only = require("pieces.utils").make_buffer_read_only
local M = {}
local conversations = conversations_module.conversations
local results_popup

local updater = ListUpdater:new(results_popup,1,conversations,
	function(conversation)
        return conversation.name:gsub("\n", "\\n")
    end,
    function(conversation)
        return conversation.annotation
	end,
	function (item)
	    results_popup:unmount()
	    copilot_module.setup() -- reset the copilot view
	    for k, v in pairs(item.messages) do
	        if v == -1 then -- message is deleted
	            goto continue
	        end

	        local table_str = vim.fn.PiecesGetMessage(k)
	        if table_str == nil then
	            vim.notify("Not a valid conversation", vim.log.levels.ERROR)
	            break
	        end
	        local func, err = load("return " .. table_str)
	        if not func then
	            print("Error loading string:", err)
	            return
	        end
	        local message = func()
	        copilot_module.append_to_chat(message.raw, message.role)

	        ::continue::
	    end
	    vim.fn.PiecesSetConversation(item.id)
	end,
	function (item)
	    local choice = vim.fn.confirm("Are you sure you want to delete '" .. item.name .."'", "&Yes\n&No", 1)
	    if choice == 1 then
	        conversations_module.delete(item.id)
	    end
	end)

function M.update()
	if results_popup and type(results_popup.bufnr) == "number" then
		updater:update()
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
	make_buffer_read_only(results_popup.bufnr)
	updater.results_popup = results_popup -- Update the new result popup
	updater:mount()
end

return M

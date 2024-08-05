local M = {}


M.conversations = {}

function M.append_conversations(conversation, first)
	for i, v in ipairs(M.conversations) do
		if v.id == conversation.id then
			M.conversations[i] = conversation
			return
		end
	end
	if first then
		table.insert(M.conversations, 1, conversation)
	else
		table.insert(M.conversations, conversation)
	end
end

function M.delete(conversation_id)
	vim.fn.PiecesDeleteConversation(conversation_id)
end

return M


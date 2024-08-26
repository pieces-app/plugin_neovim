local M = {}

M.conversations = {}

function M.append_conversations(conversation, sort)
    local updated = false

    -- Check if the conversation already exists and update it
    for i, v in ipairs(M.conversations) do
        if v.id == conversation.id then
            M.conversations[i] = conversation
            updated = true
            break
        end
    end

    -- If the conversation was not updated, insert it
    if not updated then
        table.insert(M.conversations, 1, conversation)
    end

    -- Sort the conversations if required
    if sort then
        table.sort(M.conversations, function(a, b)
            return a.update > b.update
        end)
    end
end



function M.delete(conversation_id)
	vim.fn.PiecesDeleteConversation(conversation_id)
end

function M.remove_conversation(conversation_id)
    for i, v in ipairs(M.conversations) do
        if v.id == conversation_id then
            table.remove(M.conversations, i)
            return
        end
    end
end

return M

local M = {}

M.conversations = {}

function M.append_conversations(conversation, sort)
    -- Check if the conversation already exists and update it
    for i, v in ipairs(M.conversations) do
        if v.id == conversation.id then
            M.conversations[i] = conversation
            if sort then
                table.sort(M.conversations, function(a, b)
                    return a.updated > b.updated
                end)
            end
            return
        end
    end

    table.insert(M.conversations, conversation)
    if sort then
        table.sort(M.conversations, function(a, b)
            return a.updated > b.updated
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


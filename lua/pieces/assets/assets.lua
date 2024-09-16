local M = {}

M.snippets = {}

function M.search(query)
	local results = {}
	for _, snippet in ipairs(M.snippets) do
		if snippet.name:lower():find(query:lower()) then
			table.insert(results, snippet)
		end
	end
	return results
end

function M.append_snippets(snippet, first)
	for i, v in ipairs(M.snippets) do
		if v.id == snippet.id then
			M.snippets[i] = snippet
			return
		end
	end
	if first then
		table.insert(M.snippets, 1, snippet)
	else
		table.insert(M.snippets, snippet)
	end
end


function M.get_by_name(name)
	for _, snippet in ipairs(M.snippets) do
		if snippet.name == name then
			return snippet
		end
	end
	return nil
end

function M.remove_snippet(snippet_id)
	for i, v in ipairs(M.snippets) do
		if v.id == snippet_id then
			table.remove(M.snippets, i)
			return
		end
	end
end

return M


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

function M.append_snippets(snippet)
	for i, v in ipairs(M.snippets) do
		if v.id == snippet.id then
			M.snippets[i] = snippet
			return
		end
	end
	table.insert(M.snippets, snippet)
end

function M.get_by_name(name)
	for _, snippet in ipairs(M.snippets) do
		if snippet.name == name then
			return snippet
		end
	end
	return nil
end

return M

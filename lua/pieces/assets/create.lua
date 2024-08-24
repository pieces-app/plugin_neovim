local M = {}
function M.setup(l1,l2)
    local start_pos = vim.fn.getpos("'<")
    local end_pos = vim.fn.getpos("'>")
    local lines = vim.fn.getline(start_pos[2], end_pos[2])

    if #lines == 0 then
        return ""
    end

    lines[#lines] = string.sub(lines[#lines], 1, end_pos[3])
    lines[1] = string.sub(lines[1], start_pos[3])
    vim.fn.PiecesCreateSnippet(table.concat(lines, "\n"))
end

return M
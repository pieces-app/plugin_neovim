M = {}
function M.edit_asset(snippet)
    local buf = vim.api.nvim_create_buf(false, false)
  
    vim.api.nvim_buf_set_option(buf, 'filetype', snippet.filetype)
    vim.api.nvim_buf_set_lines(buf, 0, -1, false, vim.split(snippet.raw, '\n'))
    vim.api.nvim_buf_set_name(buf,snippet.name)
    vim.api.nvim_set_current_buf(buf)

    vim.api.nvim_create_autocmd("BufWritePre", {
    buffer = buf,
    callback = function()
        vim.api.nvim_buf_set_option(buf, 'readonly', true)
        local num_lines = vim.api.nvim_buf_line_count(buf)
        local lines = vim.api.nvim_buf_get_lines(buf, 0, num_lines, false)
        local content = table.concat(lines, "\n")
        vim.fn.PiecesEditAsset(snippet.id,content)
        vim.api.nvim_buf_delete(buf, { force = true })
    end,
    })
end
function M.delete_asset(snippet)
    local choice = vim.fn.confirm("Are you sure you want to delete '" .. snippet.name.."'", "&Yes\n&No", 1)
    if choice == 1 then
        vim.fn.PiecesDeleteAsset(snippet.id)
    end
end
return M
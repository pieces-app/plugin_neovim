local function make_buffer_read_only( bufnr )
  -- Create an autogroup
  local group = vim.api.nvim_create_augroup("PreventInsertMode", { clear = true })

  -- Add autocommands to the group for the new buffer
  vim.api.nvim_create_autocmd({ "InsertEnter", "InsertCharPre" }, {
    group = group,
    buffer = bufnr,
    callback = function()
      vim.api.nvim_feedkeys(vim.api.nvim_replace_termcodes("<Esc>", true, false, true), "n", true)
      vim.notify("Insert mode is disabled in this popup", vim.log.levels.WARN)
    end})
end

return {
  make_buffer_read_only=make_buffer_read_only
}
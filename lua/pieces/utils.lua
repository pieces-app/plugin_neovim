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

local function notify_pieces_os()
  local choice = vim.fn.confirm("PiecesOS is not currently running. To use this feature, please start PiecesOS. Would you like to launch it now?", "&Yes\n&No", 1)
    if choice == 1 then
      vim.cmd("PiecesOpenPiecesOS")
    end
end
return {
  make_buffer_read_only=make_buffer_read_only,
  notify_pieces_os=notify_pieces_os
}
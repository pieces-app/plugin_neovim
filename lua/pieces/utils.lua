local function make_buffer_read_only( bufnr )
  -- Create an autogroup
  local group = vim.api.nvim_create_augroup("PreventInsertMode", { clear = true })

  -- Add autocommands to the group for the new buffer
  vim.api.nvim_create_autocmd({ "InsertEnter",  "BufEnter" }, {
    group = group,
    buffer = bufnr,
    callback = function()
      vim.api.nvim_feedkeys(vim.api.nvim_replace_termcodes("<Esc>", true, false, true), "n", true)
    end})
end

local function notify_pieces_os()
  local choice = vim.fn.confirm("PiecesOS is not currently running. To use this feature, please start PiecesOS. Would you like to launch it now?", "&Yes\n&No", 1)
    if choice == 1 then
      vim.cmd("PiecesOpenPiecesOS")
    end
end

local function notify_login()
  local choice = vim.fn.confirm("You must login to use this feature, Do you want to open the login page?", "&Yes\n&No", 1)
    if choice == 1 then
      vim.cmd("PiecesLogin")
    end
end
return {
  make_buffer_read_only=make_buffer_read_only,
  notify_login=notify_login,
  notify_pieces_os=notify_pieces_os
}

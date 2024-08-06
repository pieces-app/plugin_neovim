local M = {}

M.get_commands = function()
  local commands = {
    {
      label = "/help",
      insertText = "/help",
      kind = vim.lsp.protocol.CompletionItemKind.Function,
    },
    {
      label = "/change_model",
      insertText = "/change_model",
      kind = vim.lsp.protocol.CompletionItemKind.Function,
      args = { "model1", "model2", "model3" }
    }
  }
  return commands
end
M.filter_arg = function(command)
  local commands = M.get_commands()

  for _, value in ipairs(commands) do
    if value.insertText == command then
      if value.args then
        return value.args
      else
        break
      end
    end
  end
  return {}
end
-- Define a function to check if the buffer is empty
local function buffer_has_words()
    local bufnr = vim.api.nvim_get_current_buf()
    local lines = vim.api.nvim_buf_get_lines(bufnr, 0, -1, false)
    local first_word = false -- We should only know if the buffer contain more than one word
    -- Check if any line contains non-whitespace characters
    for _, line in ipairs(lines) do
        if line:match('%S') then
          if first_word then
            return false
          else
            first_word = true
          end
        end
    end

    return true
end

local function setup_source()
  local cmp = require('cmp')
  local source = {}

  source.complete = function(self, request, callback)
    if buffer_has_words() then
        local prev_context = request.context.prev_context
        if prev_context then
          local row = prev_context.cursor.row
          local col = prev_context.cursor.col
          local bufnr = prev_context.bufnr
          local line = vim.api.nvim_buf_get_lines(bufnr, col,row, false)

          callback({ items = M.filter_arg(line), isIncomplete = false })
        end
        local items = M.get_commands()
        -- Call the callback with the completion items
        callback({ items = items, isIncomplete = false })
    else
        -- Provide an empty result if no input
        callback({ items = {}, isIncomplete = false })
    end
  end

  cmp.register_source('pieces_slash_commands_input', source)
end

M.setup_buffer = function(bufnr)
  -- Configure nvim-cmp for the specific buffer
  require'cmp'.setup.buffer({
    sources = {
      { name = 'pieces_slash_commands_input' }
    },
  },bufnr)
  vim.api.nvim_buf_set_option(bufnr, 'omnifunc', 'v:lua.vim.lsp.omnifunc')
end

setup_source()

return M

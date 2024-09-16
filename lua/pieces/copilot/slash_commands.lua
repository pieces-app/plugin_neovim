local context = require("pieces.copilot.context.ui")
local M = {}
local commands

-- Function to return the commands with the args
local function _commands()
  local table_str = vim.fn.PiecesGetModels()
  local func, err = load("return " .. table_str)
  if not func then
      print("Error loading string:", err)
      return
  end
  local models_args = {}
  for _ , value in ipairs(func()) do
    table.insert(models_args,{
      label = value,
      insertText = value,
      kind = vim.lsp.protocol.CompletionItemKind.Text
    })
  end

  -- Define commands and their arguments in a structured table
  return {
      ["/change_model"] = {
          label = "/change_model",
          insertText = "/change_model",
          kind = vim.lsp.protocol.CompletionItemKind.Function,
          args = models_args,
          fn = vim.fn.PiecesChangeModel
      },
      ["/context"] = {
        label = "/context",
        insertText = "/context",
        kind = vim.lsp.protocol.CompletionItemKind.Function,
        fn = context.setup
      }
  }
end

-- Function to get all commands
M.get_commands = function()
    local command_list = {}
    for _, cmd in pairs(commands) do
        table.insert(command_list, cmd)
    end
    return command_list
end

-- Function to get arguments for a specific command
M.get_args = function(command)
    if commands[command] then
        return commands[command].args or {}
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
    source.new = function()
        return setmetatable({}, { __index = source })
    end

    source.complete = function(self, request, callback)
        local line = request.context.cursor_before_line
        local command = line:match("^(/%S+)")
        if command then
            local args = M.get_args(command)
            if #args > 0 then
                callback({ items = args, isIncomplete = true })
                return
            end
        end

        if buffer_has_words() then
            local items = M.get_commands()
            callback({ items = items, isIncomplete = true })
        else
            -- Provide an empty result if no input
            callback({ items = {}, isIncomplete = true })
        end
    end

    cmp.register_source('pieces_slash_commands_input', source)
end

M.setup_buffer = function(bufnr)
    -- Configure nvim-cmp for the specific buffer
    -- Don't forget to set the commands reason for that is lua loads before python
    if commands == nil then
      commands = _commands()
    end
    require 'cmp'.setup.buffer({
        sources = {
            { name = 'pieces_slash_commands_input' }
        },
    }, bufnr)
    vim.api.nvim_buf_set_option(bufnr, 'omnifunc', 'v:lua.vim.lsp.omnifunc')
end

setup_source()



function M.handle_slash(line)
    for command_name, command_list in pairs(commands) do
        if line:sub(1, #command_name) == command_name then
            local args = M.get_args(command_name)
            if args and #args > 0 then
                local arg_string = line:sub(#command_name + 2):match("^%s*(.-)%s*$") -- Trim leading/trailing whitespace

                -- Check if the arg is valid
                for _, val in ipairs(command_list.args) do
                    if val.insertText == arg_string then
                        return command_list.fn(arg_string)
                    end
                end
                return arg_string .. " is an invalid argument"

            else
                return command_list.fn()
            end
        end
    end
    return false
end


return M

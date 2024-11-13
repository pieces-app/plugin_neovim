local make_buffer_read_only = require("pieces.utils").make_buffer_read_only
local M = {}
local welcoming = {}
for line in string.gmatch([=[
```
    ____  _                        ____              _   __                _         
   / __ \(_)__  ________  _____   / __/___  _____   / | / /__  ____ _   __(_)___ ___ 
  / /_/ / / _ \/ ___/ _ \/ ___/  / /_/ __ \/ ___/  /  |/ / _ \/ __ \ | / / / __ `__ \
 / ____/ /  __/ /__/  __(__  )  / __/ /_/ / /     / /|  /  __/ /_/ / |/ / / / / / / /
/_/   /_/\___/\___/\___/____/  /_/  \____/_/     /_/ |_/\___/\____/|___/_/_/ /_/ /_/ 

```
We're thrilled to have you join us. This step-by-step guide will help you get started with the Pieces Neovim plugin, ensuring you can integrate it into your development workflow with ease.

]=], "([^\n]*)\n?") do
    table.insert(welcoming, line)
end


local steps = {
[=[
**Step 1: Save a Snippet**

- Let's get started by saving a snippet to Pieces.
- Select the following snippet, then run `:PiecesCreateSnippet`

```cmd
pip3 install pieces-cli
```
]=],
[=[
**Step 2: Manage your saved Snippets**

- Now, let's view all of your saved snippets by typing **`:PiecesSnippets`**.

  - Use <Up> and <Down> arrow keys to navigate the snippet list.
  - Press <Enter> to open the selected snippet for editing.
  - Press <Del> on the selected snippet to delete it.
  - When editing a snippet:
      i.  Press i to enter insert mode and make changes.
      ii.  Press <Esc> to exit insert mode.
      iii. Type :w and press <Enter> to save the edited snippet.
      iv.  Type :q and press <Enter> to exit the snippet editor.
]=],
[=[
**Step 3: Activate Copilot**

- Run **`:PiecesCopilot`** to Activate the Pieces Copilot to assist you with code.
  - Use /change_model in the Copilot input to change the model
  - Use /context to change the conversation context

]=],
[=[
**Step 4: Manage Conversations**

- Access your previous conversations and interactions with the Pieces Copilot using **`:PiecesConversations`**.
]=],
[=[
**Step 5: Check your account status**

- Run **`:PiecesAccount`** to Manage your Pieces account settings directly from Neovim.
]=],
[=[
**Step 6: Sharing your Feedback**

- Your feedback is very **important** to us. Please share some of your feedback by typing `:PiecesFeedback`.
]=],
[=[
**Step 7: Contributing**

- The Pieces for Neovim plugin is an **open source project** and you can contribute to it by creating a pull request or open an issue by typing **`:PiecesContribute`**.
]=]
}

local commands = {
  "'<,'>PiecesCreateSnippet",
  "PiecesSnippets",
  "PiecesCopilot",
  "PiecesConversations",
  "PiecesAccount",
  "PiecesFeedback",
  "PiecesContribute"
}

local previous_sign_line, bufnr, lines

local function update_onboarding_ui(current_step)
  local start_line = #lines + 1
  for line in string.gmatch(steps[current_step], "([^\n]*)\n?") do
    table.insert(lines, line)
  end
  vim.api.nvim_buf_set_lines(bufnr, 0, -1, false, lines)

  if previous_sign_line ~= nil then
    vim.fn.sign_place(previous_sign_line, 'onboardingSigns', "CompletedStep", bufnr, { lnum = previous_sign_line })
  end
  vim.fn.sign_place(start_line, 'onboardingSigns', "PendingStep", bufnr, { lnum = start_line })

  previous_sign_line = start_line
end


function M.start_onboarding()
  if bufnr ~= nil then
    vim.fn.sign_unplace("onboardingSigns")
  else
    bufnr = vim.api.nvim_create_buf(false, true)
  end
  lines = welcoming
  previous_sign_line = nil
  vim.fn.sign_define('CompletedStep', { text = '✔', texthl = 'PiecesSuccessMsg' })
  vim.fn.sign_define('PendingStep', { text = '↻', texthl = 'PiecesGreen' })

  if vim.fn.PiecesOpenPiecesOS() == false then
    table.insert(steps, 1, [=[Let's start by checking PiecesOS
PiecesOS is a required background service that operate the whole plugin.
Install PiecesOS using the **`:PiecesInstall`**]=])
    table.insert(commands, 1,"PiecesInstall")
  end

  vim.api.nvim_buf_set_option(bufnr, 'modifiable', true)
  vim.api.nvim_buf_set_option(bufnr, 'readonly', false)
  vim.api.nvim_buf_set_option(bufnr, 'filetype', 'markdown')
  make_buffer_read_only(bufnr)

  vim.api.nvim_win_set_buf(0, bufnr)

  local current_step = 1
  update_onboarding_ui(current_step)


  local function prompt_next_command(index)
    if index > #steps then
      vim.api.nvim_buf_delete(bufnr, { force = true })
      return
    end

    local command = commands[index]
    local augroup_id = vim.api.nvim_create_augroup("PiecesOnboarding", { clear = true })

    vim.api.nvim_create_autocmd("CmdlineLeave", {
      group = augroup_id,
      pattern = "*",
      callback = function()
        if current_step >= #steps  then -- No commands are here so let's stop
          local c = vim.api.nvim_buf_line_count(bufnr)
          vim.fn.sign_place(previous_sign_line, 'onboardingSigns', "CompletedStep", bufnr, { lnum = previous_sign_line })
          vim.api.nvim_buf_set_lines(bufnr, c, c , false, { "" ,"Now you are a `10x` developer using Pieces 🎉!"})
          return vim.api.nvim_clear_autocmds({ group = augroup_id })
        end
        local current_cmdline = vim.fn.getcmdline()
        if current_cmdline == command then
          current_step = index + 1
          update_onboarding_ui(current_step)
          prompt_next_command(index + 1)
        end
      end,
    })

  end

  prompt_next_command(1)
end
vim.api.nvim_create_user_command('PiecesOnboarding', M.start_onboarding,{})
return M

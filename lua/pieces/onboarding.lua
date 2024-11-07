local M = {}
local steps = {
[=[
**Step 1: Check Pieces Health**

- Start by checking the health of your PiecesOS using **`:PiecesHealth`** , which checks if PiecesOS is running or not.
]=],
[=[
**Step 2: Verify Versions**

- Use **`:PiecesOSVersion`**  to display the current version of your PiecesOS.
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
**Step 5: Manage Code Snippets**

- View and manage your code snippets using **`:PiecesSnippets`** .

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
**Step 6: Check your account status**

- Run **`:PiecesAccount`** to Manage your Pieces account settings directly from Neovim.

]=]
}
local commands = {
  "PiecesHealth",
  "PiecesOSVersion",
  "PiecesCopilot",
  "PiecesConversation",
  "PiecesSnippets",
  "PiecesAccounts",
}


local function update_onboarding_ui(bufnr, completed_steps, current_step)

  local lines = {
    "**Welcome to Pieces for Neovim!**",
    "We're thrilled to have you join us. This step-by-step guide will help you get started with the Pieces Neovim plugin," +
    " ensuring you can integrate it into your development workflow with ease."
  }

  if vim.fn.PiecesOpenPiecesOS then
    table.concat( lines, [=[
Let's start by checking PiecesOS 
PiecesOS is a required background service that operate the whole plugin.
Install PiecesOS using the **:PiecesInstall**
  ]=])
    table.concat( commands, "PiecesInstall", 1 )
  end

  for i, step in ipairs(steps) do
    if completed_steps[i] or i == current_step then
      table.insert(lines, step)
    end
  end
  vim.api.nvim_buf_set_lines(bufnr, 0, -1, false, lines)

  -- Clear existing signs
  vim.fn.sign_unplace('onboardingSigns', { buffer = bufnr })

  -- Define signs for completed and pending steps
  vim.fn.sign_define('CompletedStep', { text = '✔', texthl = 'Normal' })
  vim.fn.sign_define('PendingStep', { text = '↻', texthl = 'Normal' })

  -- Place signs in the gutter
  for i, _ in ipairs(steps) do
    if completed_steps[i] or i == current_step then
      local sign_name = completed_steps[i] and 'CompletedStep' or 'PendingStep'
      vim.fn.sign_place(i, 'onboardingSigns', sign_name, bufnr, { lnum = i + 2 })
    end
  end
end

function M.start_onboarding()
  local completed_steps = {}

  local bufnr = vim.api.nvim_create_buf(false, true)
  vim.api.nvim_buf_set_option(bufnr, 'modifiable', true)
  vim.api.nvim_buf_set_option(bufnr, 'readonly', false)

  vim.api.nvim_command('botright split') 
  vim.api.nvim_win_set_buf(0, bufnr)
  vim.api.nvim_win_set_height(0, 15)

  local current_step = 1
  update_onboarding_ui(bufnr, completed_steps, current_step)

  local function mark_step_done(index)
    completed_steps[index] = true
    current_step = index + 1
    update_onboarding_ui(bufnr, completed_steps, current_step)
  end

  local function prompt_next_command(index)
    if index > #steps then
      vim.api.nvim_buf_delete(bufnr, { force = true })
      return
    end

    local command = commands[index]
    -- Create a new augroup
    local augroup_id = vim.api.nvim_create_augroup("PiecesOnboarding", { clear = true })

    vim.api.nvim_create_autocmd("CmdlineLeave", {
      group = augroup_id,
      pattern = "*",
      callback = function()
        local current_cmdline = vim.fn.getcmdline()
        if vim.fn.getcmdtype() == ':' and current_cmdline == command then
          mark_step_done(index)
          prompt_next_command(index + 1)
        end
      end,
    })

  end


  M.mark_step_done = mark_step_done
  prompt_next_command(1)
end

return M

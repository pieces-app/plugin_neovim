local tutor = [=[
# Welcome to Pieces for developers

This tutorial will help you to get started with Pieces for developers

### PiecesOS Installation

Pieces is a required background tool to run this plugin
inorder to be able to use this plugin install PiecesOS using `:PiecesInstall`{normal} command

### Save your first snippet

Go to the Visual mode and select the following snippet:

~~~ cmd
pip install pieces-cli
~~~

Run `:PiecesCreateSnippet`{normal} to create a snippet

### Open your saved snippets

Now, let's view all of your saved snippets using `:PiecesSnippets`{normal}

Navigation and actions:

- Use <Up> and <Down> arrow keys to navigate the snippet list.
- Press <Enter> to open the selected snippet for editing.
- Press <Del> on the selected snippet to delete it.
- When editing a snippet:
- Press i to enter insert mode and make changes.
- Press <Esc> to exit insert mode.
- Type `:w`{vim} `<Enter>`{normal}.
- Type `:q`{vim} `<Enter>`{normal}.


### Chat with the Copilot

You can chat with multiple LLM models using `:PiecesCopilot`{normal}
If you want to change the LLM model write `/change_model <model_name>` in the copilot input
Also you can manage the Copilot context using `/context`


### Pieces Account and Personal cloud

You can login to Pieces using `:PiecesLogin`{normal} then connect to the cloud using `:PiecesConnectCloud`{normal}

Key features of connecting to the cloud:

- Cloud backups
- Link sharing
- Cloud ML
- Cloud integrations

### Feedback

Your feedback is very **important** to us. Please share some of your feedback by typing `:PiecesFeedback`{normal}.

### Contribute

The Neovim plugin is an **open source project** and you can contribute to it by creating a pull request or open an issue by typing `:PiecesContribute`{normal}.

]=]

-- Function to check for a file and create it if it doesn't exist
local function ensure_tutor_file()
  local tutor_dir = nil
  local runtime_files = vim.api.nvim_get_runtime_file("tutor", true)
  for _, file in ipairs(runtime_files) do
    if file:match("tutor$") then
      tutor_dir = file
      break
    end
  end
  if tutor_dir then
    local pieces_file_path = tutor_dir .. "/Pieces.tutor"
    local file = io.open(pieces_file_path, "r")

    if file and file:read("*a") == tutor then
      file:close()
    else
      -- File does not exist, create it
      file = io.open(pieces_file_path, "w")
      if file then
        file:write(tutor)
        file:close()
      else
      end
    end
  else
  end
end

ensure_tutor_file()

# [Pieces for Developers](https://pieces.app) | Neovim Plugin

# Important

Please make sure you have [**Pieces OS**](https://docs.pieces.app/installation-getting-started/what-am-i-installing) installed to run the Package.

## Getting Started with the Pieces Neovim Plugin

Welcome to the **Pieces Neovim Plugin**!

Neovim Plugin offers extensive functionality to interact with Pieces OS.

## Installation

### Using vim-plug

1. Add the following lines to your `init.vim` or `init.lua`:

```vim
" init.vim
call plug#begin('~/.vim/plugged')

Plug 'kyazdani42/nvim-web-devicons'
Plug 'MunifTanjim/nui.nvim'
Plug 'hrsh7th/nvim-cmp'
Plug 'pieces-app/plugin_neo_vim'

call plug#end()
```

2. Install the plugins by running `:PlugInstall` in Neovim.

### Using packer.nvim

1. Add the following lines to your `init.lua`:

```lua
-- init.lua
vim.cmd [[packadd packer.nvim]]

return require('packer').startup(function()
  use 'kyazdani42/nvim-web-devicons'
  use 'MunifTanjim/nui.nvim'
  use 'hrsh7th/nvim-cmp'
  use 'pieces-app/plugin_neo_vim'
end)
```

2. Install the plugins by running `:PackerSync` in Neovim.

3. Run :UpdateRemotePlugins

## Configuration

After installing the plugin, you can configure the host by adding the following lines to your `init.vim` or `init.lua`:

```lua
require("pieces_config").host = "http://localhost:1000"
```

By default the host will be http://localhost:1000 on Windows and MacOS and http://localhost:5323 on Linux

## Usage

Once installed and configured, you can start using Plugin Neo Vim by following the usage instructions provided in the [documentation](https://github.com/pieces-app/plugin_neo_vim).

## Contributing

Contributions are welcome! Please read the [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on how to contribute to this project.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
```

Feel free to customize the README further based on your specific needs and additional details about your plugin.
## Commands

### `:PiecesHealth`

Check the Pieces OS Health 

### `:PiecesOSVersion`

Displays the Pieces OS version

### `:PiecesPluginVersion`

Displays the current version of the plugin

### `:PiecesCopilot`

Opens the Pieces Copilot in a split view

#### Slash commands
You can write the slash command in the Copilot input to enter a command.

- change_model: used to change the current LLM model

### `:PiecesConversations`

Opens a conversations list to choose a conversation from.

- Press <del> on the selected conversation to delete it
- Press <Up> arrow to go up in the conversation list
- Press <Down> arrow to go down in the conversation list
- Press <Enter> to open the conversation in the Copilot

### `:PiecesSnippets`

List the Snippets Saved

- Press <del> on the selected snippet to delete it
- Press <Up> arrow to go up in the snippet list
- Press <Down> arrow to go down in the snippet list
- Press <Enter> to open the snippet for you to edit, Also don't forget to save using the `:w` command to save the edited snippet 

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
Plug 'pieces-app/plugin_neovim'

call plug#end()
```

Install the plugins by running `:PlugInstall` in Neovim.

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
Install the plugins by running `:PackerSync` in Neovim.



2. download python and pynvim (`pip install pynvim`)

3. Run :UpdateRemotePlugins


## Commands

The Pieces Neovim plugin provides several commands to interact with Pieces OS. Here's a list of available commands:

## General Commands

### `:PiecesHealth`

Check the health of Pieces OS.

```vim
:PiecesHealth
```

### `:PiecesOSVersion`

Display the version of Pieces OS.

```vim
:PiecesOSVersion
```
### `:PiecesPluginVersion`

Display the current version of the Pieces Neovim plugin.

```vim
:PiecesPluginVersion
```

## Copilot Commands 

### `:PiecesCopilot`

Open the Pieces Copilot window in a split view. 

```vim
:PiecesCopilot
```

#### Using the Copilot Chat

1. Press `i` to enter insert mode and type your message.
2. Press `<Esc>` to exit insert mode.
3. Press `<Enter>` to send the message to Pieces Copilot and see the response.

#### Copilot Chat Commands

In the Copilot chat input, you can use slash commands to perform specific actions:

####  `/change_model`

Change the current LLM model.

### `:PiecesChats`

Open a list of Pieces Copilot conversations to choose from.

```vim
:PiecesChats
```
Navigation and actions:
- Press `<Del>` on the selected conversation to delete it
- Use `<Up>` and `<Down>` arrow keys to navigate the conversation list
- Press `<Enter>` to open the selected conversation in the Copilot

## Asset Management Commands

### `:PiecesDrive`

List all of the saved matierals.

```vim
:PiecesDrive
```
Navigation and actions:
- Use `<Up>` and `<Down>` arrow keys to navigate the matieral list.
- Press `<Enter>` to open the selected matieral for editing.
- Press `<Del>` on the selected matieral to delete it.
- When editing a matieral:
  1. Press `i` to enter insert mode and make changes.
  2. Press `<Esc>` to exit insert mode.
  3. Type `:w` and press `<Enter>` to save the edited matieral.
  4. Type `:q` and press `<Enter>` to exit the matieral editor.


### `:PiecesCreateMatieral`

Create a matieral from the selected text in the visual mode.

```vim
:PiecesCreateMatieral
```

1. Enter visual mode by pressing `v` in normal mode.
2. Select the desired text using arrow keys or Vim motions.
3. Type `:PiecesCreateMatieral` and press `<Enter>`.

## Auth Commands

### `:PiecesAccount`

Shows your Pieces account information such as Username, Email, Personal Cloud Status and Personal Domain in a new window.  

```vim
:PiecesAccount
```
You can also logout from your account by going to the `Logout` option in the Auth status menu and then press `enter`. You will be logged out of your Pieces account.

### `:PiecesLogin`

Login to your Pieces account.

```vim
:PiecesLogin
```

### `:PiecesLogout`

Logout of your Pieces account.

```vim
:PiecesLogout
```

### `:PiecesConnectCloud`

Connect to your Personal Pieces Cloud. 

```vim
:PiecesConnectCloud
```

### `:PiecesDisconnectCloud`

Disconnect from your Personal Pieces Cloud.

```vim
:PiecesDisconnectCloud
```
 Note: In order to use the Personal Pieces Cloud commands, you must have an account connected to Pieces OS.

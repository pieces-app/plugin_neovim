local setup = require('pieces_assets.ui').setup
vim.api.nvim_create_user_command("PiecesSnippets", setup, {})
return {setup = setup}
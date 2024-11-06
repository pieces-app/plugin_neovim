vim.api.nvim_create_user_command('PiecesFeedback', function()
    local choice = vim.fn.confirm(
[=[Thank you for using Pieces for Neovim!
We always care about your feedback.
Feel free to share your experience with us.
https://github.com/pieces-app/plugin_neovim/discussions/194
Would you like to open GitHub? ]=],
        "&Yes\n&No", 1)
    if choice == 1 then
        vim.fn.PiecesOpenLink("https://github.com/pieces-app/plugin_neovim/discussions/66")
    end
end, {})

vim.api.nvim_create_user_command('PiecesContribute', function()
    local choice = vim.fn.confirm(
[=[Contribute to the project
https://github.com/pieces-app/plugin_neovim
Would you like to open the feedback page in your browser?]=]
    , "&Yes\n&No", 1)
    if choice == 1 then
        vim.fn.PiecesOpenLink("https://github.com/pieces-app/plugin_neovim/")
    end
end, {})

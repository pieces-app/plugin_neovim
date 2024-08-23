" Set the highlight attributes for NonText
hi def PiecesAnnotation guifg=#888888 gui=italic ctermfg=8
hi def PiecesWarningMsg guifg=Yellow
hi def PiecesSuccessMsg guifg=Green
hi def PiecesErrorMsg guifg=Red
hi def PiecesUrl guifg=#0000EE gui=underline


function! RunPiecesStartup()
    try
        call PiecesStartup()
    catch /^Vim\%((\a\+)\)\=:E/
        call nvim_command('UpdateRemotePlugins')
        echohl WarningMsg
        echomsg 'Warning: Please restart Neovim to ensure the Pieces Plugin works correctly.'
        echohl None
    endtry
endfunction


" Autocommand to run the function after NeoVim has fully started
autocmd VimEnter * call RunPiecesStartup()

command! -range=% PiecesCreateSnippet <line1>,<line2>lua require('pieces_assets.create').setup(<line1>, <line2>)

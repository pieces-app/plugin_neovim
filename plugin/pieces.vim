" Set the highlight attributes for NonText
hi def PiecesAnnotation guifg=#888888 gui=italic ctermfg=8
hi def PiecesWarningMsg guifg=Yellow
hi def PiecesSuccessMsg guifg=Green
hi def PiecesErrorMsg guifg=Red
hi def PiecesUrl guifg=#0000EE gui=underline

function! PiecesRunRemotePlugins()
    call nvim_command('UpdateRemotePlugins')
    echohl WarningMsg
    echomsg 'Warning: The Pieces Plugin has been updated. To ensure it functions correctly, please restart Neovim.'
    echohl None
endfunction

function! RunPiecesStartup()
    try
        call PiecesStartup()
    catch /^Vim\%((\a\+)\)\=:E/
        call PiecesRunRemotePlugins()
    endtry
endfunction


" Autocommand to run the function after NeoVim has fully started
autocmd VimEnter * call RunPiecesStartup()


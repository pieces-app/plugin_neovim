" Set the highlight attributes for NonText
hi def PiecesAnnotation guifg=#888888 gui=italic ctermfg=8


function! RunPiecesStartup()
    try
        call PiecesStartup()
    catch /^Vim\%((\a\+)\)\=:E/
        echohl WarningMsg
        echomsg 'Please run :UpdateRemotePlugins'
        echohl None
    endtry
endfunction


" Autocommand to run the function after NeoVim has fully started
autocmd VimEnter * call RunPiecesStartup()

command! -range=% PiecesCreateSnippet <line1>,<line2>lua require('pieces_assets.create').setup(<line1>, <line2>)

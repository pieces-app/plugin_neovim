" Set the highlight attributes for NonText
hi def PiecesAnnotation guifg=#888888 gui=italic ctermfg=8
" Define a function to call vim.fn.PiecesStartup()
function! RunPiecesStartup()
    call PiecesStartup()
endfunction

" Autocommand to run the function after NeoVim has fully started
autocmd VimEnter * call RunPiecesStartup()

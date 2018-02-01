set nocompatible
if has('win32') || has('win64')
    let g:python3_host_prog = 'c:\Apps\Miniconda3\envs\neovim3\python.exe'
    let g:python_host_prog = 'c:\Apps\Miniconda3\envs\neovim2\python.exe'
    call plug#begin('~\AppData\Local\nvim\bundle')
else
    let g:python3_host_prog = '/usr/local/miniconda3/envs/neovim3/bin/python'
    let g:python_host_prog = '/usr/local/miniconda3/envs/neovim2/bin/python'
    call plug#begin('~/.local/share/nvim/bundle')
endif
Plug 'Shougo/deoplete.nvim', { 'do': ':UpdateRemotePlugins' }
call plug#end()
set runtimepath+=~/code/neovim-fsharp
filetype indent plugin on
" =============== Deoplete ======================
let g:deoplete#enable_at_startup = 1

" ================ Turn Off Swap Files ==============
set noswapfile
set nobackup
set nowb

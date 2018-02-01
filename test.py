import pytest
from neovim import attach
from time import sleep

config = '''
:set nocompatible
:let g:python3_host_prog = 'c:\Apps\Miniconda3\envs\neovim3\python.exe'
:let g:python_host_prog = 'c:\Apps\Miniconda3\envs\neovim2\python.exe'
:call plug#begin('~\AppData\Local\nvim\bundle')
:Plug 'Shougo/deoplete.nvim', { 'do': ':UpdateRemotePlugins' }
:call plug#end()
:set runtimepath+=~/code/neovim-fsharp
:filetype indent plugin on
" =============== Deoplete ======================
:let g:deoplete#enable_at_startup = 1
'''


cleanup_func = ''':function BeforeEachTest()
  tabnew
  let curbufnum = eval(bufnr('%'))
  redir => buflist
  silent ls!
  redir END
  let bufnums = []
  for buf in split(buflist, '\\n')
    let bufnum = eval(split(buf, '[ u]')[0])
    if bufnum != curbufnum
      call add(bufnums, bufnum)
    endif
  endfor
  if len(bufnums) > 0
    exe 'silent bwipeout! '.join(bufnums, ' ')
  endif
  silent tabonly
endfunction
'''


@pytest.fixture(scope="module")
def nvim():
    print("module level fixt")
    nvim = attach(
            'child',
            argv=[
                "nvim", "-u",
                "C:\\Users\\john\\code\\neovim-fsharp\\test.vimrc",
                "--embed"])
    nvim.input(cleanup_func)
    print("config and cleanup should be done")
    assert len(nvim.tabpages) == 1
    assert len(nvim.windows) == 1
    assert len(nvim.buffers) == 1
    return nvim


@pytest.fixture()
def cleanup(nvim):
    # cleanup nvim
    nvim.command('call BeforeEachTest()')
    assert len(nvim.tabpages) == 1
    assert len(nvim.windows) == 1
    assert len(nvim.buffers) == 1


def eventually_has_output(nvim, output, timeout):
    attempts = timeout
    result = False

    while attempts > 0:
        content = nvim.funcs.getreg('a', 1, True)[-1]
        if content == output:
            result = True
            break
        sleep(1)
        attempts -= 1
    return result


def test_get_type(nvim, cleanup):
    nvim.command('redir @a')
    nvim.command(r'e C:\Users\john\code\vim-fsharp\install.fsx')
    window = nvim.current.window
    window.cursor = [14, 7]
    nvim.command('FSharpGetType')
    result = eventually_has_output(nvim, "val vimInstallDir : string", 5)
    assert result is True


def test_get_type2(nvim, cleanup):
    nvim.command('redir @a')
    nvim.command(r'e C:\Users\john\code\vim-fsharp\install.fsx')
    window = nvim.current.window
    window.cursor = [35, 4]
    nvim.command('FSharpGetType')
    result = eventually_has_output(nvim, "val Target : name:string -> body:(unit -> unit) -> unit", 5)
    assert result is True

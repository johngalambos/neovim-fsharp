import sys
import os
import neovim
sys.path.insert(1, os.path.dirname(__file__))
from fsharpvim import FSAutoComplete, G


@neovim.plugin
class NvimFsharp(object):

    # start up the process remotely
    # for every command we send, echo it through the process
    # see what happens to stdin and stdout
    def __init__(self, vim):
        self.vim = vim
        self.plugin_dir = os.path.abspath(
                os.path.join(os.path.dirname(__file__), '..\\..\\'))
        self.__log('Plugin path: {}'.format(self.plugin_dir))

    def __log(self, message):
        self.vim.command('echomsg "{}"'.format(message))

    @neovim.autocmd(
            'BufEnter', pattern='*.fsx,*.fs',
            eval='expand("<afile>")', sync=True)
    def autocmd_handler(self, filename):
        self.__log("Reloaded")
        fsharp_dir = os.path.dirname(filename)
        self.__log("Entered the buffer filename: {}".format(filename))
        self.__log("setting fsharp_dir to {}".format(fsharp_dir))
        if G.fsac is None:
            G.fsac = FSAutoComplete(self.plugin_dir, self.vim, debug=True)
            self.__log("The service should be started! Parsing file")

        G.fsac.parse(
            self.vim.current.buffer.name, True,
            self.vim.current.buffer)

    @neovim.autocmd('VimLeavePre', pattern='*', sync=False)
    def vim_leave_handler(self, filename):
        self.__log('shutting down fsac')
        G.fsac.shutdown()

    @neovim.command('FSharpGetType', range='', nargs='*', sync=True)
    def command_handler(self, args, range):
        if G.fsac is None:
            self.__log("FSAC not started yet")
            return

        # G.fsac.parse(
        #     self.vim.current.buffer.name, True,
        #     self.vim.current.buffer)

        b = self.vim.current.buffer
        # G.fsac.parse(b.name, True, b)
        row, col = self.vim.current.window.cursor
        # TODO John
        # res = G.fsac.tooltip(b.name, row, col + 1, self.vim.eval('a:includeComments') != '0')
        # this is not synchronous
        res = G.fsac.tooltip(b.name, row, col + 1, False)
        lines = res.splitlines()
        self.vim.out_write("len lines: {}\n".format(str(len(lines))))
        first = ""
        if len(lines):
            first = lines[0]
        if first.startswith('Multiple') or first.startswith('type'):
            self.vim.out_write("{0}\n".format(res))
        elif first.startswith('HasComments'):
            self.vim.out_write("{0}\n".format(res.replace("HasComments", "", 1)))
        else:
            self.vim.out_write('{0}\n'.format(first))

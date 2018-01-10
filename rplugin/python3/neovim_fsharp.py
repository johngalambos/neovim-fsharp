import neovim
import subprocess


@neovim.plugin
class Fsac(object):
    server_handle = None

    # start up the process remotely
    # for every command we send, echo it through the process
    # see what happens to stdin and stdout
    def __init__(self, vim):
        self.vim = vim
        self.count = 0

    def __log(self, message):
        self.vim.command('echomsg "{}"'.format(message))

    @neovim.command('JStartServer', range='', nargs='*')
    def command_handler(self, args, range):
        self.start()
        self.__log("JStartServer2")
        while True:
            content = Fsac.server_handle.stdout.readline()
            self.__log(content)

    @neovim.command('JStopServer', range='', nargs='*', sync=True)
    def command_handler2(self, args, range):
        self.__log("JStopServer2")
        self.stop()

    @neovim.autocmd('BufEnter', pattern='*.py', eval='expand("<afile>")',
                    sync=True)
    def autocmd_handler(self, filename):
        self.__log("BufEnter")

    @neovim.command('JCommunicate', range='', nargs='*', sync=False)
    def communicate(self, args, range):
        msg = "Hello {}\n".format(self.count)
        self.__log("Sending " + msg)
        Fsac.server_handle.stdin.write(msg)
        Fsac.server_handle.stdin.flush()
        self.count += 1

    @neovim.function('JohnnyFunc')
    def function_handler(self, args):
        self.__log("JohnnyFunc")

    def start(self):
        Fsac.server_handle = subprocess.Popen(
            [
                "dotnet",
                r"C:\Users\john\code\temp\dotnetnew\bin\Debug\netcoreapp2.0\dotnetnew.dll"
            ],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True
        )

    def stop(self):
        self.__log("StopServer")
        Fsac.server_handle.kill()



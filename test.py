from neovim import attach
from time import sleep
nvim = attach('child', argv=["nvim", "--embed"])
buffer = nvim.current.buffer
window = nvim.current.window
firstcontent = nvim.funcs.getreg('a', 1, True)
print('first content ' + str(firstcontent))
nvim.command('redir @a')
nvim.command(r'e C:\Users\john\code\vim-fsharp\install.fsx')
sleep(5)
window.cursor = [14, 7]
attempts = 4

while attempts > 0:
    print('injecting command')
    nvim.command('FSharpGetType')
    sleep(5)
    content = nvim.funcs.getreg('a', 1, True)
    print(str(content))
    attempts -= 1

print("finished test")

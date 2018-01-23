import pytest
from neovim import attach
from time import sleep

nvim = attach('child', argv=["nvim", "--embed"])
firstcontent = nvim.funcs.getreg('a', 1, True)
print('first content ' + str(firstcontent))


@pytest.fixture(scope="module")
def nvim():
    # fixt = { "name": "test" }
    # return fixt
    nvim = attach('child', argv=["nvim", "--embed"])
    nvim.command(r'e C:\Users\john\code\vim-fsharp\install.fsx')
    print("fixture sleep")
    sleep(5)
    print("fixture wake")
    nvim.command('redir @a')
    return nvim


def eventually_has_output(nvim, output, timeout):
    attempts = timeout
    print("attempts {} timeout {}".format(attempts, timeout))

    while attempts > 0:
        print("inside loop attempts {} timeout {}".format(attempts, timeout))
        content = nvim.funcs.getreg('a', 1, True)
        print("output {} is {}".format(attempts, str(content)))
        if content == output:
            return True
        attempts -= 1
        sleep(1)
    return False


def test_get_type(nvim):
    window = nvim.current.window
    window.cursor = [14, 7]
    nvim.command('FSharpGetType')
    result = eventually_has_output(nvim, "type", 5)
    assert result is True

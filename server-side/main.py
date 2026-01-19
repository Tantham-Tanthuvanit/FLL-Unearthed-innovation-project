import os
import sys

if os.name == "nt":
    import msvcrt
    os.system("cls")

    def get_key():
        ch = msvcrt.getch()
        try:
            return ch.decode()
        except UnicodeDecodeError:
            return ""
else:
    import tty
    import termios
    import atexit

    os.system("clear")

    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)

    tty.setraw(fd)

    def restore():
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

    atexit.register(restore)

    def get_key():
        return sys.stdin.read(1)

while True:
    # draw UI

    ch = get_key()

    match ch:
        # ctrl + c
        case "q":
            print("break")
            break

        case _:
            print(ch)
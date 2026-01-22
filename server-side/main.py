import os
import sys
import requests

from time import sleep
from api import get_telemetry_data

get_telemetry = "http://127.0.0.1:8000/get-telemetry"

class TextColor:
    RESET = "\033[0m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"

if os.name == "nt":
    import msvcrt
    os.system("cls")

    def get_key():
        ch = msvcrt.getch()
        try:
            return ch.decode()
        except UnicodeDecodeError:
            return ""
        
    def clear_screen():

        _ = os.system("cls")


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

    def clear_screen():

        _ = os.system("clear")

tab = 0
selected_row = 0

menue_options = [
    "dashboard",
    "add data"
]

while True:
    # draw UI

    match tab:
        case 0:
            for i in range(len(menue_options)):
                print(f"{TextColor.GREEN} [ {menue_options[i]} ] {TextColor.RESET}") if i == selected_row else print(f"   {menue_options[i]}")

        case 1:
            response = requests.get(get_telemetry)

            if response.status_code == 200:
                telemetry = response.json()

                try:

                    fan_state1 = (
                        f"{TextColor.GREEN}spinning{TextColor.RESET}" if telemetry["fan1"] else f"{TextColor.RED}not spinning{TextColor.RESET}"
                    )

                    fan_state2 = (
                        f"{TextColor.GREEN}spinning{TextColor.RESET}" if telemetry["fan2"] else f"{TextColor.RED}not spinning{TextColor.RESET}"
                    )

                    # print out states
                    print(f"""{TextColor.YELLOW}
███████╗ █████╗ ███╗   ██╗
██╔════╝██╔══██╗████╗  ██║
█████╗  ███████║██╔██╗ ██║
██╔══╝  ██╔══██║██║╚██╗██║
██╔══╝  ██╔══██║██║╚██╗██║   :   {TextColor.RESET} {fan_state1}""")
                    print(f"{TextColor.YELLOW}Fan2   :   {TextColor.RESET} {fan_state2}")

                except Exception as e:
                    print(f"Error : {e}")

            else:
                print("Error:", response.status_code)

    print("\n\n\n\n[Q]uit       [B]ack")
        

    ch = get_key()

    match ch:
        # ctrl + c
        case "q":
            print("break")
            clear_screen()
            break
            
        case "s":
            selected_row = (selected_row + 1)%len(menue_options)

        case "w":
            selected_row = (selected_row - 1)

            if selected_row < 0:
                selected_row = len(menue_options)-1

        case "b":
            tab = 0

        case " ":
            match selected_row:
                case 0:
                    tab = 1
                case 1:
                    tab = 2


    clear_screen()            
import os
import sys
import requests
import select

from time import sleep, time
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

    def get_key(timeout=2.0):
        start = time()

        while time() - start < timeout:
            if msvcrt.kbhit():
                ch = msvcrt.getch()
                try:
                    return ch.decode()
                except UnicodeDecodeError:
                    return ""
            sleep(0.01)

        return None  # no key pressed in timeout
        
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

    def get_key(timeout=2.0):
        rlist, _, _ = select.select([sys.stdin], [], [], timeout)
        if rlist:
            return sys.stdin.read(1)
        return None


    def clear_screen():

        _ = os.system("clear")

tab = 0
selected_row = 0

spin_counter = 0

menue_options = [
    "dashboard",
    "add data"
]

#spin_anim = ["", "", "", "", "", ""]
spin_anim = ["◐", "◓", "◑", "◒"]
#spin_anim = ["|", "/", "—", "\\"]


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
                        f"{TextColor.GREEN}{spin_anim[spin_counter]}{TextColor.RESET}" if telemetry["fan1"] else f"{TextColor.RED}󱑬{TextColor.RESET}"
                    )

                    fan_state2 = (
                        f"{TextColor.GREEN}{spin_anim[spin_counter]}{TextColor.RESET}" if telemetry["fan2"] else f"{TextColor.RED}󱑬{TextColor.RESET}"
                    )

                    tempreture = (
                        f"{TextColor.GREEN}{telemetry['temperature']}°C{TextColor.RESET}" if 'temperature' in telemetry else f"{TextColor.RED}ERROR{TextColor.RESET}"
                    )

                    # print out states
                    print(f"{TextColor.YELLOW}Fan1   :   {TextColor.RESET} {fan_state1}")
                    print(f"{TextColor.YELLOW}Fan2   :   {TextColor.RESET} {fan_state2}")
                    print(f"{TextColor.YELLOW}Temp   :   {TextColor.RESET} {tempreture}")

                except Exception as e:
                    print(f"Error : {e}")

            else:
                print("Error:", response.status_code)

    print("\n\n\n\n[Q]uit       [B]ack")
        

    ch = get_key(1)

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
        
        case None:

            spin_counter = (spin_counter + 1) % len(spin_anim)

            clear_screen()
            continue

    

    clear_screen()            
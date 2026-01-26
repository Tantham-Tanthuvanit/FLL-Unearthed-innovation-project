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

typing_lock = True

menue_options = [
    "dashboard",
    "add data"
]

ans = ["","","","","",""]
data = [
    "name",
    "id",
    "dig location",
    "date found",
    "temperature",
    "humidity"
]
selected_data = 0

#spin_anim = ["", "", "", "", "", ""]
spin_anim = ["◐", "◓", "◑", "◒"]
#spin_anim = ["|", "/", "—", "\\"]

BACKSPACE = ("\x08", "\x7f", "\b")

label_width = max(len(label) for label in data)

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
                       f"{TextColor.GREEN}{telemetry["temperature"]}°C{TextColor.RESET}" if "temperature" in telemetry else f"{TextColor.RED}ERROR{TextColor.RESET}"
                    )

                    humidity =  (
                        f"{TextColor.GREEN}{telemetry["humidity"]}%{TextColor.RESET}" if "humidity" in telemetry else f"{TextColor.RED}ERROR{TextColor.RESET}"
                    )

                    motor1 = (
                        f"{TextColor.GREEN}running{TextColor.RESET}" if telemetry["motor1"] else f"{TextColor.RED}stopped{TextColor.RESET}"
                    )

                    motor2 = (
                        f"{TextColor.GREEN}running{TextColor.RESET}" if telemetry["motor2"] else f"{TextColor.RED}stopped{TextColor.RESET}"
                    )

                    # print out states
                    print(f"{TextColor.YELLOW}Fan1   :   {fan_state1}")
                    print(f"{TextColor.YELLOW}Fan2   :   {fan_state2}")
                    print(f"{TextColor.YELLOW}Temp   :   {tempreture}")
                    print(f"{TextColor.YELLOW}Humi   :   {humidity}")
                    print(f"{TextColor.YELLOW}Mot1   :   {motor1}")
                    print(f"{TextColor.YELLOW}Mot2   :   {motor2}")

                except Exception as e:
                    print(f"Error : {e}")

            else:
                print("Error:", response.status_code)

        case 2:


            for i in range(len(data)):

                buf = (
                    f"{TextColor.GREEN}>" if i == selected_data else f"{TextColor.GREEN} "
                )
                
                label = f"{TextColor.YELLOW}{data[i]:<{label_width}}{TextColor.RESET}" if i == selected_data else f"{data[i]:<{label_width}}"
                print(f"{buf}{label}  :   {ans[i]}")




    if tab == 2:
        print(f"\n\n\n\n{TextColor.RESET}[Q]uit       [B]ack       [P]ush")
    else:
        print(f"\n\n\n\n{TextColor.RESET}[Q]uit       [B]ack")
        

    ch = get_key(1)

    if typing_lock and tab == 2 and ch:
        if ch == " ":
            typing_lock = not typing_lock

        elif ch in BACKSPACE:
            ans[selected_data] = ans[selected_data][:-1]

        elif ch.isprintable():
            ans[selected_data] += ch
    else:
        match ch:
            # ctrl + c
            case "q":
                print("break")
                clear_screen()
                break
                
            case "s":
                if tab == 2 and not typing_lock:
                    selected_data = (selected_data +1) % len(ans)

                else:
                    selected_row = (selected_row + 1)%len(menue_options)

            case "w":
                if tab == 2 and not typing_lock:
                    selected_data -= 1

                    if selected_data < 0:
                        selected_data = len(ans)-1
                else:
                    selected_row = (selected_row - 1)

                    if selected_row < 0:
                        selected_row = len(menue_options)-1

            case "p":
                if tab == 2 and not typing_lock:
                    payload = {
                        "name": ans[0],
                        "id": ans[1],
                        "dig_location": ans[2],
                        "date_found": ans[3],
                        "temperature": int(ans[4]),
                        "humidity": int(ans[5])
                    }

                    response  = requests.post("http://localhost:8000/send-data", json=payload)

            case "b":
                tab = 0

            case " ":

                if tab == 2:
                    typing_lock = not typing_lock
                else:
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
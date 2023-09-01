# debug.py: Mikko Heinänen 2023
# debug.py is called when the timer service fails to run main.py
#          So this will have to collect all the required info and dump it
#          in the debug channel
from main import *
import platform
import subprocess
import argparse
from datetime import datetime


# Num of charactes the dump can have at max
dc_max_message_lenght = 2000


def total_len(list_of_strings: list[str]) -> int:
    lenght = int()

    for i in list_of_strings:
        lenght = lenght + len(i)

    return lenght

def trim_to_character_lenght(lenght, list_of_strings: list[str]) -> list[str]:
    list_lenght = total_len(list_of_strings) 
    list_over_lenght = max(list_lenght - lenght, 0)

    if list_over_lenght == 0:
        return list_of_strings

    index = int()
    removed_lenght = int()
    # calculate how many lines need to be removed to satisfy lenght limit
    for i in range(0, len(list_of_strings)):
       removed_lenght = removed_lenght + len(list_of_strings[i])

       if removed_lenght >= list_over_lenght:
           index = i
           break

    # Remove the lines
    del list_of_strings[0:index]
    return list_of_strings

def convert_list_of_strings_to_string(list_of_strings: list[str]) -> str:
    output = str()

    for i in list_of_strings:
        output += i

    return output


if __name__=="__main__":
    parser = argparse.ArgumentParser(
        prog='debug.py',
        description='sends debug data to discord',
        epilog='@Mixkus'
    )
    parser.add_argument('-d', '--debug', action='store_true', help='reroutes messages being sent to discord to stdout')
    shell_args = parser.parse_args()


    # Let's collect the logs of bot.service from journalctl
    service_log_msg = subprocess.run(['journalctl -u bot.service | grep "$(date +"%b %d")"'], stdout=subprocess.PIPE, shell=True).stdout.decode('utf-8')
    service_log_msg = service_log_msg.splitlines()
    service_log_len = len(service_log_msg)

    # Append system info to the message list
    message = []
    message.append("**Error dump " + str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")) +  "**\n")
    message.append("\nSys info:\n")
    message.append("```")
    message.append("OS:   " + str(platform.system()) + '\n')
    message.append("Kernel: " + str(platform.release()) + '\n')
    message.append("CPU:  " + str(platform.processor()) + '\n')
    message.append("arch: " + str(platform.architecture()) + '\n')
    message.append("```\n")

    # Append python info
    message.append("Python info:\n")
    message.append("```")
    message.append("implementation: " + str(platform.python_implementation()) + '\n')
    message.append("version:        " + str(platform.python_version()) + '\n')
    message.append("```\n")

    # Add \n to all service_log_msg line ends
    for i in range(0, len(service_log_msg)):
        service_log_msg[i] += '\n'

    # Trim service_log_msg to fit under the 2000 character limit
    service_log_msg = trim_to_character_lenght(dc_max_message_lenght - total_len(message) - 100, service_log_msg)

    # Append bot.service error log
    message.append("bot.service dump: " + str(len(service_log_msg)) + " of " + str(service_log_len) + " lines shown\n")
    message.append("```")
    message = message + service_log_msg
    message.append("\n```")

    print("Sending message which contains " + str(total_len(message)) + " characters")

    # Check if not in debug mode
    if shell_args.debug == 0:
        send_debug(convert_list_of_strings_to_string(message))
        exit(1)

    print("--- start of debug output ---\n")
    print(convert_list_of_strings_to_string(message))
    print("\n--- End of debug output ---")
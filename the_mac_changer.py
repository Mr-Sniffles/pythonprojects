#!/usr/bin/env python3

import subprocess
import optparse
import re

#guettering the arguments:
def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="Interface to change its MAC ADD")
    parser.add_option("-n", "--mac", dest="new_mac", help="New MAC Address")
    (options, arguments) = parser.parse_args()
    #checking the values:
    if not options.interface:
        parser.error("[-] Please specify an interface")
    elif not options.new_mac:
        parser.error("[-] Please specify a new MAC Address")
    return options

#changing the linux mac address(we will combine the inputs)):
def change_mac(interface, new_mac):
    # FIRST WAY:(an unsecured way, cause allows to the user to put other shell commands, with ->
    # <command1>;<command2>
    # subprocess.call("ip link set dev " + interface + " down", shell=True)
    # subprocess.call("ip link set dev " + interface + " address " + new_mac, shell=True)
    # subprocess.call("ip link set dev " + interface + " up", shell=True)
    # print("[+]Changing MAC address for: " + interface + " to: " + new_mac)
    # SECOND WAY:(a more secured way, not allowing that issue, using lists)

    """with this way, put the shell command in a single string first, then separate them,
    to create your list (without the ' ')"""

    subprocess.call(["ip", "link", "set", "dev", interface, "down"])
    subprocess.call(["ip", "link", "set", "dev", interface, "address", new_mac])
    subprocess.call(["ip", "link", "set", "dev", interface, "up"])
    print("[+]Changing MAC address for: " + interface + " to: " + new_mac)

#steps 1 and 2 to the algorithm
def get_current_mac(interface):
    ifconfig_result = subprocess.check_output(["ifconfig", interface])
    mac_add_sr = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_result.decode("utf-8"))
    if mac_add_sr:
        return mac_add_sr.group(0)
    else:
        print("[-] MAC address not found in ifconfig")

options = get_arguments()

#A simple algorithm to show us if the MAC was really changed...
"""
The goal -> Check if MAC address was changed.
    Steps:
        1) Execute and read ifconfig
        2) Read the MAC address from output
        3) Check if MAC in ifconfig is what the user requested 
        4) print appropriate message
"""
#takes the value before it changes:
current_mac = get_current_mac(options.interface)
print("Current MAC= "+ str(current_mac))
#when it will change:
change_mac(options.interface, options.new_mac)
current_mac = get_current_mac(options.interface)
#checking part (step 3 and 4)
if current_mac == options.new_mac:
    print("[+] MAC address changed successfully to " + current_mac )
else:
    print("[-] MAC address not changed to: " + current_mac )






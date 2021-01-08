from classes.device import NetworkDevice
from helpers.fileio import FileToList, FileToDict
import argparse
import sys

# User-defined variables
local_credentials = ("admin", "admin")
enable_password = "secret"

# Answer file locations - Update as needed
windowsanswer_file = "windowsanswer.txt"
variables_file = "variables.ps1"
devices_file = "devices.txt"

# Shouldn't need to change these
devices = FileToDict(devices_file, "=")
answerfile = FileToDict(windowsanswer_file,"=")
variablesfile = FileToDict(variables_file, "=", remove_quotes=True)
domain_credentials = ("{0}\{1}".format(
                       answerfile['domain_identifier'], 
                       answerfile['user']
                       ), answerfile['pass'])

# Used for debugging
#print(windowsanswer)
#print(variablesfile)

''' Replace values in command with data from an answer file '''
def replace(command):
    if "DOMAIN_CONTROLLER_IP" in command:
        command = command.replace("DOMAIN_CONTROLLER_IP", answerfile['ap01_ip'])
    if "VCENTER_PASSWORD" in command:
        command = command.replace("VCENTER_PASSWORD", variablesfile['$vcenter_pass'])
    return command


''' Write each command to device '''
def applyconfig(device, commands):
    print("Configuring device...")
    for command in commands:
        command = replace(command)
        response = device.write(command, 1.0)
        print(response.decode('utf-8'))
    print("Configuration complete.")
    device.disconnect()


''' Login and configure each device '''
def run(commands):
    for name, ipaddr in devices.items():
        # Create device object
        device = NetworkDevice(ipaddr)

        # Try accessing device using a domain account
        domain_access = device.connect(auth=domain_credentials, en_password=enable_password)

        if domain_access:
            # domain login was successful, configure anyway...
            applyconfig(device, commands)
        else:
            # domain account failed. Connect using a local device account
            connected = device.connect(auth=local_credentials, en_password=enable_password)
            if connected:
                # configure the device
                applyconfig(device, commands)
            

''' Start here '''
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='''
    This script applies network device configurations from an external file
    ''')
    parser.add_argument("username", help="Account username")
    parser.add_argument("password", help="Account password")
    parser.add_argument("commands", help="File containing commands to execute")
    args = parser.parse_args()

    global username
    global password
    username = args.username
    password = args.password

    command_list = FileToList(args.commands)
    if command_list:
        run(command_list)
    else:
        print("There was a problem reading the commands file.")
        sys.exit(1)
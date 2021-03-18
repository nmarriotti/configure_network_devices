#from classes.protocols import Telnet, SSH
from classes.ClassConstructor import Builder
from helpers.fileio import FileToList, FileToDict
from helpers.ports import IsPortOpen
import argparse
import sys
import socket, time

# User-defined variables
local_credentials = ()
enable_password = ""

# Return dictionary of devices to configure
devices = FileToDict("devices.txt", "=")


def applyconfig(device, commands):
    ''' Write each command to device '''
    print("Configuring...")
    for command in commands:
        response = device.write(command, 0.2)
        if verbose:
            try:
                print(response.decode('utf-8'))
            except:
                print(response[-2].decode('utf-8'))
    print("Configuration complete.")
    device.disconnect()



def run(commands):
    ''' Login and configure each device '''
    for name, ipaddr in devices.items():

        # Returns the first available protocol
        protocol = IsPortOpen(ipaddr, ports=[22,23])

        # Exit if both SSH and Telnet are unavailable
        if not protocol:
            print("No ports available, skipping device...")
            continue
        else:
            print("Selected protocol:", protocol.upper())
		
        # Creates appropriate object based on protocol
        b = Builder()
        device = b.construct(protocol)(ipaddr)

        time.sleep(3)

        # Try connecting to the device
        print("Connecting to",ipaddr)
        connected = device.connect(auth=credentials, en_password=enable_password)

        if connected:
            print("Connected")
            # login was successful, execute commands
            applyconfig(device, commands)
        else:
            print("Unable to connect")
       


if __name__ == "__main__":
    ''' Start here '''
    parser = argparse.ArgumentParser(description='''
    This script applies network device configurations from an external file
    ''')
    parser.add_argument("--username", required=True, help="Account username")
    parser.add_argument("--password", required=True, help="Account password")
    parser.add_argument("--enablepass", required=True, help="Enable password")
    parser.add_argument("--commands", required=True, help="File containing commands to execute")
    parser.add_argument("--verbose", required=False, action='store_true', help="Print device output to screen")
    args = parser.parse_args()

	# Set global variables from command-line arguments
    credentials = (args.username, args.password)
    enable_password = args.enablepass

    # Set flag to trigger additional output
    verbose = args.verbose

    # Load the commands from file
    command_list = FileToList(args.commands)
	
    if command_list:
        # Connect/configure device
        print("Automated Network Device Configuration")
        print("======================================")
        run(command_list)
    else:
        print("There was a problem reading the commands file.")
        sys.exit(1)
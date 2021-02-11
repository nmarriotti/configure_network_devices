#from classes.protocols import Telnet, SSH
from classes.ClassConstructor import Builder
from helpers.fileio import FileToList, FileToDict
from helpers.ports import IsPortOpen
import argparse
import sys
import socket, time

# User-defined variables

def applyconfig(device, commands):
    ''' Write each command to device '''
    sys.stdout.write("Configuring...\n")
    sys.stdout.flush()
    for command in commands:
        response = device.write(command, 0.2)
        if verbose:
            try:
                sys.stdout.write(response.decode('utf-8') + '\n')
            except:
                sys.stdout.write(response[-2].decode('utf-8') + '\n')
            sys.stdout.flush()
    sys.stdout.write("Configuration complete.\n")
    sys.stdout.flush()
    device.disconnect()



def run(commands):
    ''' Login and configure each device '''
    for name, ipaddr in devices.items():

        # Returns the first available protocol
        protocol = IsPortOpen(ipaddr, ports=[22, 23])

        # Exit if both SSH and Telnet are unavailable
        if not protocol:
            sys.stdout.write("No ports available, skipping device...\n")
            continue
        else:
            sys.stdout.write("Selected protocol: {0}\n".format(protocol.upper()))
		
        sys.stdout.flush()

        # Creates appropriate object based on protocol
        b = Builder()
        device = b.construct(protocol)(ipaddr)

        time.sleep(3)

        # Try connecting to the device
        sys.stdout.write("Connecting to {0}\n".format(ipaddr))
        sys.stdout.flush()
        connected = device.connect(auth=credentials, en_password=enable_password)

        if connected:
            sys.stdout.write("Connected\n")
            sys.stdout.flush()
            # login was successful, execute commands
            applyconfig(device, commands)
        else:
            sys.stdout.write("Unable to connect\n")
            sys.stdout.flush()
       


if __name__ == "__main__":
    ''' Start here '''
    parser = argparse.ArgumentParser(description='''
    This script applies network device configurations from an external file
    ''')
    parser.add_argument("--devices", required=True, help="File containing list of devices")
    parser.add_argument("--username", required=True, help="Account username")
    parser.add_argument("--password", required=True, help="Account password")
    parser.add_argument("--enablepass", required=True, help="Enable password")
    parser.add_argument("--commands", required=True, help="File containing commands to execute")
    parser.add_argument("--verbose", required=False, action='store_true', help="sys.stdout.write device output to screen")
    args = parser.parse_args()

	# Set global variables from command-line arguments
    credentials = (args.username, args.password)
    enable_password = args.enablepass
 
    # Set flag to trigger additional output
    verbose = args.verbose

    # Load devices from file
    devices = FileToDict(args.devices, "=")

    # Load the commands from file
    command_list = FileToList(args.commands)
	
    if command_list:
        # Connect/configure device
        sys.stdout.write("Automated Network Device Configuration\n")
        sys.stdout.write("======================================\n")
        sys.stdout.flush()
        run(command_list)
    else:
        sys.stdout.write("There was a problem reading the commands file.\n")
        sys.stdout.flush()
        sys.exit(1)
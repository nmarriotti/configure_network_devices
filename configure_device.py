from classes.ClassConstructor import Builder
from helpers.fileio import FileToList, FileToDict
from helpers.ports import IsPortOpen
import argparse
import sys
import socket, time

def applyconfig(device, commands):
    ''' Write each command to device '''
    sys.stdout.write("Configuring...\n")
    sys.stdout.flush()
    counter = 0
    for command in commands:
        counter += 1
        try:
            response = device.write(command, 0.2)
            if verbose:
                try:
                    sys.stdout.write(response.decode('utf-8') + '\n')
                    sys.stdout.flush()
                except:
                    sys.stdout.write(response[-2].decode('utf-8') + '\n')
                    sys.stdout.flush()
        except EOFError:
            sys.stdout.write("Error executing command #{0} ({1}). The connection is already closed.\n".format(counter, command))
            sys.stdout.flush()
            return
        except OSError:
            sys.stdout.write("Error executing command #{0} ({1}). The connection is already closed.\n".format(counter, command))
            sys.stdout.flush()
            return
    sys.stdout.write("Configuration complete.\n")
    sys.stdout.flush()
    device.disconnect()



def run(commands):
    ''' Login and configure each device '''
    for name, ipaddr in devices.items():
        
        # Returns the first available protocol
        protocol = IsPortOpen(ipaddr, ports=[22,23])

        # Exit if both SSH and Telnet are unavailable
        if not protocol:
            sys.stdout.write("No ports available, skipping device...\n")
            sys.stdout.flush()
            continue
		
        sys.stdout.write("\nConnecting to {0} via {1}\n".format(ipaddr, protocol.lower()))
        sys.stdout.flush()

        # Creates appropriate object based on protocol
        b = Builder()
        device = b.construct(protocol)(ipaddr)

        # Try connecting to the device
        connected = device.connect(auth=credentials, en_password=enable_password)

        if connected:
            sys.stdout.write("Connected!\n")
            sys.stdout.flush()
            # login was successful, execute commands
            applyconfig(device, commands)
        else:
            sys.stdout.write("Unable to connect. Check credentials and try again!\n")
            sys.stdout.flush()
       


if __name__ == "__main__":
    ''' Start here '''
    parser = argparse.ArgumentParser(description='''
    This script applies network device configurations from an external file
    ''')
    parser.add_argument("-u", "--username", required=True, help="Account username")
    parser.add_argument("-p", "--password", required=True, help="Account password")
    parser.add_argument("-e", "--enablepass", required=True, help="Enable password")
    parser.add_argument("-c", "--commands", required=True, help="File containing commands to execute")
    parser.add_argument("-v", "--verbose", required=False, action='store_true', help="sys.stdout.write device output to screen")
    args = parser.parse_args()

    # Return dictionary of devices to configure
    devices = FileToDict("devices.txt", "=")

    # Set global variables from command-line arguments
    credentials = (args.username, args.password)
    enable_password = args.enablepass

    # Set flag to trigger additional output
    verbose = args.verbose

    # Load the commands from file
    command_list = FileToList(args.commands)
	
    if command_list:
        # Connect/configure device
        run(command_list)
    else:
        sys.stdout.write("There was a problem reading the commands file.\n")
        sys.stdout.flush()
        sys.exit(1)

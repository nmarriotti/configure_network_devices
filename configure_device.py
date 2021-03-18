#from classes.protocols import Telnet, SSH
from classes.ClassConstructor import Builder
from helpers.fileio import FileToList, FileToDict
from helpers.ports import IsPortOpen
import argparse
import sys
import socket, time

<<<<<<< HEAD
# User-defined variables

def applyconfig(device, commands):
    ''' Write each command to device '''
    sys.stdout.write("\nConfiguring...\n")
    sys.stdout.flush()
    for command in commands:
        response = device.write(command, 0.2)
        if verbose:
            try:
                sys.stdout.write(response.decode('utf-8').replace("\x08","") + '\n')
            except:
                sys.stdout.write(response[-2].decode('utf-8').replace("\x08","") + '\n')
            sys.stdout.flush()
    sys.stdout.write("Configuration complete.\n")
    sys.stdout.flush()
=======
def applyconfig(device, commands):
    ''' Write each command to device '''
    print("Configuring...")
    counter = 0
    for command in commands:
        counter += 1
        try:
            response = device.write(command, 0.2)
            if verbose:
                try:
                    print(response.decode('utf-8'))
                except:
                    print(response[-2].decode('utf-8'))
        except EOFError as e:
            print("Error executing command #{0} ({1}). The connection is closed.".format(counter, command))
            return
        except OSError as e:
            print("Error executing command #{0} ({1}). The connection is closed.".format(counter, command))
            return
    print("Configuration complete.")
>>>>>>> addSSH
    device.disconnect()



def run(commands):
    ''' Login and configure each device '''
    EXIT_CODE = 0
    for name, ipaddr in devices.items():
        
        # Returns the first available protocol
<<<<<<< HEAD
        protocol = IsPortOpen(ipaddr, ports=[22, 23])
=======
        protocol = IsPortOpen(ipaddr, ports=[22,23])
>>>>>>> addSSH

        # Exit if both SSH and Telnet are unavailable
        if not protocol:
            sys.stderr.write("No ports available for {0}, skipping device...\n".format(ipaddr))
            sys.stderr.flush()
            EXIT_CODE = 1
            continue
		
<<<<<<< HEAD
        sys.stdout.flush()
=======
        print("\nConnecting to {0} via {1}".format(ipaddr, protocol.lower()))
>>>>>>> addSSH

        # Creates appropriate object based on protocol
        b = Builder()
        device = b.construct(protocol)(ipaddr)

        # Try connecting to the device
<<<<<<< HEAD
        sys.stdout.write("Connecting to {0} via {1}\n".format(ipaddr, protocol.upper()))
        sys.stdout.flush()
        connected = device.connect(auth=credentials, en_password=enable_password)

        if connected:
            sys.stdout.write("Connected\n")
            sys.stdout.flush()
            # login was successful, execute commands
            applyconfig(device, commands)
        else:
            sys.stderr.write("Unable to connect\n")
            sys.stderr.flush()
            EXIT_CODE = 1
	
    return EXIT_CODE
=======
        connected = device.connect(auth=credentials, en_password=enable_password)

        if connected:
            print("Connected!")
            # login was successful, execute commands
            applyconfig(device, commands)
        else:
            print("Unable to connect. Check credentials and try again!")
>>>>>>> addSSH
       


if __name__ == "__main__":
    ''' Start here '''
    parser = argparse.ArgumentParser(description='''
    This script applies network device configurations from an external file
    ''')
<<<<<<< HEAD
    parser.add_argument("--devices", required=True, help="File containing list of devices")
    parser.add_argument("--username", required=True, help="Account username")
    parser.add_argument("--password", required=True, help="Account password")
    parser.add_argument("--enablepass", required=True, help="Enable password")
    parser.add_argument("--commands", required=True, help="File containing commands to execute")
    parser.add_argument("--verbose", required=False, action='store_true', help="sys.stdout.write device output to screen")
=======
    parser.add_argument("-u", "--username", required=True, help="Account username")
    parser.add_argument("-p", "--password", required=True, help="Account password")
    parser.add_argument("-e", "--enablepass", required=True, help="Enable password")
    parser.add_argument("-c", "--commands", required=True, help="File containing commands to execute")
    parser.add_argument("-v", "--verbose", required=False, action='store_true', help="Print device output to screen")
>>>>>>> addSSH
    args = parser.parse_args()

    # Return dictionary of devices to configure
    devices = FileToDict("devices.txt", "=")

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
<<<<<<< HEAD
        sys.stdout.write("Automated Network Device Configuration\n")
        sys.stdout.write("======================================\n")
        sys.stdout.flush()
        exit_code = run(command_list)
        sys.exit(exit_code)
    else:
        sys.stderr.write("There was a problem reading the commands file.\n")
        sys.stderr.flush()
        sys.exit(1)
=======
        run(command_list)
    else:
        print("There was a problem reading the commands file.")
        sys.exit(1)
>>>>>>> addSSH

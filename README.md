# Configure Network Devices

This is a Python script to automate configurations of one or more network devices such as switches and routers.

### SSH vs Telnet

<<<<<<< HEAD
SSH takes precedence over Telnet, however in the event SSH is not configured then Telnet will be used.

### Devices (--devices)

This is a simple text file that contains IP address of the devices you wish to configure. Please use the following format when creating this file.
=======
SSH takes precedence over Telnet, however in the event SSH is not configured then Telnet will be used if the port is opened.

### Devices

Modify _devices.txt_ to add/remove devices. This file contains IP address of the devices you wish to configure. Please use the following format when creating this file.
>>>>>>> addSSH

```
Device1=192.168.1.1
switch=192.168.1.2
...
```

<<<<<<< HEAD
### Commands (--commands)

This is a simple text file containing the commands to execute. Each command should be entered on a separate line.

### Verbosity (--verbose)
=======
### Commands (-c, --commands)

This is a text file containing the commands to execute. Each command should be entered on a separate line.

### Verbosity (-v, --verbose)
>>>>>>> addSSH

Adding the optional _--verbose_ flag will display the standard output returned from the device as each command is executed

### How to Use

```
<<<<<<< HEAD
python configure_device.py --devices <path_to_devices_file> --username <device_username> --password <device_password> --enablepass <device_enablepass> --commands <path_to_commands_file>
```

=======
usage: configure_device.py [-h] -u USERNAME -p PASSWORD -e ENABLEPASS -c COMMANDS [-v]

This script applies network device configurations from an external file

arguments:
  -h,            --help                     show this help message and exit
  -u USERNAME,   --username USERNAME        Account username
  -p PASSWORD,   --password PASSWORD        Account password
  -e ENABLEPASS, --enablepass ENABLEPASS    Enable password
  -c COMMANDS,   --commands COMMANDS        File containing commands to execute
  -v,            --verbose                  Print device output to screen
```
>>>>>>> addSSH

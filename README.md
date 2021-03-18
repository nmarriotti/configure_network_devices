# Configure Network Devices

This is a Python script to automate configurations of one or more network devices such as switches and routers.

### SSH vs Telnet

SSH takes precedence over Telnet, however in the event SSH is not configured then Telnet will be used if the port is opened.

### Devices

Modify _devices.json_ to add/remove devices. This file contains IP address and credentials of the devices you wish to configure. An example is shown below.
```
{
    "devices": [
        {
            "name": "device1",
            "ip": "192.168.1.250",
            "username": "admin",
            "password": "admin",
            "enablepass": "secret"
        },
        {
            "name": "device2",
            "ip": "192.168.1.250",
            "username": "admin",
            "password": "admin",
            "enablepass": "secret"
        }
    ] 
}
```

### Commands (-c, --commands)

This is a text file containing the commands to execute. Each command should be entered on a separate line and stored in the _configs/_ directory.

### Verbosity (-v, --verbose)

Adding the optional _--verbose_ flag will display the standard output returned from the device as each command is executed

### How to Use

```
usage: configure_device.py [-h] -c COMMANDS [-v]

This script applies network device configurations from an external file

arguments:
  -h,            --help                     show this help message and exit
  -c COMMANDS,   --commands COMMANDS        File containing commands to execute
  -v,            --verbose                  Print device output to screen
```

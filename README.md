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

### Example
The below example connects to a device preconfigured for telnet and configures it to use SSH. The device is then configured again _(for demonstration purposes only)_ and uses SSH for the new connection.

```
$ python3 configure_device.py -c enablessh.txt -v

Connecting to 192.168.1.250 via telnet
providing username...
providing password...
Enable mode activated.
Connected!
Configuring...

config t
Enter configuration commands, one per line.  End with CNTL/Z.
switch1(config)#
line vty 0 15
switch1(config-line)#
transport input ssh
switch1(config-line)#
exit
switch1(config)#
exit
switch1#
exit

Configuration complete.

Connecting to 192.168.1.250 via ssh
Connected!
Configuring...
Enable mode activated.
switch1#en
Enter configuration commands, one per line.  End with CNTL/Z.
line vty 0 15
transport input ssh
exit
exit
exit
Configuration complete.
```

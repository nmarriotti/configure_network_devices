# Configure Network Devices

This is a Python script to automate configurations of one or more network devices such as switches and routers.

### SSH vs Telnet

SSH takes precedence over Telnet, however in the event SSH is not configured then Telnet will be used.

### Devices (--devices)

This is a simple text file that contains IP address of the devices you wish to configure. Please use the following format when creating this file.

```
Device1=192.168.1.1
switch=192.168.1.2
...
```

### Commands (--commands)

This is a simple text file containing the commands to execute. Each command should be entered on a separate line.

### How to Use

```
python configure_device.py --devices <path_to_devices_file> --username <device_username> --password <device_password> --enablepass <device_enablepass> --commands <path_to_commands_file>
```


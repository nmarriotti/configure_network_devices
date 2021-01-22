import telnetlib
import time
import datetime
import paramiko

class Telnet():
    def __init__(self, ipaddr, port=23):
        self.IPADDR = ipaddr
        self.PORT = port
        self.enable_mode = False
        self.enable_mode_requested = False
        self.enable_commands = ["en","enable"]
        self.AUTH = ()
        self.enablepassword = None
        self.PROTOCOL = "Telnet"


    def promptedForUsername(self, s):
        if "Username:" in s:
            return True
        return False
    

    def promptedForPassword(self, s):
        if "Password:" in s:
            return True
        return False


    ''' enable mode '''
    def activateEnableMode(self):
        self.enable_mode_requested = False
        data = self.tn.read_until(b"Password:",5)
        if b"Password:" in data:
            response = self.write(self.enablepassword, 1.0)
            if b"#" in response:
                print("Enable mode activated.")
                self.enable_mode = True
                return True
        return False


    ''' Send command '''
    def write(self, cmd, sleeptime=0.0):
        if cmd in self.enable_commands:
            self.tn.write(cmd.encode('ascii') + b"\n")
            time.sleep(sleeptime)
            if not self.activateEnableMode():
                raise Exception("Enable mode failed.")
        else:
            self.tn.write(cmd.encode('ascii') + b"\n")
            time.sleep(sleeptime)
        return self.tn.read_very_eager()
        

    ''' Login '''
    def connect(self, auth, en_password=None, timeout=10):
        self.AUTH = auth
        self.enablepassword = en_password

        # For some reason we need to sleep for a second or else the connection will fail
        time.sleep(1)

        print("\nConnecting to {0}:{1} as {2}...".format(self.IPADDR, self.PORT, auth[0]))
        try:
            # Connect
            self.tn = telnetlib.Telnet(self.IPADDR, self.PORT, timeout)
            
            time.sleep(2)
            data = self.tn.read_very_eager().decode('utf-8')

            # Check if username is required
            if self.promptedForUsername(data):
                self.tn.write(auth[0].encode('ascii') + b"\n")
                time.sleep(1.0)

            data = self.tn.read_until(b"Password:", 5).decode('utf-8')

            # Check if password is required
            if self.promptedForPassword(data):
                self.tn.write(auth[1].encode('ascii') + b"\n")
                time.sleep(1.0)

            # char '>' signifies successful login
            data = self.tn.read_until(b">", 20)
            print(data.decode('utf-8'))

            if not b">" in data:
                return False
            else:
                return True

        except Exception as e:
            print(str(e))
        return False


    ''' Close the telnet connection '''
    def disconnect(self):
        self.tn.close()




class SSH():
    AUTH = ()

    def __init__(self, ipaddr, port=22):
        self.IPADDR = ipaddr
        self.PORT = port
        self.enable_mode = False
        self.enable_mode_requested = False
        self.enable_commands = ["en","enable"]
        self.enablepassword = None
        self.PROTOCOL = "SSH"


    ''' Login '''
    def connect(self, auth, en_password=None, timeout=10):
        self.AUTH = auth
        self.enablepassword = en_password
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        # For some reason we need to sleep for a second or else the connection will fail
        #time.sleep(1)

        print("\nConnecting to {0}:{1} as {2}...".format(self.IPADDR, self.PORT, auth[0]))
        try:
            self.ssh.connect(self.IPADDR, self.PORT, username=r'{}'.format(self.AUTH[0]), password=r'{}'.format(self.AUTH[1]))
            self.shell = self.ssh.invoke_shell()
            self.connected = True
            return True
        except Exception as e:
            print(str(e))
        return False
    

    ''' Reads the command output '''
    def get_command_results(self):
        maxseconds = 3
        bufsize = 1024

        # Poll until completion or timeout
        # Note that we cannot directly use the stdout file descriptor
        # because it stalls at 64K bytes (65536).
        start = datetime.datetime.now()
        start_secs = time.mktime(start.timetuple())
        output = b''
        self.shell.setblocking(0)
        while True:
            if self.shell.recv_ready():
                data = self.shell.recv(bufsize)
                output += data

            if self.shell.exit_status_ready():
                break

            rbuffer = output.rstrip().split(b"\n")[-1]
            if len(rbuffer) > 0:
                if rbuffer[-1] == 35 or rbuffer[-1] == 62 or rbuffer[-1] == 58: ## got a Cisco command prompt
                    break
            
            time.sleep(0.1)

        if self.shell.recv_ready():
            data = self.shell.recv(bufsize)
            output += data
        
        # Get the last element in the last
        output = output.split(b"\n")

        return output


    ''' enable mode '''
    def activateEnableMode(self, output):
        self.enable_mode_requested = False
        if b"Password:" in output:
            output = self.write(self.enablepassword, 4.0)[-1]
            if b"#" in output:
                print("Enable mode activated.")
                self.enable_mode = True
                return True
        return False


    ''' Send command '''
    def write(self, cmd, sleeptime=0.0):
        self.shell.send(cmd + '\n')
        output = self.get_command_results()
        if cmd in self.enable_commands:
            if not self.activateEnableMode(output[-1]):
                raise Exception("Enable mode failed.")
        return output
        

    ''' Close the SSH connection '''
    def disconnect(self):
        self.ssh.close
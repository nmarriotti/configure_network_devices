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



    def activateEnableMode(self):
        ''' enable mode '''
        self.enable_mode_requested = False
        data = self.tn.read_until(b"Password:",5)
        if b"Password:" in data:
            response = self.write(self.enablepassword, 1.0)
            if b"#" in response:
                print("Enable mode activated.")
                self.enable_mode = True
                return True
        return False



    def write(self, cmd, sleeptime=0.0):
        ''' Send command '''
        if cmd in self.enable_commands:
            self.tn.write(cmd.encode('ascii') + b"\n")
            time.sleep(sleeptime)
            if not self.activateEnableMode():
                raise Exception("Enable mode failed.")
        else:
            self.tn.write(cmd.encode('ascii') + b"\n")
            time.sleep(sleeptime)
        return self.tn.read_very_eager()
        


    def connect(self, auth, en_password=None, timeout=15):
        ''' Login '''
        self.AUTH = auth
        self.enablepassword = en_password

        # Must wait a few seconds for previous socket remnants to be cleaned update
        time.sleep(3)
        
        try:
            # Connect
            self.tn = telnetlib.Telnet(self.IPADDR, self.PORT, timeout)
            
            data = self.tn.read_until(b"Username:",5).decode('utf-8')
			
            # Check if username is required
            if self.promptedForUsername(data):
                self.tn.write(auth[0].encode('ascii') + b"\n")
                time.sleep(2.0)

            data = self.tn.read_until(b"Password:", 5).decode('utf-8')
            # Check if password is required
            if self.promptedForPassword(data):
                self.tn.write(auth[1].encode('ascii') + b"\n")
                time.sleep(2.0)
            # char '>' signifies successful login
            data = self.tn.read_until(b">", 20)

            if not b">" in data:
                return False
            else:
                return True

        except Exception as e:
            print(str(e))
        return False



    def disconnect(self):
        ''' Close the telnet connection '''
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



    def connect(self, auth, en_password=None, timeout=10):
        ''' Login '''
        self.AUTH = auth
        self.enablepassword = en_password
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        try:
            self.ssh.connect(self.IPADDR, self.PORT, username=r'{}'.format(self.AUTH[0]), password=r'{}'.format(self.AUTH[1]))
            self.shell = self.ssh.invoke_shell()
            self.connected = True
            return True
        except Exception as e:
            print(str(e))
        return False
    


    def get_command_results(self):
        ''' Reads the command output '''
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



    def activateEnableMode(self, output):
        ''' enable mode '''
        self.enable_mode_requested = False
        if b"Password:" in output:
            output = self.write(self.enablepassword, 4.0)[-1]
            if b"#" in output:
                print("Enable mode activated.")
                self.enable_mode = True
                return True
        return False



    def write(self, cmd, sleeptime=0.0):
        ''' Send command '''
        self.shell.send(cmd + '\n')
        output = self.get_command_results()
        if cmd in self.enable_commands:
            if not self.activateEnableMode(output[-1]):
                raise Exception("Enable mode failed.")
        return output
        

    def disconnect(self):
        ''' Close the SSH connection '''
        self.ssh.close
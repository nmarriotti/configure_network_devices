import telnetlib
import time

class NetworkDevice():
    def __init__(self, ipaddr, port=23):
        self.IPADDR = ipaddr
        self.PORT = port
        self.enable_mode = False
        self.enable_mode_requested = False
        self.enable_commands = ["en","enable"]
        self.AUTH = ()
        self.enablepassword = None


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
            response = self.write(self.enablepassword, 4.0)
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

        print("Connecting to device as {0}...".format(auth[0]))
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
                time.sleep(4.0)

            # char '>' signifies successful login
            data = self.tn.read_until(b">", 20)
            print(data.decode('utf-8'))

            if not b">" in data:
                return False
            else:
                return True

        except Exception as e:
            return(str(e))
        return False


    ''' Close the telnet connection '''
    def disconnect(self):
        self.tn.close()
import socket
import time

protocols = {
    22: "SSH",
    23: "Telnet"
}

def IsPortOpen(ip, ports, timeout=3, delay=10, retry=5):
    retVal = False

    for port in ports:
        # Create a socket
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        
        # Attempt to establish a connection
        conn_status = s.connect_ex((ip, port))

        if conn_status == 0:
            retVal =  protocols[port]
            
    s.close()
    return retVal
import socket

protocols = {
    22: "SSH",
    23: "Telnet"
}

def IsPortOpen(ip, ports, timeout=3, delay=10, retry=5):
    # Create a socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(timeout)
    for port in ports:
        try:
            # Attempt to establish a connection
            s.connect((ip, port))
            s.shutdown(socket.SHUT_RDWR)
            # This port is open
            return protocols[port]
        except:
            # This port is closed
            pass
        finally:
            # Close the socket
            s.close()
    return False
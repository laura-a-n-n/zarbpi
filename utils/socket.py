import socket
import traceback

from config.main import settings

class Socket:
    def __init__(self, port=settings["socket_port"]):
        super()
        self.socket = socket.socket()
        self.socket.bind(("localhost", port))
        self.socket.listen()
        self.socket.settimeout(0)
    
    def read(self, verbose=False):
        try:
            self.connection, self.address = self.socket.accept()
        except:
            return False
        if verbose: print(f'Connected to {self.address}')

        try:
            data = self.connection.recv(1024).decode()
            self.connection.send(b'ACK')

            if verbose: print(f'Received message: {data}')
            return data
        except:
            traceback.print_exc()
            pass
        
        self.connection.close()
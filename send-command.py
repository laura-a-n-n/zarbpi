import sys
import socket
from config.main import settings

if __name__ == "__main__":
    command = sys.argv[1]
    client_socket = socket.socket()
    client_socket.connect(("localhost", settings["socket_port"]))
    client_socket.send(bytes(command, encoding="utf8"))
    client_socket.close()
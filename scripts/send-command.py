import sys
import socket

if __name__ == "__main__":
    command = sys.argv[1]
    client_socket = socket.socket()
    client_socket.connect(("localhost", 7777))
    client_socket.send(bytes(command, encoding="utf8"))
    client_socket.close()
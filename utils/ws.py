from websocket import create_connection
import subprocess

ws = create_connection("wss://zarbalatrax.com:777/")
ws.send("Hello, World")

while True:
    result =  ws.recv()
    print(f"Received {result}")
    if f"{result}" == "ZARBALATRAX, SPEAK YOU GREAT BEAST":
        subprocess.Popen(["python3", "/home/zarbalatrax/main/scripts/send-command.py", ".G"])

ws.close()

from websocket import WebSocketApp
import subprocess
import requests
from time import sleep

zocket_queue = []

def on_open(wsapp):
    print("open")
    wsapp.send("c2FyYmVsZXRyYWlzX2xlZ2VuZF9nb2RfNjY2ISEh")
    wsapp.send("zocket:zarbalatrax:hello")

def on_close(wsapp, code, reason):
    wsapp.send("zocket:zarbalatrax:goodbye")
    print(code, reason)
    print("close")
    sleep(10)
    start_webzocket()

def on_error(wsapp: WebSocketApp, e):
    wsapp.send("zocket:zarbalatrax:goodbye")
    print(e)
    wsapp.close()
    sleep(10)
    start_webzocket()

def on_message(wsapp, result):
    print(f"Received {result}")
    if f"{result}" == "zocket:client:request_presence":
        wsapp.send("zocket:zarbalatrax:hello")
    elif f"{result}" == "zocket:client:play":
        wsapp.send("zocket:zarbalatrax:I SHALL SPEAK")
        subprocess.Popen(["python3", "/home/zarbalatrax/main/scripts/send-command.py", ".G"])
    elif f"{result}".startswith("zocket:client:play:"):
        value = int(f"{result}".split("zocket:client:play:").pop())
        if isinstance(value, int):
            subprocess.Popen(["python3", "/home/zarbalatrax/main/scripts/send-command.py", f";Q,{value}"])
            sleep(0.5)
            subprocess.Popen(["python3", "/home/zarbalatrax/main/scripts/send-command.py", ".G"])
    elif f"{result}".startswith("zocket:client:print:"):
        value = int(f"{result}".split("zocket:client:print:").pop())
        if isinstance(value, int):
            subprocess.Popen(["python3", "/home/zarbalatrax/main/scripts/send-command.py", f";X,{value}"])
    elif f"{result}" == "zocket:client:fetch":
        url = 'https://zarbalatrax.com:666/static/upload.png'
        output_path = 'output.png'
        username = 'sarb'
        password = 'Squambo666'

        # Fetching the image with authentication
        response = requests.get(url, auth=(username, password))

        # Check if the request was successful
        if response.status_code == 200:
            with open(output_path, 'wb') as f:
                f.write(response.content)
            print(f"Image saved to {output_path}")
        else:
            print(f"Failed to download image. Status code: {response.status_code}")


def start_webzocket():
    wsapp = WebSocketApp("wss://zarbalatrax.com:777/", on_open=on_open, on_close=on_close, on_message=on_message, on_error=on_error)
    wsapp.run_forever()

if __name__ == "__main__":
    start_webzocket()

from websocket import WebSocketApp
import subprocess
import requests
from time import sleep
from PIL import Image

import threading

class ThreadSafeDict:
    def __init__(self):
        self._dict = {}
        self._lock = threading.Lock()

    def get(self, key, default=None):
        with self._lock:
            return self._dict.get(key, default)

    def set(self, key, value):
        with self._lock:
            self._dict[key] = value

    def get_and_set(self, key, new_value):
        """Atomically reads and sets a value"""
        with self._lock:
            old_value = self._dict.get(key)
            self._dict[key] = new_value
            return old_value

    def update(self, key, update_fn):
        """Atomically updates a value using update_fn(old_value) -> new_value"""
        with self._lock:
            old_value = self._dict.get(key)
            new_value = update_fn(old_value)
            self._dict[key] = new_value
            return new_value

zocket_queue = []

def on_open(wsapp):
    print("open")
    with open(".zarbsecret", "r") as f:
        wsapp.send(f.read())
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


state = ThreadSafeDict()
state.set("upload_in_progress", False)

def on_message(wsapp, result):
    global state

    if f"{result}".startswith("zocket:sarbeletrais:code:"):
        print("sarb requested write to ZarbData.h")
        if state.get_and_set("upload_in_progress", True):
            print("upload is already in progress")
            return
        try:
            with open("/home/zarbalatrax/zarbalatrax-3/zarbalatrax/ZarbData.h", "w") as f:
                f.write(f"{result}".split("zocket:sarbeletrais:code:").pop())
        except e:
            print(e)
        subprocess.call(["/home/zarbalatrax/upload-script.sh"], cwd="/home/zarbalatrax")
        state.set("upload_in_progress", False)
        return

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
    elif f"{result}".startswith("zocket:client:queue:"):
        value = int(f"{result}".split("zocket:client:queue:").pop())
        if isinstance(value, int):
            subprocess.Popen(["python3", "/home/zarbalatrax/main/scripts/send-command.py", f";Q,{value}"])
    elif f"{result}".startswith("zocket:client:print:"):
        value = int(f"{result}".split("zocket:client:print:").pop())
        if isinstance(value, int):
            subprocess.Popen(["python3", "/home/zarbalatrax/main/scripts/send-command.py", f";X,{value}"])
    elif f"{result}" == "zocket:client:fetch":
        url = 'https://zarbalatrax.com/sarbeletrais/content/upload.png'
        output_path = 'images/upload.png'
        username = 'squambo'
        password = 'SquamboLegend666'

        # Fetching the image with authentication
        response = requests.get(url, auth=(username, password))

        print(response.headers)
        # Check if the request was successful
        if response.status_code == 200:
            with open(output_path, 'wb') as f:
                f.write(response.content)
            print(f"Image saved to {output_path}")

            image = Image.open(output_path)
            image.thumbnail((512, 512))
            image.save(output_path)
            print(f"Image resized to {image.size}")
            subprocess.Popen(["python3", "/home/zarbalatrax/main/scripts/send-command.py", f";X,0"])
        else:
            print(f"Failed to download image. Status code: {response.status_code}")


def start_webzocket():
    wsapp = WebSocketApp("wss://zarbalatrax.com:777/", on_open=on_open, on_close=on_close, on_message=on_message, on_error=on_error)
    wsapp.run_forever()

if __name__ == "__main__":
    start_webzocket()

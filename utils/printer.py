import os
import time

from escpos import *
from config.main import settings

class Printer:
    def __init__(self):
        super()

        self.printer = False
        
        while not self.printer:
            try:
                self.printer = self._connect()
            except:
                print("Waiting for printer...")
                time.sleep(5)
    
    def _connect(self, width=512):
        connection = printer.Serial(settings["port"], baudrate=settings["baudrate"], profile=settings["profile"])
        if width > 0:
            connection.profile.profile_data["media"]["width"]["pixels"] = width
        return connection
    
    def initialize(self):
        self.printer = self.printer or self._connect()
        print("Printer: ", printer)
        return self.printer
    
    def cut(self):
        self.initialize().cut()

    def image(self, path: str, bottom_margin = 2):
        printer = self.initialize()
        printer.image(img_source=path, impl=settings["printer_implementation"], center=True)
        
        if bottom_margin:
            for _ in range(bottom_margin): printer.control("LF")
    
    def test_print(self):
        printer = self.initialize()

        printer.text(settings["test_text"])
        self.image(settings["test_print_image"])

        printer.cut()

    def decode_response(self, input: str, ext = "png"):
        string = input

        if input.isnumeric():
            string = f"{input:0>3}"
        else:
            string = string.lower()

        path = f"{settings['images_path']}/{string}.{ext}"

        if os.path.exists(path):
            return path
        else:
            print(f"Specified path {path} does not exist.")
            return False
    
    def get_code_from_id(self, input: str):
        i = 0
        k = int(input)
        while k >= settings["file_ids"][i+1] and i < len(settings["file_ids"]) - 1:
            i += 1

        return settings["file_names"][i]


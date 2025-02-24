import time
import serial
import traceback
import threading

from config.main import settings
from utils.printer import Printer
from utils.audio import Audio
from utils.zocket import Socket
from utils.decider import decide
from utils.gmail import poll_for_emails

play_button_activated = False
venmo_thread = threading.Thread(target=poll_for_emails)
venmo_thread.start()

def main():
    global play_button_activated
    # wait for input buffer to be nonzero
    answer = False
    while not answer and arduino.in_waiting == 0: 
        socket_response = socket.read()
        if socket_response:
            arduino.write(socket_response.encode())
            answer = socket_response

    # read answer
    if not answer:
        answer = arduino.readline().decode("utf-8").strip()
    print("Received:", answer)
    if not (answer and answer.startswith(settings["command_prefix"])):
        print("(Not a command.)")
        return
        
    answer = answer[1:] # trim .

    split = answer.split(",")

    if split[0][0] == settings["audio_keyword"]:
        print("Audio command detected!")
        print(audio.music_playing, audio.current_song, audio.sounds)
        try:
            channel = audio.play(f"{split[1]:0>3}")
            if settings["playback_needs_delay"](int(split[1])) or not play_button_activated:
                while channel.get_busy():
                    time.sleep(0.05) # wait for idle animation to finish before doing anything else
                if settings["playback_is_idle"](int(split[1])) or not play_button_activated: audio.music(should_play=False)
        except Exception:
            traceback.print_exc()
            print("Was not able to play that file!")
            pass
    elif split[0][0] == settings["begin_keyword"]:
        decision = decide("intro")
        arduino.write(str(decision).encode())
    elif split[0][0] == settings["play_keyword"]:
        decision = decide("play")
        play_button_activated = True
        arduino.write(str(decision).encode())
        if decision <= settings["num_fortunes"]: # if is a fortune
            audio.play("097")
    elif split[0][0] == settings["stop_keyword"]:
        audio.music(should_play=False)
    elif split[0][0] == settings["idle_keyword"]:
        decision = decide("idle")
        arduino.write(str(decision).encode())
    elif split[0][0] == settings["print_keyword"]:
        decoded = settings["decodings"][printer.get_code_from_id(split[1])]
        decoded = decoded.copy()
        decoded.append(decoded[-1])
        decoded[-2] = split[1]

        for string in decoded:
            image_name = printer.decode_response(string)

            print(f"---> {string}")
            print(f"Decoded: {image_name}")

            if image_name:
                printer.image(image_name)
            else:
                print("(Not an image file.)")
        
        printer.cut()

        audio.music(should_play=False)
        play_button_activated = False

if __name__ == "__main__":
    print("Running. Preparing to speak...")

    printer = Printer()
    audio = Audio()
    socket = Socket()
    
    with serial.Serial(settings["arduino_port"], settings["arduino_baudrate"], timeout=1.0) as arduino:
        time.sleep(0.1) # wait for serial to open

        if arduino.isOpen():
            print("{} connected!".format(arduino.port))

            try:
                while True:
                    main()
            except KeyboardInterrupt:
                print("KeyboardInterrupt has been caught.")
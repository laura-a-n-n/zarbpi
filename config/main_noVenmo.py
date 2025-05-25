VERSION = 0.5

settings = dict(
    port = "/dev/ttyUSB0",
    baudrate = 38400,
    profile="TM-T88III",
    printer_implementation = "bitImageColumn",

    arduino_port = "/dev/ttyACM0",
    arduino_baudrate = 38400,

    images_path = "/home/zarbalatrax/main/images",
    sounds_path = "/home/zarbalatrax/main/sounds",
    test_text = f"ZarbOS v{VERSION}",
    test_print_image = "006.png",

    command_prefix = ".",
    audio_keyword = "A",
    play_keyword = "P",
    idle_keyword = "I",
    begin_keyword = "B",
    stop_keyword = "S",
    print_keyword = "X",
    decodings = dict(
        CF = ["HEADER", "F_COM", "FOOT_CF"], # common fortune
        CS = ["HEADER", "S_COM", "FOOT_CS"], # common story
        RF = ["HEADER", "F_RARE", "FOOT_RF"], # rare fortune
        RS = ["HEADER", "S_RARE", "FOOT_RS"], # rare story
        GM = ["HEADER", "GODMODE", "FOOT_GM"], # god mode
        S = ["HEADER", "SOUND", "FOOT_S"], # sound design
        AP = "play",
        AS = "stop",
        I = "idle",
        P = "activate",
        B = "begin"
    ),

    # categories = 
    # ['common fortune', 'rare fortune', 'common story', 'rare story', 'sound design', 'idle', ' intro', 'in a past life', ' he man', 'bg music']
    file_names = ["CF", "RF", "CS", "RS", "S", None, None, None, "GM"],
    file_ids = [1, 14, 31, 44, 60, 71, 84, 97, 100, 101],
    playback_needs_delay = lambda id : id >= 71 and id < 97,
    playback_is_idle = lambda id : id >= 71 and id < 84,
    bg_music_start = 101,
    num_bg_music = 3,
    fade_time = 1000,
    num_fortunes = 30,

    # socket settings
    socket_port = 7777,
)
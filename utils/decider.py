import random
import os.path
from config.main import settings

def create_idle():
    return list(range(71, 84))

def create_intro():
    return list(range(84, 95))

def create_play():
    return list(range(1, 71)) + [100]

banks = dict(
    idle = create_idle(),
    intro = create_intro(),
    play = create_play()
)

exclude_filter = [23, 63, 100]

def decide(mode):
    id = 0
    in_bank = False
    excluded = False
    while not os.path.isfile(f"{settings['sounds_path']}/{id:0>3}.wav") or in_bank == False or excluded:
        if mode == "idle": 
            if len(banks["idle"]) == 0: banks["idle"] = create_idle()

            id = banks["idle"][random.randint(0, len(banks["idle"]) - 1)]
            in_bank = id in banks["idle"] and "idle" or False
        elif mode == "intro":
            if len(banks["intro"]) == 0: banks["intro"] = create_intro()

            id = banks["intro"][random.randint(0, len(banks["intro"]) - 1)]
            in_bank = id in banks["intro"] and "intro" or False
        elif mode == "play":
            if len(banks["play"]) == 0: banks["play"] = create_play()

            if random.randint(1, 100) == 1:
                id = 100
            else:
                id = banks["play"][random.randint(0, len(banks["play"]) - 1)]
            in_bank = id in banks["play"] and "play" or False
        excluded = id in exclude_filter
    banks[in_bank].pop(banks[in_bank].index(id))

    return id
    

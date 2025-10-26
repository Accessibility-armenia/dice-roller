import pygame
import random
import json
import os
import winsound
from accessible_output2.outputs.auto import Auto

pygame.init()
pygame.display.set_caption("Dice Roller 1.2")
screen = pygame.display.set_mode((1920, 1080))
clock = pygame.time.Clock()

# === Озвучка ===
speaker = Auto()

# === Звуки ===
throw_sound = pygame.mixer.Sound("brosokzara.ogg")
pygame.mixer.music.load("o.mp3")

# === Настройки ===
CONFIG_FILE = "config.txt"
dice_count = 1
music_enabled = True
volume = 15
language = "arm"
throw_enabled = True  # звук зары включён по умолчанию

def save_settings():
    data = {
        "dice_count": dice_count,
        "music_enabled": music_enabled,
        "volume": volume,
        "language": language,
        "throw_enabled": throw_enabled
    }
    with open(CONFIG_FILE, "w") as f:
        json.dump(data, f)

def load_settings():
    global dice_count, music_enabled, volume, language, throw_enabled
    try:
        with open(CONFIG_FILE, "r") as f:
            data = json.load(f)
            dice_count = data.get("dice_count", 1)
            music_enabled = data.get("music_enabled", True)
            volume = data.get("volume", 15)
            language = data.get("language", "arm")
            throw_enabled = data.get("throw_enabled", True)
    except (FileNotFoundError, json.JSONDecodeError):
        save_settings()

if not os.path.exists(CONFIG_FILE):
    save_settings()

load_settings()
pygame.mixer.music.set_volume(volume / 100)
throw_sound.set_volume(volume / 100)

if music_enabled and volume > 0:
    pygame.mixer.music.play(-1)

# === Инструкция ===
def get_instructions():
    if language == "arm":
        return (
            "Բարի գալուստ Զառի Գցում 1.2։ "
            "Սեղմեք Space՝ զառը գցելու համար։ "
            "Սեղմեք Tab՝ մեկ կամ երկու զառ ընտրելու համար։ "
            "Սեղմեք Enter՝ երաժշտությունը միացնելու կամ անջատելու համար։ "
            "Սեղմեք ԱՅՈՎ սլաքը՝ ձայնը մեծացնելու համար 5 տոկոսով։ "
            "Սեղմեք ՆԵՐՔԵՎ սլաքը՝ ձայնը փոքրացնելու համար 5 տոկոսով։ "
            "Սեղմեք Control և F3՝ երաժշտությունը մեծացնելու համար 1 տոկոսով։ "
            "Սեղմեք Shift և F3՝ երաժշտությունը փոքրացնելու համար 1 տոկոսով։ "
            "Սեղմեք S՝ զառի ձայնը միացնելու կամ անջատելու համար։ "
            "Սեղմեք L՝ փոխելու լեզուն։ "
            "Սեղմեք C՝ պատճենելու տեղեկատվությունը ծրագրի մասին։ "
            "Սեղմեք I՝ լսելու այս տեղեկատվությունը կրկին։ "
            "Սեղմեք F3՝ վերականգնելու բոլոր կարգավորումները։ "
            "Սեղմեք Escape՝ դուրս գալու համար։"
        )
    else:
        return (
            "Welcome to Dice Roller 1.2! "
            "Press Space to roll the dice. "
            "Press Tab to switch between one or two dice. "
            "Press Enter to toggle music. "
            "Press Up Arrow to increase volume by 5 percent. "
            "Press Down Arrow to decrease volume by 5 percent. "
            "Press Control and F3 to increase music volume by 1 percent. "
            "Press Shift and F3 to decrease music volume by 1 percent. "
            "Press S to toggle dice sound. "
            "Press L to change language. "
            "Press C to copy game information. "
            "Press I to hear this information again. "
            "Press F3 to reset all settings. "
            "Press Escape to exit."
        )

speaker.speak(get_instructions())

def wait_for_sound(sound):
    while sound.get_num_channels() > 0:
        pygame.time.wait(50)

def roll_dice():
    if not throw_enabled:
        speaker.speak("Ձայնը անջատված է" if language == "arm" else "Dice sound disabled")
        return
    if dice_count == 1:
        throw_sound.play()
        wait_for_sound(throw_sound)
        n = random.randint(1, 6)
        speaker.speak(str(n))
    else:
        for _ in range(2):
            throw_sound.play()
            wait_for_sound(throw_sound)
        n1 = random.randint(1, 6)
        n2 = random.randint(1, 6)
        speaker.speak(f"{n1}, {n2}")
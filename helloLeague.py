from pynput import keyboard
import requests
import time

import configParser
import teamHandler

VALID_KEYS = []
VALID_MODIFIERS = []
curPresses = set()

isWriting = False
teamEnums = {}

enumz = {
    'tab': keyboard.Key.tab,
    'caps_lock': keyboard.Key.caps_lock,
    'shift_l': keyboard.Key.shift_l,
    'ctrl_l': keyboard.Key.ctrl_l,
    'alt_l': keyboard.Key.alt_l
}

def loadKeysAndMods():
    global VALID_KEYS
    global VALID_MODIFIERS
    VALID_KEYS_temp, VALID_MODIFIERS_temp = configParser.verifyJsonIntegrity()
    VALID_KEYS = [keyboard.KeyCode.from_char(str(x)) for x in VALID_KEYS_temp]
    VALID_MODIFIERS = [enumz[VALID_MODIFIERS_temp[0]]]


def on_press(key:keyboard.KeyCode):
    global curPresses
    global isWriting

    print(key)
    if isWriting:
        return

    if key in VALID_MODIFIERS or key in VALID_KEYS:
        curPresses.add(key)

    if key in VALID_KEYS and curPresses.intersection(VALID_MODIFIERS):
        try:
            print(curPresses)
            isWriting = True
            teamClass.autoGUISending(int(key.char)-1)
            curPresses.remove(key)
            isWriting = False
        except KeyError as e:
            print(e)

def on_release(key):
    global curPresses
    try:
        curPresses.remove(key)
    except KeyError as e:
        print(e)

teamClass = None

def main():
    global teamEnums
    global teamClass

    loadKeysAndMods()

    while True:
        try:
            requests.get('https://127.0.0.1:2999/liveclientdata/playerlist', verify=False)
            print('Game detected! Initialising . . .')
            break
        except requests.exceptions.RequestException:
            print("Try launching a game first!")
            print("Waiting for game to start . . .")
            time.sleep(5)
    
    while True:
        try:
            teamClass = teamHandler.TeamHandler()
            break
        except:
            print("The game appears to be launched, but loading! Waiting . . .")
            time.sleep(3)

    print('Initialisation complete! Ready to go!')
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

if __name__ == '__main__':
    main()

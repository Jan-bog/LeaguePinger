import os
import json

from pynput import keyboard

cwd = os.path.dirname(os.path.realpath(__file__))

def createConfig():
    VALID_KEYS = ['1', '2', '3', '4', '5']
    VALID_MODIFIERS = 'caps_lock'
    dictie = {
        'VALID_KEYS': VALID_KEYS,
        'VALID_MODIFIERS': VALID_MODIFIERS}
    try:
        os.mkdir('data')
    except FileExistsError:
        pass
    with open(os.path.join('data', 'config.txt'), 'w+', encoding='utf-8') as f:
        f.write(f'VALID_KEYS: {VALID_KEYS}\n')
        f.write(f'VALID_MODIFIERS: {VALID_MODIFIERS}\n')
        f.write("""\n# Valid keys are ones to use for champions. 1 will usually be the toplaner, 2 the jungler, 3 the mid, etc
# Valid modifiers is the key that needs to be held down to activate
# Values like F1, F2, F3, F4, F5 should work as well
# Valid modifiers are caps_lock, tab, shift_l, ctrl_l, alt_l, etc
# If in doubt, consult the documentation for pynput.keyboard
# If parsing fails, this file will be remade for you""")
    return VALID_KEYS, [VALID_MODIFIERS]

def parseConfig():
    VALID_KEYS = []
    VALID_MODIFIERS = []
    with open(os.path.join('data', 'config.txt'), 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines:
            if line.startswith('VALID_KEYS'):
                VALID_KEYS = [x for x in line.split(': ')[1][1:-2].strip().replace("'", '').replace(",", '').split(' ')]
            elif line.startswith('VALID_MODIFIERS'):
                VALID_MODIFIERS.append(line.split(': ')[1].strip())
    return VALID_KEYS, VALID_MODIFIERS

def verifyJsonIntegrity():
    try:
        return parseConfig()
    except:
        print("config.txt is corrupted. Destroying and creating a new one . . .")
        config = createConfig()
        print(f'Config file created in /data/config.txt')
        return config
    
def main():
    b = createConfig()
    a = parseConfig()
    assert a == b
    verifyJsonIntegrity()

if __name__ == '__main__':
    main()
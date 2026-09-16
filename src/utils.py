import sys
import os
import subprocess

def ansicolors():
    if sys.platform == "win32":
        import ctypes
        kernel32 = ctypes.windll.kernel32
        kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)

    return {
        "RED": "\033[91m",
        "PINK": "\033[38;5;218m",
        "GREEN": "\033[92m",
        "YELLOW": "\033[93m",
        "BLUE": "\033[94m",
        "PURPLE": "\033[38;5;141m",
        "TURQUOISE": "\033[38;5;158m",
        "CYAN": "\033[38;5;123m",

        "DEFAULT": "\033[0m"
    }

colors = ansicolors()

def printcl(color, text):
    print(f'{colors[color]}{text}{colors['DEFAULT']}')

def printcl_concat(*words: tuple[str, str]):
    colored_str = ""

    for word in words:
        colored_str += f'{colors[word[0]]}{word[1]}{colors['DEFAULT']}'  

    print(colored_str)
    
def cs_clear():
    subprocess.run("cls" if os.name == "nt" else "clear", shell=True)
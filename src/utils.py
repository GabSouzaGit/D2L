import sys
import os
import subprocess

def ansicolors():
    if sys.platform == "win32":
        import ctypes
        kernel32 = ctypes.windll.kernel32
        kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)

    return {
        "RED":      "\033[91m",
        "GREEN":    "\033[92m",
        "YELLOW":   "\033[93m",
        "BLUE":     "\033[0;38;2;153;175;255;49m",
        "PINK":     "\033[0;38;2;255;153;189;49m",
        "PURPLE":   "\033[0;38;2;225;117;255;49m",
        "CYAN":     "\033[0;38;2;0;255;145;49m",

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
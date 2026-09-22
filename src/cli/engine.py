from utils import ansicolors
from time import sleep
from utils import colors
import json
import re

from cli.especial_flags import wait_template, pause_template
from cli.especial_callers import wait_caller, pause_caller

colors = ansicolors()

colours_by_ch = {
    'DIANA': 'PINK',
    'DENA': 'PURPLE',
    'LACEY': 'CYAN'
}

templates = [
    {
        "type": "narrator",
        "color": colors['DEFAULT'],
        "text": "",
        "default-speed": 0.025,
    },
    {
        "type": "dialog",
        "name": "",
        "color": "",
        "text": "",
        "default-speed": 0.03,
    },
    {
        "type": "wait",
        "time": 0,
    },
    {
        "type": "pause",
        "message": ""
    }
]

template_by_flag = {
    "NARRATOR":       templates[0],
    "DIANA":          templates[1],
    "DENA":           templates[1],
    "LACEY":          templates[1],
    "UNDEF_DIALOG":   templates[1],

    # Flags especiais
    "WAIT":           templates[2],
    "PAUSE":          templates[3]
}

def narrator_formatter(msg_dict : dict):
    return f'~ "{msg_dict['text']}"'

def dialog_formatter(msg_dict : dict):
    return f'{msg_dict['name']}:\n{msg_dict['color']}{msg_dict['text']}{colors['DEFAULT']}'

def get_params(line : str):
    splitted_sentence  = line.split("=")
    key = splitted_sentence[0]

    params = False
    if len(splitted_sentence) > 1: 
        params = json.loads(splitted_sentence[1])

    return [ params, key ]

def treat_especial_flags(line):
    actions = {
        "WAIT": wait_template,
        "PAUSE": pause_template
    }

    params, key = get_params(line)

    if key not in actions: return [ False, params, key ]

    act = actions[key](template_by_flag[key], params)

    return [ act, params, key ]

def treat_citations(line : str, color : str):
    cit_start = r'citation\("'
    cit_end = r'"\)'

    has_citation = re.search(cit_start, line, flags=re.IGNORECASE)

    if has_citation:

        line = line.removesuffix('")')
        line = re.sub(cit_start, f'{colors["DEFAULT"]} - ', line)

        return re.sub(cit_end, f' - {color}', line)

    return line

textfmt_by_type = {
    'narrator': narrator_formatter,
    'dialog': dialog_formatter
}

# Faz a analise das flags (@) e transforma o texto numa estrutura de dados.
def story_parser(filepath):
    story_struct = []

    with open(filepath, "r") as file:
        current_template = None

        has_params = False
        building_block = False

        # Lê linha por linha:
        for line in (line.strip() for line in file):
            if(line == "" and building_block == False): continue

            # É uma flag
            if line == "":
                current_template['text'] += '\n'
            if line.startswith("@"):
                flag_line = line.removeprefix("@")

                if flag_line == "END":
                    current_template['text'] = current_template['text'].rstrip()

                    story_struct.append(current_template.copy())

                    building_block = False
                    has_params = False

                    current_template = None

                    continue

                action, params, key = treat_especial_flags(flag_line)

                if action:
                    story_struct.append(action)
                    continue

                current_template = template_by_flag[key if key in template_by_flag else "UNDEF_DIALOG"].copy()

                if params:
                    current_template["default-speed"] = params.get(
                        "speed",
                        current_template["default-speed"]
                    )

                    current_template["color"] = colors[
                        params["color"] if "color" in params else (colours_by_ch[key] if key in colours_by_ch else 'DEFAULT')
                    ]

                    has_params = True

                if key == "NARRATOR":
                    building_block = True
                    continue
                else:
                    building_block = True
                    current_template["name"] = key.capitalize()

                    if not has_params:   
                        current_template["color"] = colors[colours_by_ch[key]]
            else:
                if building_block:
                    line = treat_citations(line, current_template["color"])
                    current_template['text'] += f'{line}\n'
                    
    return story_struct

def print_animation(time, text):
    for letter in text:
        print(letter, end="", flush=True)
        sleep(time)

def story_processor(story_struct):
    especial_callers = {
        "wait": wait_caller,
        "pause": pause_caller
    }

    for story_part in story_struct:
        caller_prop = None

        if story_part["type"] == "narrator" or story_part["type"] == "dialog":
            text_formatted = textfmt_by_type[story_part['type']](story_part)

            def caller():
                print_animation(
                    story_part['default-speed'], 
                    text_formatted
                )

            caller_prop = caller
        else:
            def esp_caller():
                especial_callers[story_part["type"]](story_part["value"])
                
            caller_prop = esp_caller

        yield {
            "type": story_part["type"],
            "call": caller_prop
        }
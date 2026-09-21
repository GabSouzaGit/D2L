from utils import ansicolors
from time import sleep
from utils import colors
import json

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
    }
]

def narrator_formatter(msg_dict : dict):
    return f'~ "{msg_dict['text']}"'

def dialog_formatter(msg_dict : dict):
    return f'{msg_dict['name']}:\n{msg_dict['color']}{msg_dict['text']}{colors['DEFAULT']}'

textfmt_by_type = {
    'narrator': narrator_formatter,
    'dialog': dialog_formatter
}

# Faz a analise das flags (@) e transforma o texto numa estrutura de dados.
def story_parser(filepath):
    typeof_text = {
        "NARRATOR":       templates[0],
        "DIANA":          templates[1],
        "DENA":           templates[1],
        "LACEY":          templates[1],
        "UNDEF_DIALOG":   templates[1]
    }
    
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

                splitted_sentence  = flag_line.split("=")
                key = splitted_sentence[0]

                params = False
                if len(splitted_sentence) > 1: 
                    params = json.loads(splitted_sentence[1])

                current_template = typeof_text[key if key in typeof_text else "UNDEF_DIALOG"].copy()

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
                    splitted_line = line.split("-")
                    if len(splitted_line) > 1:
                        #print(splitted_line)
                        #input()

                        ch_speak, inline_narrator = splitted_line
                        current_template['text'] += f'{ch_speak}{colors['DEFAULT']}-{inline_narrator}\n'
                        continue

                    current_template['text'] += f'{line}\n'
                    
    return story_struct

def print_animation(time, text):
    for letter in text:
        print(letter, end="", flush=True)
        sleep(time)

def story_processor(story_struct):
    for story_part in story_struct:
        text_formatted = textfmt_by_type[story_part['type']](story_part)

        def caller():
            print_animation(
                story_part['default-speed'], 
                text_formatted
            )

        yield {
            "call": caller
        }
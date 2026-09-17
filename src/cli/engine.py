from utils import ansicolors
from time import sleep
from utils import colors

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
def story_interpreter(filepath):
    typeof_text = {
        "NARRATOR": templates[0],
        "DIANA":    templates[1],
        "DENA":     templates[1],
        "LACEY":    templates[1]
    }
    
    story_struct = []

    with open(filepath, "r") as file:
        current_template = None
        building_block = False

        for line in (line.strip() for line in file):
            if(line == ""): continue

            if line.startswith("@"):
                key = line.removeprefix("@")

                if key == "END":
                    current_template['text'] = current_template['text'].rstrip()

                    story_struct.append(current_template.copy())

                    building_block = False
                    current_template = None

                    continue
                
                current_template = typeof_text[key].copy()

                if key == "NARRATOR":
                    building_block = True
                    continue
                else:
                    building_block = True

                    current_template["name"] = key.capitalize()
                    current_template["color"] = colors[colours_by_ch[key]]
            else:
                if building_block:
                    current_template['text'] += line + "\n"
                    
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
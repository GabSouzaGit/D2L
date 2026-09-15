from utils import ansicolors
from pprint import pprint

colors = ansicolors()

templates = [
    {
        "type": "narrator",
        "color": colors['DEFAULT'],
        "text": "",
        "default-speed": 0.018,
    },
    {
        "type": "dialog",
        "name": "",
        "color": "",
        "text": "",
        "default-speed": 0.025,
    }
]

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
                    current_template["color"] = colors[key]
            else:
                if building_block:
                    current_template['text'] += line + "\n"
                    
    return story_struct
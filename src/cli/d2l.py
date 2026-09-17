from interactive.engine import story_interpreter
from utils import cs_clear, printcl
from pathlib import Path
from pprint import pprint

def greet():
    print('╔══════════════════════════════════════╗')
    print('║       D²L — O ARQUIVO DIGITAL        ║')
    print('╚══════════════════════════════════════╝')
    print('\n')
    printcl('BLUE', 'Seja bem vindo ao sistema CLI do "D²L - As aventuras de Diana, Dena e Lacey"!')
    printcl('PINK', 'Acesse as temporadas abaixo e leia as histórias dessas 3 meninas.')
    print('\n')

    seasons = Path("./stories/")
    season_paths = []

    for index, season in enumerate(seasons.iterdir(), start=1):
        print(
            f'{index} - {index}ª TEMPORADA',
        )

        season_paths.append(Path(season))

    printcl('RED', '0. SAIR')

    return season_paths

while 1:
    season_paths = greet()
    season_selected = input()

    if(season_selected == "0"): exit()
    
    if season_selected.isdigit():
        season_index = int(season_selected) - 1

        if season_index < len(season_paths):
            season = season_paths[season_index]
            example = season/"example.txt" #mudar para usuário escolher historia

            # while 1: (fazer novo loop para esperar qual historia será aberta)

            story_struct = story_interpreter(example)
            pprint(story_struct)

            input()

    cs_clear()
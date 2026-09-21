from cli.engine import story_parser, story_processor
from utils import cs_clear, printcl
from pathlib import Path
from pprint import pprint
import os

def ascii_art():
    print('\n')
    print('                 ██████ ╗░██████╗░██╗░░░░░')
    print('                 ██╔══██ ╗╚════██╗██║░░░░░')
    print('                 ██║░░██ ║░░███╔═╝██║░░░░░')
    print('                 ██║░░██ ║██╔══╝░░██║░░░░░')
    print('                 ██████ ╔╝███████╗███████╗')
    print('                  ╚═════╝░╚══════╝╚══════╝')
    print('\n')

def greet():
    print('╔══════════════════════════════════════════════════════════╗')
    print('║       "D²L — As Aventuras de Diana, Dena e Lacey"        ║')
    print('║                   O Arquivo digital                      ║')
    print('╚══════════════════════════════════════════════════════════╝')
    print('\n')
    printcl('BLUE', 'Seja bem vindo ao sistema CLI do "D²L - As aventuras de Diana, Dena e Lacey"!')
    printcl('PINK', 'Acesse as temporadas abaixo e leia as histórias dessas 3 meninas.')
    print('\n')

    BASE_PATH = Path(__file__).resolve().parent

    seasons = BASE_PATH / "stories"
    season_paths : list[Path] = []


    for index, season in enumerate(seasons.iterdir()):
        if season.is_dir(): 
            print(f'{index} - {index}ª TEMPORADA')
            season_paths.append(Path(season))

    printcl('RED', '\n0. SAIR')

    return season_paths

def warn_wrong_entry():
    cs_clear()
    printcl("YELLOW", "\nInsira um valor válido.\n")

def d2l_eventloop():
    ascii_art()

    while 1:
        season_paths = greet()
        season_selected = input()

        if(season_selected == "0"): exit()
        
        if season_selected.isdigit():
            season_index = int(season_selected) - 1

            if season_index < len(season_paths) and season_index > -1:
                season = season_paths[season_index]
                cs_clear()
                
                files = os.listdir(season)

                while 1:
                    for index, file in enumerate(season.iterdir(), start=1):
                        print(f'Epsiódio {index}: {file.stem}')

                    printcl('RED', '\n0 - Retornar')
                    choose = input()
                    if choose == "0": 
                        cs_clear()
                        break

                    if choose.isdigit():
                        index = int(choose) - 1
                        
                        if index < len(files) and index > -1:
                            story_struct = story_parser(season/files[index])
                            cs_clear()
                            input("Pressione [ENTER] para avançar nos dialogos.\n\n[ENTER] -> Ok!")
                            cs_clear()
                            
                            for action in story_processor(story_struct):
                                action['call']()
                                print("\n")
                                input()

                            print("-" * 50, "\n")
                        else:
                            warn_wrong_entry()
                    else:
                        warn_wrong_entry()
                        continue 
        else:
            warn_wrong_entry()

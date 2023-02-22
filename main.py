# main function of the program
# here will go only:
# calls for other modules, importations, and clean execution of pre-made functions
# this may be the primary program's module

import pygame, sys
from pygame.locals import *
import screen, character_structure, item_structure, health_system, storage_system, game_map, inputs
from screen import tamanho_da_tela, tamanho_dos_tiles

pygame.init()

def request_play(obj:character_structure.character, mapa, keys=None):
    response = None
    if keys:
        if keys[K_SPACE]:
            obj.catch(mapa.items)
        a = {K_UP:0, K_DOWN:1, K_LEFT:2, K_RIGHT:3}
        for i in a.keys():
            if keys[i]:
                response = obj.actions[0][a[i]]()
    else:
        response = obj.lance()
    if response in mapa.get_full_spaces(obj):
        obj.back_to_last_position()

def debug():
    pygame.time.Clock().tick(30)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

def flip_screen( disp ):
    pygame.display.flip()
    disp.fill((0,0,0))

def main():
    mapa_do_jogo = game_map.Map()
    display = screen.create(pygame)
    mapa_do_jogo.items.append(item_structure.Flashlight(mapa_do_jogo.lightpoints,(5, 0)))
    mapa_do_jogo.items.append(item_structure.Flashlight(mapa_do_jogo.lightpoints,(5, 8)))
    mapa_do_jogo.player = character_structure.character(
        (0, 0), health_system.HealthSystem, storage_system.StorageSystem
    )

    while 1:
        debug()
        keys = inputs.keys_update(pygame)
        request_play(mapa_do_jogo.player, mapa_do_jogo, keys)
        mapa_do_jogo.player.run()
        for i in mapa_do_jogo.items:
            i.run()
        screen.fill_background(pygame, display)
        screen.blit_player(pygame, display, mapa_do_jogo.player)
        screen.fill_background_fog(pygame, display, mapa_do_jogo.lightpoints)
        flip_screen(display)

main()
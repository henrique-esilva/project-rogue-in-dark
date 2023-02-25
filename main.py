# main function of the program
# here will go only:
# calls for other modules, importations, and clean execution of pre-made functions
# this may be the primary program's module

import pygame, sys, os
from pygame.locals import *
import screen, character_structure, item_structure, health_system, storage_system, game_map, inputs, graphics
from screen import tamanho_da_tela, tamanho_dos_tiles

dirpath = os.getcwd()
sys.path.append(dirpath)

if getattr(sys, "frozen", False):
    os.chdir(sys._MEIPASS)

pygame.init()

def request_play(obj:character_structure.character, mapa, keys=None):
    response = None
    last_position = obj.position
    if keys:
        if keys[K_SPACE]:
            obj.catch(mapa.items)
        a = {K_UP:'up', K_DOWN:'down', K_LEFT:'left', K_RIGHT:'right'}
        for i in a.keys():
            if keys[i]:
                response = obj.move_direction(a[i])
                obj.last_position = last_position
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
    mapa_do_jogo.player.animations = graphics.AnimationClass()
    mapa_do_jogo.player.animations.idle.configura(0)
    mapa_do_jogo.player.animations.idle.set(pygame,"imagens//tic", 39)
    mapa_do_jogo.player.animations.front.configura(0)
    mapa_do_jogo.player.animations.front.set(pygame,"imagens//jogador//front", 19)
    mapa_do_jogo.player.animations.back.configura(0)
    mapa_do_jogo.player.animations.back.set(pygame,"imagens//jogador//back", 28)
    mapa_do_jogo.player.animations.right.configura(0)
    mapa_do_jogo.player.animations.right.set(pygame,"imagens//jogador//right", 37)
    mapa_do_jogo.player.current_animation = mapa_do_jogo.player.animations.idle

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
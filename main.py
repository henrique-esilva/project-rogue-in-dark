# main function of the program
# here will go only:
# calls for other modules, importations, and clean execution of pre-made functions
# this may be the primary program's module

import sys, os
import pygame
from pygame.locals import *
import screen, character_structure, item_structure, health_system, storage_system, game_map, inputs, graphics, objetos
from screen import tamanho_da_tela, tamanho_dos_tiles

dirpath = os.getcwd()
sys.path.append(dirpath)

if getattr(sys, "frozen", False):
    os.chdir(sys._MEIPASS)

pygame.init()

def request_play(obj:character_structure.character, mapa_do_jogo, keys=None):
    response = None
    last_position = obj.position
    if keys:
        soma = [0, 0]
        if keys[K_RSHIFT]:
            obj.catch(mapa_do_jogo.items)
        elif keys[K_END] and not obj.catchcd:
            for i in mapa_do_jogo.caixas:
                dists = {}
                dists[ ( (obj.position[0]-i.position[0])**2 + (obj.position[1]-i.position[1])**2 ) ** 0.5 ] = i
                if min(dists.keys()) < 2:
                    interact = dists[min(dists.keys())]
                    if interact.interact(obj):
                        obj.catchcd = 10 # defina atraso de coleta de item para o maximo
        a = {K_UP:(1,-0.5), K_DOWN:(1,0.5), K_LEFT:(0,-0.5), K_RIGHT:(0,0.5)}
        for i in a.keys():
            last = obj.position
            if keys[i]:
                soma[a[i][0]] += a[i][1]
                response = obj.move_direction(a[i])
                for space in mapa_do_jogo.get_full_spaces(obj):
                    if pygame.Rect(response[0]*tamanho_dos_tiles[0], response[1]*tamanho_dos_tiles[1], tamanho_dos_tiles[0], tamanho_dos_tiles[1]).colliderect(pygame.Rect(space[0]*tamanho_dos_tiles[0], space[1]*tamanho_dos_tiles[1], tamanho_dos_tiles[0], tamanho_dos_tiles[1])):
                        obj.last_position = last
                        obj.back_to_last_position()
                        break
        obj.direction_for_rotate = soma.copy()
    else:
        obj.lance()
        evitar_colisao(obj, mapa_do_jogo=mapa_do_jogo)

def evitar_colisao(obj:character_structure.character, mapa_do_jogo:game_map.Map):
    try:
        if obj.intangible:return 0
    except:pass
    response = obj.position
    for space in mapa_do_jogo.get_full_spaces(obj):
        if pygame.Rect(response[0]*tamanho_dos_tiles[0], response[1]*tamanho_dos_tiles[1], tamanho_dos_tiles[0], tamanho_dos_tiles[1]).colliderect(pygame.Rect(space[0]*tamanho_dos_tiles[0], space[1]*tamanho_dos_tiles[1], tamanho_dos_tiles[0], tamanho_dos_tiles[1])):
            obj.back_to_last_position()
            break

def debug():
    pygame.time.Clock().tick(25)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

def main():
    graphics.ani_base['tic'] = graphics.import_animation(pygame, "imagens//tic", 39)
    graphics.ani_base['walk_ghost'] = graphics.import_animation(pygame, "imagens//fantasma", 0)

    display = screen.create(pygame)
    screen.configura_imagens(pygame)

    mapa_do_jogo = game_map.Map()
    mapa_do_jogo.caixas.append(objetos.Box((4,2),health_system.HealthSystem, storage_system.StorageSystem))
    mapa_do_jogo.items.append(item_structure.Flashlight(mapa_do_jogo.lightpoints,(5, 0)))
    mapa_do_jogo.items.append(item_structure.Flashlight(mapa_do_jogo.lightpoints,(5, 8)))

    a = character_structure.Standard_Ghost(
        (3, 2), health_system.HealthSystem, storage_system.StorageSystem
    )
    a.animation = graphics.Animation()
    a.animation.configura(0)
    a.animation.set_default('tic')
    mapa_do_jogo.enemies.append(a)

    a = character_structure.Standard_Ghost(
        (5, 3), health_system.HealthSystem, storage_system.StorageSystem
    )
    a.animation = graphics.Animation()
    a.animation.configura(0)
    a.animation.set_default('walk_ghost')
    a.counting_steps = [0, 0, 6, 1/2]
    mapa_do_jogo.enemies.append(a)
    del a

    mapa_do_jogo.player = character_structure.character(
        (0, 0), health_system.HealthSystem, storage_system.StorageSystem
    )
    mapa_do_jogo.player.animation = graphics.Animation()
    mapa_do_jogo.player.animation.configura(0)
    mapa_do_jogo.player.animation.set_default('tic')

    while 1:
        debug()
        keys = inputs.keys_update(pygame)
        request_play(mapa_do_jogo.player, mapa_do_jogo, keys)
        mapa_do_jogo.player.run()
        for i in mapa_do_jogo.enemies:
            request_play(i, mapa_do_jogo)
            i.run()
        for i in mapa_do_jogo.caixas:
            i.run()
        for i in mapa_do_jogo.items:
            i.run()

    
        screen.fill_background(display, mapa_do_jogo.lightpoints)
        screen.fill_boxes(display, mapa_do_jogo.caixas)
        screen.fill_items(display, mapa_do_jogo.items)
        screen.blit_player(pygame, display, mapa_do_jogo.player) # this need a call for pygame
        screen.fill_enemies(pygame, display, mapa_do_jogo.enemies) # this need a call for pygame too
        screen.fill_background_fog(display, mapa_do_jogo.lightpoints)
        screen.flip_screen(pygame, display)

main()
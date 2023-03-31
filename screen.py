from random import randint

tamanho_dos_tiles = (32, 32)
tamanho_da_tela = (20, 12)

imagem_preta_vazia = None
imagem_do_piso = None
imagem_da_caixa = None
imagens_de_itens = {}

def configura_imagens(pygame):
    global imagem_preta_vazia
    global imagem_do_piso
    global imagem_da_caixa
    global imagens_de_itens
    imagem_preta_vazia = pygame.Surface.convert_alpha( pygame.Surface.convert( pygame.Surface( tamanho_dos_tiles ) ) )
    imagem_do_piso = pygame.image.load("imagens/piso.png")
    imagem_da_caixa= pygame.image.load("imagens/mesa.png")
    imagens_de_itens['#flashlight'] = pygame.image.load("imagens/lanterna.png")

def create(pyg):
    pyg.display.set_caption("nome_do_jogo")
    flags = pyg.SCALED
    return pyg.display.set_mode(
        (
        tamanho_dos_tiles[0] * tamanho_da_tela[0],
        tamanho_dos_tiles[1] * tamanho_da_tela[1]
        ),
        flags
    )

def fill_background(display, lanternas):
    display.fill((100, 100, 100))
    img = imagem_do_piso
    for x in range(tamanho_da_tela[0]):
        for y in range(tamanho_da_tela[1]):
            #for i in lanternas:
            #    dists = []
            #    dists.append( ((i.position[0] - x) ** 2 + (i.position[1] - y) ** 2) ** (1/2) )
            #    if min(dists) < 6:
            display.blit(img, (x * tamanho_dos_tiles[0], y * tamanho_dos_tiles[1]))

def fill_boxes(display, caixas):
    a = []
    for i in caixas:
        a.append(i.position)
    for x in range(tamanho_da_tela[0]):
        for y in range(tamanho_da_tela[1]):
            if (x, y) in a:
                display.blit(imagem_da_caixa, (x * tamanho_dos_tiles[0], y * tamanho_dos_tiles[1]))

def fill_items(display, items):
    global imagens_de_itens
    a = []
    for i in items:
        a.append(i.position)
    for x in range(tamanho_da_tela[0]):
        for y in range(tamanho_da_tela[1]):
            if (x, y) in a:
                display.blit(imagens_de_itens[i.id], (x * tamanho_dos_tiles[0], y * tamanho_dos_tiles[1]))

def blit_player(pyg, display, player):
    if player.animation:
        img = pyg.transform.rotate(player.image, player.degrees)
        rect = img.get_rect()
        rect.center = (player.position[0]*tamanho_dos_tiles[0] + tamanho_dos_tiles[0]/2, player.position[1]*tamanho_dos_tiles[1]+tamanho_dos_tiles[1]/2)
        display.blit( img, rect)

def fill_enemies(pyg, display, enemies):
    for i in  enemies:
        blit_player(pyg, display, i)

def fill_background_fog(display, lanternas):

    lan = lanternas

    imagem = imagem_preta_vazia

    for x in range(tamanho_da_tela[0]):
        for y in range(tamanho_da_tela[1]):
            # calcular distancia em relacao ao jogador
            # preencher com um quadrado preto de canal alfa proporcional a distancia
            # o canal alfa sera proporcional a distribuicao de luz num plano

            pixel = (x, y)
            alt = {}
            for i in lan:
                pos = i.position
                dist = ( (pos[0] - pixel[0]) ** 2 + (pos[1] - pixel[1]) ** 2 ) ** (1/2) -2 -i.force
                alt[dist]=pos
            dist = min(alt.keys())
            if pixel!=alt[dist]:
                flut = i.get_flutuaction()
                intensidade = (16+flut)*(dist)**2 - (7-flut)*dist
                if intensidade >= 250: intensidade = 250
                imagem.fill((0,0,0))
                imagem.set_alpha( intensidade )
                display.blit( imagem, (x * tamanho_dos_tiles[0], y * tamanho_dos_tiles[1]) )

def flip_screen( pyg, disp ):
    pyg.display.flip()
    disp.fill((0,0,0))
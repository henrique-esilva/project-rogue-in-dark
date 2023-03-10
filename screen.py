from random import randint

tamanho_dos_tiles = (32, 32)
tamanho_da_tela = (20, 12)

imagem_preta_vazia = None
imagem_do_piso = None
imagem_da_caixa = None

def configura_imagens(pygame):
    global imagem_preta_vazia
    global imagem_do_piso
    global imagem_da_caixa
    imagem_preta_vazia = pygame.Surface.convert_alpha( pygame.Surface.convert( pygame.Surface( tamanho_dos_tiles ) ) )
    imagem_do_piso = pygame.image.load("imagens/piso.png")
    imagem_da_caixa= pygame.image.load("imagens/caixa.png")

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

def fill_background(pyg, display, lanternas):
    display.fill((100, 100, 100))
    img = imagem_do_piso
    for x in range(tamanho_da_tela[0]):
        for y in range(tamanho_da_tela[1]):
            #for i in lanternas:
            #    dists = []
            #    dists.append( ((i.position[0] - x) ** 2 + (i.position[1] - y) ** 2) ** (1/2) )
            #    if min(dists) < 6:
            display.blit(img, (x * tamanho_dos_tiles[0], y * tamanho_dos_tiles[1]))

def blit_player(pyg, display, player):
    if player.animations:
        img = pyg.transform.rotate(player.image, player.degrees)
        rect = img.get_rect()
        rect.center = (player.position[0]*tamanho_dos_tiles[0] + tamanho_dos_tiles[0]/2, player.position[1]*tamanho_dos_tiles[1]+tamanho_dos_tiles[1]/2)
        display.blit( img, rect)

def fill_background_fog(pyg, display, lanternas):

    lan = lanternas

    imagem = imagem_preta_vazia

    for x in range(tamanho_da_tela[0]):
        for y in range(tamanho_da_tela[1]):
            # calcular distancia em relacao ao jogador
            # preencher com um quadrado preto de canal alfa proporcional a distancia
            # o canal alfa sera proporcional a distribuicao de luz num plano
            # o canal alfa tera um pequeno raio de aleatoriedade somado ao final
            pixel = (x, y)
            alt = {}
            for i in lan:
                pos = i.position
                dist = ( (pos[0] - pixel[0]) ** 2 + (pos[1] - pixel[1]) ** 2 ) ** (1/2)
                alt[dist]=pos
            dist = min(alt.keys())
            if pixel!=alt[dist]:
                intensidade = 17*dist**2 - 7*dist
                if intensidade >= 250: intensidade = 250
                #255 -(200/(0.3 * dist**2)) + randint( 0, 3 )
                imagem.fill((0,0,0))
                imagem.set_alpha( intensidade )
                display.blit( imagem, (x * tamanho_dos_tiles[0], y * tamanho_dos_tiles[1]) )

def fill_boxes(pyg, display, caixas):
    a = []
    for i in caixas:
        a.append(i.position)
    for x in range(tamanho_da_tela[0]):
        for y in range(tamanho_da_tela[1]):
            if (x, y) in a:
                display.blit(imagem_da_caixa, (x * tamanho_dos_tiles[0], y * tamanho_dos_tiles[1]))
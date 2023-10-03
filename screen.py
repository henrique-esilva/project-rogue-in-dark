from random import randint

tamanho_dos_tiles = (32, 32)
tamanho_da_tela = (20, 12)

imagem_preta_vazia = None
imagem_do_piso = None
imagem_da_caixa = None
imagens_das_paredes = None
imagens_de_itens = {}
imagens={}

def configura_imagens(pygame):
    global imagem_preta_vazia
    global imagem_do_piso
    global imagem_da_caixa
    global imagens_de_itens
    global imagens_das_paredes
    imagem_preta_vazia = pygame.Surface.convert_alpha( pygame.Surface.convert( pygame.Surface( tamanho_dos_tiles ) ) )
    imagem_do_piso = pygame.image.load("imagens/piso.png")
    imagem_da_caixa= pygame.image.load("imagens/mesa.png")
    imagens["#door"]=pygame.image.load("imagens/porta.png")
    imagens["#lamp"]=pygame.image.load("imagens/lamp.png")
    imagens_das_paredes = []
    a=pygame.image.load("imagens/paredes-musgo/spritesheet.png")
    for x in range(12):
        img=pygame.Surface((32,32))
        img.blit(a,(0,0),pygame.Rect(32*x,0,32,32))
        imagens_das_paredes.append(img)
        
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

def render(display, image, vetor:iter):
    for i in vetor:
        display.blit(image, (i[0] * tamanho_dos_tiles[0], i[1] * tamanho_dos_tiles[1]))

def fill_background(display): # deprecated
    for x in range(tamanho_da_tela[0]):
        for y in range(tamanho_da_tela[1]):
            display.blit(imagem_do_piso, (x * tamanho_dos_tiles[0], y * tamanho_dos_tiles[1]))

def fill_floors(display, floors):
    for i in floors:
        initial = list(i[0])
        while initial[0] <= i[1][0]:
            while initial[1] <= i[1][1]:
                display.blit(imagem_do_piso, (initial[0] * tamanho_dos_tiles[0], initial[1] * tamanho_dos_tiles[1]))
                initial[1]+=1
            initial[0]+=1
            initial[1]=i[0][1]

def fill_walls(display, paredes):
    for n in range(len(paredes)):
        for i in paredes[n]:
            render(display, imagens_das_paredes[n], paredes[n])

def fill_objects(display, caixas):
    for i in caixas:
        a = []
        vetor=caixas.get(i)
        img=imagens[i]
        for i in vetor:
            if not i.invisible:
                a.append(i.position)
        render(display, img, a)

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
        display.blit( img, rect )

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
                if intensidade >= 251: intensidade = 251
                imagem.fill((0,0,0))
                imagem.set_alpha( intensidade )
                display.blit( imagem, (x * tamanho_dos_tiles[0], y * tamanho_dos_tiles[1]) )

def flip_screen( pyg, disp ):
    pyg.display.flip()
    disp.fill((0,0,0))
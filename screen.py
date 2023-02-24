from random import randint

tamanho_dos_tiles = (32, 32)
tamanho_da_tela = (10, 10)

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

def fill_background(pyg, display):
    display.fill((100, 100, 100))
    img = pyg.image.load("imagens/piso.png")
    for x in range(tamanho_da_tela[0]):
        for y in range(tamanho_da_tela[1]):
            display.blit(img, (x * tamanho_dos_tiles[0], y * tamanho_dos_tiles[1]))

def blit_player(pyg, display, player):
    if player.animations:
        img = pyg.transform.rotate(player.image, player.degrees)
        rect = img.get_rect()
        rect.center = (player.position[0]*tamanho_dos_tiles[0] + tamanho_dos_tiles[0]/2, player.position[1]*tamanho_dos_tiles[1]+tamanho_dos_tiles[1]/2)
        display.blit( img, rect)#pyg.Rect(player.position[0]*tamanho_dos_tiles[0], player.position[1]*tamanho_dos_tiles[1], tamanho_dos_tiles[0], tamanho_dos_tiles[1]) )
        return 0

def fill_background_fog(pyg, display, lanternas):

    lan = lanternas

    imagem = pyg.Surface.convert_alpha( pyg.Surface.convert( pyg.Surface( tamanho_dos_tiles ) ) )

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
                intensidade = 255 -(200/(0.3 * dist**2)) + randint( 0, 3 )
                imagem.fill((0,0,0))
                imagem.set_alpha( intensidade )
                display.blit( imagem, (x * tamanho_dos_tiles[0], y * tamanho_dos_tiles[1]) )
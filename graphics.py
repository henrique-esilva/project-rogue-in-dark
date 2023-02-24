import math, sys

#  pegar o valor de retorno com
#  uma VAR, ok?
def import_animation(pygame, arg, start = 0):     # O "arg"(parametro) deve ser o nome do diretório + "\\" + nome da animação. E PRONTO. O subprograma faz o resto
    a = []

    for i in range ( start , 999 ):
        try:


            patch = arg + ("\\frame%04d.png" % i)      # Aqui é criada uma string do caminho da imagem

            a.append(          pygame.image.load( patch )          )    # Aqui a imagem é importada

        except:    break

    if len(a) == 0:

        print('\nWARNING: \'import_animation()\' retornando vetor de 0 (zero) valores')
        print('    a animação não está recebendo nenhum quadro!')
    return a

class AnimationClass():

	def __init__(self):

		self.idle = Animation()
		self.front = Animation()
		self.back = Animation()
		self.right = Animation()



class Animation():

	def __init__(self):

		self.content = []
		self.inicioDoLoop = 0
		self.repetindo = True
		self.rodando = True
		self.index = 0

	def configura(self, inicioDoLoop):
		self.inicioDoLoop = inicioDoLoop

	def set(self, pygame, path = None, start = 0 ):

		if path:

			self.path = path
			self.content = import_animation( pygame, path, start )
		else:

			try:

				self.content = import_animation( pygame, self.path )
			except AttributeError:
				print('\nWARNING: Animation() class in Animation.set() function')
				print('    recebendo valor nulo para o caminho de diretório!')
				print('    resulta em tentativa falha de auto-incrementação\n')
				print('    erro iminente!\n')

	def turnOn(self):

		self.rodando = True
		self.index = 0

	def turnOff(self):

		self.rodando = False

	def configura_repeteco(self, arg):
		
		self.repetindo = arg

	def run(self):

		if self.rodando:

			self.index += 1
			if self.index >= len(self.content):
				try:
					if self.repetindo:
						self.index = self.inicioDoLoop
					else:
						self.turnOff()
						self.index = 0

				except AttributeError:
					print('WARNING: erro de atribuição de instância em \'Animation.run()\'')
					print('    configure a classe de animação!')

	def retorna_quadro(self):

		try:
			return self.content[math.floor( self.index )]	

		except IndexError:
			print( '\nWARNING: \'index\' invalido para -> \'Animation\' em \'retorna_valor()\'' )
			print( 'index =', self.index )
			print( 'efetivo =', math.floor( self.index ) )
			print( 'len(self.content) = ' + str(len(self.content)) + '\n')
			sys.exit()
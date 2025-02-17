import pygame
from random import randint
import ctypes #Esto hasta print(ancho,alto) para tamaño pantalla equipo


user32 = ctypes.windll.user32
user32.SetProcessDPIAware()
ancho, alto = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
#print(ancho, alto) Hasta aqui lo de la pantalla
pygame.init()
ventana = pygame.display.set_mode((ancho,alto))
pygame.display.set_caption("ARKANOID")

fondo = pygame.image.load('FONDO.png')

ball = pygame.image.load("Bakugan.png")
ballrect = ball.get_rect()
speed = [randint(3,6),randint(3,6)]
ballrect.move_ip(0,0)

barra = pygame.image.load("BATE.png")
barrarect = barra.get_rect()
barrarect.move_ip(240,540)

fuente = pygame.font.Font(None, 36)

class CartaVerde():
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 120, 40)  # Rectángulo del bloque
        self.color = (0, 255, 0)  # Color verde
    def dibujar(self, ventana):
        pygame.draw.rect(ventana, self.color, self.rect)

def crear_fila_de_bloques():
    bloques = []
    espaciado = 5  # Espacio entre bloques
    cantidad_bloques = 10  # Número de bloques en la fila
    for i in range(cantidad_bloques):
        for j in range(3):
            x = i * (ancho // cantidad_bloques) - (espaciado)  + 30
            y = j * (alto // 3 -300) + 30 # Fila de bloques en la parte superior
            bloque = CartaVerde(x, y)
            bloques.append(bloque)

    for i in range(cantidad_bloques):
        for j in range(3):
            x = i * (ancho // cantidad_bloques) - (espaciado)  + 30
            y = j * (alto// 3 - 420) + 1000 # Fila de bloques en la parte superior
            bloque = CartaVerde(x, y)
            bloques.append(bloque)
    return bloques

bloques = crear_fila_de_bloques()

jugando = True
while jugando:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            jugando = False
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        barrarect = barrarect.move(-9,0)
    if keys[pygame.K_RIGHT]:
        barrarect = barrarect.move(9,0)
    if keys[pygame.K_UP]:
        barrarect = barrarect.move(0,-6)
    if keys[pygame.K_DOWN]:
        barrarect = barrarect.move(0,6)

    if barrarect.colliderect(ballrect):
        speed[1] = -speed[1]

    ballrect = ballrect.move(speed)
    if ballrect.left < 0 or ballrect.right > ventana.get_width():
        speed[0] = -speed[0]
        
    if ballrect.top < 0: 
        speed[1] = -speed[1]
        
    if ballrect.bottom > alto:  # Rebote en la parte inferior
        speed[1] = -speed[1]
        
    if ballrect.bottom > ventana.get_height():
        texto = fuente.render("Game Over", True, (125,125,125))
        texto_rect = texto.get_rect()
        texto_x = ventana.get_width() / 2 - texto_rect.width / 2
        texto_y = ventana.get_height() / 2 - texto_rect.height / 2
        ventana.blit(texto, [texto_x, texto_y])
    else:
        ventana.blit(fondo, (0,0))
        ventana.blit(ball, ballrect)
        ventana.blit(barra, barrarect)

         # Dibujar los bloques
        for bloque in bloques:
            bloque.dibujar(ventana)

    pygame.display.flip()
    pygame.time.Clock().tick(120)


pygame.quit()
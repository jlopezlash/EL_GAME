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
ballrect.move_ip(200,500)

barra = pygame.image.load("BATE.png")
barrarect = barra.get_rect()
barrarect.move_ip(240,540)

vidas = 3

fuente = pygame.font.Font(None, 36)

class CartaVerde():
    def __init__(self, x, y, vida = 2):   
        self.rect = pygame.Rect(x, y, 120, 40)  # Rectángulo del bloque
        self.color = (255, 255, 0) if vida == 2 else (0, 255, 0)  # Amarillo para bloques más resistentes
        self.vida = vida #numero de vida del bloque

    def dibujar(self, ventana):
        pygame.draw.rect(ventana, self.color, self.rect)

    def colisiona(self, ballrect):
        """ Verifica si la pelota colisiona con el bloque """
        return self.rect.colliderect(ballrect)
    
    def recibir_golpe(self):
        """Reduce la vida del bloque y cambia de color si es necesario"""
        self.vida -= 1
        if self.vida == 1:
            self.color = (0, 255, 0)  # Cambia a verde si queda un golpe

def crear_fila_de_bloques():
    bloques = []
    espaciado = 5  # Espacio entre bloques
    cantidad_bloques = 10  # Número de bloques en la fila
    for i in range(cantidad_bloques):
        for j in range(3):
            x = i * (ancho // cantidad_bloques) - (espaciado)  + 30
            y = j * (alto // 3 -300) + 30 # Fila de bloques en la parte superior
            vida = 2 if randint(0, 1) else 1  # Algunos bloques requieren 2 toques
            bloques.append(CartaVerde(x, y, vida))

    for i in range(cantidad_bloques):
        for j in range(3):
            x = i * (ancho // cantidad_bloques) - (espaciado)  + 30
            y = j * (alto// 3 - 420) + 1000 # Fila de bloques en la parte superior
            vida = 2 if randint(0, 1) else 1  # Algunos bloques requieren 2 toques
            bloques.append(CartaVerde(x, y, vida))
    return bloques

bloques = crear_fila_de_bloques()

jugando = True
while jugando:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            jugando = False
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and barrarect.left > 0:  #mueve la barra y no la deja salirse
        barrarect = barrarect.move(-9, 0)
    if keys[pygame.K_RIGHT] and barrarect.right < ancho:
        barrarect = barrarect.move(9, 0)

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

        # Detectar colisión con los bloques
        for bloque in bloques[:]:
            if bloque.colisiona(ballrect):  # Si la pelota colisiona con el bloque
                bloque.recibir_golpe()  # Reducir la vida del bloque y cambiar de color
                if bloque.vida <= 0:
                    bloques.remove(bloque)  # Elimina el bloque de la lista si ya no tiene vidas
                speed[1] = -speed[1]  # Rebote de la pelota

         # Dibujar los bloques
        for bloque in bloques:
            bloque.dibujar(ventana)

    texto_vidas = fuente.render(f'Vidas: {vidas}', True, (255,255,255))
    ventana.blit(texto_vidas, (5,5))    #Muesta de las vidas por pantalla

    pygame.display.flip()
    pygame.time.Clock().tick(120)


pygame.quit()
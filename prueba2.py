import pygame
from random import randint
import ctypes  

# Obtener tamaño de pantalla
user32 = ctypes.windll.user32
user32.SetProcessDPIAware()
ancho, alto = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)

pygame.init()
ventana = pygame.display.set_mode((ancho, alto))
pygame.display.set_caption("ARKANOID")

# Cargar imágenes
fondo = pygame.image.load('FONDO.png')
ball = pygame.image.load("Bakugan.png")
ballrect = ball.get_rect()
speed = [randint(3, 6), randint(3, 6)]
ballrect.move_ip(ancho // 2, alto // 2)

barra = pygame.image.load("BATE.png")
barrarect = barra.get_rect()
barrarect.move_ip(ancho // 2, alto - 50)

vidas = 3
fuente = pygame.font.Font(None, 36)

class CartaVerde:
    def __init__(self, x, y, vida=1):
        self.rect = pygame.Rect(x, y, 120, 40)
        self.vida = vida  # Número de toques necesarios
        self.color = (0, 255, 0) if vida == 1 else (255, 255, 0)  # Amarillo para bloques más resistentes

    def dibujar(self, ventana):
        pygame.draw.rect(ventana, self.color, self.rect)

    def colisiona(self, ballrect):
        return self.rect.colliderect(ballrect)

    def recibir_golpe(self):
        """Reduce la vida del bloque y cambia de color si es necesario"""
        self.vida -= 1
        if self.vida == 1:
            self.color = (0, 255, 0)  # Cambia a verde si queda un golpe

def crear_fila_de_bloques():
    bloques = []
    espaciado = 5
    cantidad_bloques = 10
    for i in range(cantidad_bloques):
        for j in range(3):
            x = i * (ancho // cantidad_bloques) + 30
            y = j * (alto // 3 - 300) + 30
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
    if keys[pygame.K_LEFT] and barrarect.left > 0:
        barrarect = barrarect.move(-9, 0)
    if keys[pygame.K_RIGHT] and barrarect.right < ancho:
        barrarect = barrarect.move(9, 0)

    # Rebote con la barra
    if barrarect.colliderect(ballrect):
        speed[1] = -speed[1]

    # Movimiento de la pelota
    ballrect = ballrect.move(speed)
    if ballrect.left < 0 or ballrect.right > ventana.get_width():
        speed[0] = -speed[0]
    if ballrect.top < 0:
        speed[1] = -speed[1]

    # Si la pelota toca el fondo
    if ballrect.bottom > alto:
        vidas -= 1
        ballrect.topleft = (ancho // 2, alto // 2)
        speed = [randint(3, 6), -randint(3, 6)]  # Reiniciar velocidad

        if vidas == 0:
            jugando = False

    # Dibujar en pantalla
    ventana.blit(fondo, (0, 0))
    ventana.blit(ball, ballrect)
    ventana.blit(barra, barrarect)

    # Colisión con los bloques
    for bloque in bloques[:]:
        if bloque.colisiona(ballrect):
            bloque.recibir_golpe()
            if bloque.vida == 0:
                bloques.remove(bloque)
            speed[1] = -speed[1]  # Rebote de la pelota

    # Dibujar bloques
    for bloque in bloques:
        bloque.dibujar(ventana)

    # Mostrar vidas
    texto_vidas = fuente.render(f'Vidas: {vidas}', True, (255, 255, 255))
    ventana.blit(texto_vidas, (5, 5))

    pygame.display.flip()
    pygame.time.Clock().tick(120)

# Mostrar mensaje de "Game Over"
ventana.fill((0, 0, 0))
texto = fuente.render("Game Over", True, (255, 0, 0))
texto_rect = texto.get_rect(center=(ancho // 2, alto // 2))
ventana.blit(texto, texto_rect)
pygame.display.flip()
pygame.time.delay(3000)  # Esperar 3 segundos antes de cerrar
pygame.quit()

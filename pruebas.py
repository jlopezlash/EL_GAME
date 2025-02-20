import pygame
from random import randint
import ctypes

user32 = ctypes.windll.user32
user32.SetProcessDPIAware()
ancho, alto = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
pygame.init()
ventana = pygame.display.set_mode((ancho, alto))
pygame.display.set_caption("ARKANOID")

fondo = pygame.image.load('FONDO.png')

ball = pygame.image.load("Bakugan.png")
ballrect = ball.get_rect()
speed = [randint(10, 10), randint(10, 10)]
ballrect.move_ip(200, 500)

barra = pygame.image.load("BATE.png")
barrarect = barra.get_rect()
barrarect.move_ip(240, 540)

vidas = 3

fuente = pygame.font.Font(None, 36)

# Clase para bloques estándar, bloques que quitan o suman vidas
class CartaVerde():
    def __init__(self, x, y, tipo='normal', vida=2):   
        self.rect = pygame.Rect(x, y, 120, 40)  # Rectángulo del bloque
        self.tipo = tipo  # Tipo de bloque ('normal', 'quitar', 'sumar')
        self.vida = vida  # Número de vidas del bloque
        # Asignar colores según el tipo de bloque
        if self.tipo == 'normal':
            self.color = (0, 255, 0)  # Verde para los bloques normales
        elif self.tipo == 'reforzado':
            self.color = (255,255,0)
        elif self.tipo == 'quitar':
            self.color = (255, 0, 0)  # Rojo para los bloques que quitan vida
        elif self.tipo == 'sumar':
            self.color = (0, 0, 255)  # Azul para los bloques que suman vida

    def dibujar(self, ventana):
        pygame.draw.rect(ventana, self.color, self.rect)

    def colisiona(self, ballrect):
        """ Verifica si la pelota colisiona con el bloque """
        return self.rect.colliderect(ballrect)
    
    def recibir_golpe(self):
        """ Reduce la vida del bloque y cambia de color si es necesario """
        if self.tipo == 'reforzado':  # Bloques normales (amarillos)
            self.vida -= 1
            if self.vida == 1:
                return 'normal'  # Elimina el bloque
        elif self.tipo == 'quitar':
            return 'quitar_vida'  # Bloque que quita vida
        elif self.tipo == 'sumar':
            return 'sumar_vida'  # Bloque que suma vida

def crear_fila_de_bloques():
    bloques = []
    espaciado = 5  # Espacio entre bloques
    cantidad_bloques = 10  # Número de bloques en la fila
    for i in range(cantidad_bloques):
        for j in range(3):
            x = i * (ancho // cantidad_bloques) - (espaciado) + 30
            y = j * (alto // 3 - 300) + 30  # Fila de bloques en la parte superior
            tipo = 'reforzado'  # Por defecto, el bloque es normal (amarillo)
            # Aleatoriamente asignar un bloque que sume, reste vidas o sea normal
            probabilidad = randint(0, 5)
            if probabilidad == 0:
                tipo = 'quitar'  # Bloque que quita una vida
                vida = 1
            elif probabilidad == 1:
                tipo = 'sumar'  # Bloque que suma una vida
                vida = 1
            elif probabilidad == 2:
                tipo = 'reforzado'  # Bloque que suma una vida
                vida = 2
            else:
                tipo = 'normal'  # Bloque normal (verde) con dos vidas
                vida = 1  # Los bloques amarillos tienen 2 vidas
            bloques.append(CartaVerde(x, y, tipo, vida))

    return bloques

bloques = crear_fila_de_bloques()

jugando = True
while jugando:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            jugando = False

    keys = pygame.key.get_pressed()
    
    # Movimiento de la barra con restricciones para no salirse de la pantalla
    if keys[pygame.K_LEFT] and barrarect.left > 0:  # Mueve la barra y no la deja salirse
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
        texto = fuente.render("Game Over", True, (125, 125, 125))
        texto_rect = texto.get_rect()
        texto_x = ventana.get_width() / 2 - texto_rect.width / 2
        texto_y = ventana.get_height() / 2 - texto_rect.height / 2
        ventana.blit(texto, [texto_x, texto_y])
    else:
        ventana.blit(fondo, (0, 0))
        ventana.blit(ball, ballrect)
        ventana.blit(barra, barrarect)

        # Detectar colisión con los bloques
        for bloque in bloques[:]:
            if bloque.colisiona(ballrect):  # Si la pelota colisiona con el bloque
                resultado = bloque.recibir_golpe()  # Reducir la vida del bloque y cambiar de color
                if resultado == 'eliminar':  # Eliminar el bloque si ya no tiene vida
                    bloques.remove(bloque)
                elif resultado == 'quitar_vida':  # Si el bloque quita una vida
                    vidas -= 1
                    bloques.remove(bloque)
                elif resultado == 'sumar_vida':  # Si el bloque suma una vida
                    vidas += 1
                    bloques.remove(bloque)
                speed[1] = -speed[1]  # Rebote de la pelota

        # Dibujar los bloques
        for bloque in bloques:
            bloque.dibujar(ventana)

    texto_vidas = fuente.render(f'Vidas: {vidas}', True, (255, 255, 255))
    ventana.blit(texto_vidas, (5, 5))  # Mostrar las vidas por pantalla

    pygame.display.flip()
    pygame.time.Clock().tick(120)

pygame.quit()

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
speed = [randint(8, 12), randint(8, 12)]
ballrect.move_ip(200, 500)

barra = pygame.image.load("BATE.png")
barrarect = barra.get_rect()
barrarect.move_ip(240, 540)

vidas = 3

fuente = pygame.font.Font(None, 36)

contador = 0

# Clase para los bloques
class CartaVerde():
    def __init__(self, x, y, tipo='normal', vida=1):   
        self.rect = pygame.Rect(x, y, 120, 40)  # Rectángulo del bloque
        self.tipo = tipo  # Tipo de bloque
        self.vida = vida  # Número de vidas del bloque
        
        # Asignar colores según el tipo de bloque
        if self.tipo == 'amarillo':
            self.color = (255, 255, 0)  # Amarillo
        elif self.tipo == 'verde':
            self.color = (0, 255, 0)  # Verde
        elif self.tipo == 'rojo':
            self.color = (255, 0, 0)  # Rojo
        elif self.tipo == 'azul':
            self.color = (0, 0, 255)  # Azul
    def dibujar(self, ventana):
        pygame.draw.rect(ventana, self.color, self.rect)

    def colisiona(self, ballrect):
        """ Verifica si la pelota colisiona con el bloque """
        return self.rect.colliderect(ballrect)
    
    def recibir_golpe(self):
        """ Lógica para lo que sucede al ser golpeado """
        if self.tipo == 'amarillo':
            self.tipo = 'verde'  # Cambia a verde cuando es golpeado
            self.color = (0, 255, 0)  # Cambia color a verde
        elif self.tipo == 'verde':
            return 'eliminar'  # El bloque verde se elimina
        elif self.tipo == 'rojo':
            return 'quitar_vida'  # Bloque rojo quita vida
        elif self.tipo == 'azul':
            return 'sumar_vida'  # Bloque azul suma vida

def crear_fila_de_bloques():
    bloques = []
    espaciado = 5  # Espacio entre bloques
    cantidad_bloques = 10  # Número de bloques en la fila
    for i in range(cantidad_bloques):
        for j in range(3):
            x = i * (ancho // cantidad_bloques) - (espaciado) + 30
            y = j * (alto // 3 - 300) + 30  # Fila de bloques en la parte superior

            tipo = randint(0, 7)  # Aleatoriamente elegimos entre 4 tipos
            if tipo == 0 or tipo ==1 :
                bloques.append(CartaVerde(x, y, tipo='amarillo'))  # Bloque amarillo
           
            elif tipo == 2 or tipo ==  3 or tipo == 4 or tipo ==  5:
                bloques.append(CartaVerde(x, y, tipo='verde'))  # Bloque verde
            elif tipo == 6:
                bloques.append(CartaVerde(x, y, tipo='azul'))  # Bloque azul
                contador +=1
            elif tipo == 7:
                bloques.append(CartaVerde(x, y, tipo='rojo'))  # Bloque rojo
                contador +=1

    for k in range(cantidad_bloques):
        for l in range(3):
            x = k * (ancho // cantidad_bloques) - (espaciado)  + 30
            y = l * (alto// 3 - 420) + 1000 # Fila de bloques en la parte superior
            # Asignar un tipo aleatorio de bloque

            tipo = randint(0, 9)  # Aleatoriamente elegimos entre 4 tipos
            if tipo == 0 or tipo ==1 :
                bloques.append(CartaVerde(x, y, tipo='amarillo'))  # Bloque amarillo
            elif tipo == 2 or tipo ==  3 or tipo == 4 or tipo ==  5:
                bloques.append(CartaVerde(x, y, tipo='verde'))  # Bloque verde
            elif tipo == 6:
                bloques.append(CartaVerde(x, y, tipo='azul'))  # Bloque azul
                contador +=1
            elif tipo == 7 or tipo ==8 or tipo==9:
                bloques.append(CartaVerde(x, y, tipo='rojo'))  # Bloque rojo
                contador +=1
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
        
    if vidas== 0:
        texto = fuente.render("Game Over", True, (125, 125, 125))
        texto_rect = texto.get_rect()
        texto_x = ventana.get_width() / 2 - texto_rect.width / 2
        texto_y = ventana.get_height() / 2 - texto_rect.height / 2
        ventana.blit(texto, [texto_x, texto_y])

    if len(bloques)==contador:
        texto = fuente.render("You Win...IÑAKIIIII", True, (125, 125, 125))
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
                resultado = bloque.recibir_golpe()  # Procesar el golpe
                if resultado == 'eliminar':  # Eliminar el bloque (amarillo, verde, rojo y azul)
                    bloques.remove(bloque)
                elif resultado == 'quitar_vida':  # Si es un bloque rojo, quitar vida
                    vidas -= 1
                    speed[0] += 4
                    speed[1] += 4
                    bloques.remove(bloque)
                elif resultado == 'sumar_vida':  # Si es un bloque azul, sumar vida
                    vidas += 1
                    bloques.remove(bloque)
                speed[1] = -speed[1]  # Rebote de la pelota

        # Dibujar los bloques
        for bloque in bloques:
            bloque.dibujar(ventana)

    texto_vidas = fuente.render(f'Vidas: {vidas}', True, (255, 255, 255))
    ventana.blit(texto_vidas, (5, 5))  # Mostrar las vidas por pantalla

    pygame.display.flip()
    pygame.time.Clock().tick(60)

pygame.quit()

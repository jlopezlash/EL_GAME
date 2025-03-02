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
speed = [randint(20, 25), randint(20, 25)]
ballrect.move_ip(200, 500)

barra = pygame.image.load("BATE.png")
barrarect = barra.get_rect()
barrarect.move_ip(240, 540)

bloque_amarillo = pygame.image.load("cartaamarilla.jpg")
bloque_verde = pygame.image.load("carta1.jpg")
bloque_rojo = pygame.image.load("cartadragonoid.jpg")
bloque_azul = pygame.image.load("carta4.jpg")

vidas = 3

fuente = pygame.font.Font(None, 36)


# Clase para los bloques
class CartaVerde():
    def __init__(self, x, y, tipo='normal', vida=1):   
        self.rect = pygame.Rect(x, y, 120, 40)  # Rectángulo del bloque
        self.tipo = tipo  # Tipo de bloque
        self.vida = vida  # Número de vidas del bloque
        # Asignar colores según el tipo de bloque
        if self.tipo == 'amarillo':
            self.imagen = bloque_amarillo   #Amarillo
        elif self.tipo == 'verde':
            self.imagen = bloque_verde  #Verde
        elif self.tipo == 'rojo':
            self.imagen = bloque_rojo   #Rojo
        elif self.tipo == 'azul':
            self.imagen = bloque_azul  # Azul
            
        self.imagen = pygame.transform.scale(self.imagen, (120, 40))  # Ajustar el tamaño
    def dibujar(self, ventana):
        ventana.blit(self.imagen, self.rect)  # Usar la imagen del bloque en lugar de un rectángulo

    def colisiona(self, ballrect):
        """ Verifica si la pelota colisiona con el bloque """
        return self.rect.colliderect(ballrect)
    
    def recibir_golpe(self):
        """ Lógica para lo que sucede al ser golpeado """
        if self.tipo == 'amarillo':
            self.tipo = 'verde'  # Cambia a verde cuando es golpeado
            self.imagen = bloque_verde # Cambia color a verde
            self.imagen = pygame.transform.scale(self.imagen, (120, 40))  # Ajustar el tamaño
        elif self.tipo == 'verde':
            return 'eliminar'  # El bloque verde se elimina
        elif self.tipo == 'rojo':
            return 'quitar_vida'  # Bloque rojo quita vida
        elif self.tipo == 'azul':
            return 'sumar_vida'  # Bloque azul suma vida

class CartaIrrompible(CartaVerde):
    def __init__(self, x, y, tipo='irrompible'):   
        self.rect = pygame.Rect(x, y, 120, 40)  # Rectángulo del bloque
        self.tipo = tipo  # Tipo de bloque
    
    def dibujar(self, ventana):
        pygame.draw.rect(ventana, (0, 0, 0), self.rect)  # Dibuja un rectángulo blanco para los bloques irrompibles

    def recibir_golpe(self):
        """ Lógica para lo que sucede al ser golpeado, no cambia nada ya que es irrompible """
        return None  # No hace nada al recibir un golpe
                
                      
def crear_fila_de_bloques():
    bloques = []
    espaciado = 5  # Espacio entre bloques
    cantidad_bloques = 10  # Número de bloques en la fila
    for i in range(cantidad_bloques):
        for j in range(3):
            x = i * (ancho // cantidad_bloques) - (espaciado) + 30
            y = j * (alto // 3 - 300) + 30  # Fila de bloques en la parte superior

            tipo = randint(0, 8)  # Aleatoriamente elegimos entre 4 tipos
            if tipo == 0 or tipo ==1 :
                bloques.append(CartaVerde(x, y, tipo='amarillo'))  # Bloque amarillo
           
            elif tipo == 2 or tipo ==  3 or tipo == 4 or tipo ==  5:
                bloques.append(CartaVerde(x, y, tipo='verde'))  # Bloque verde
            elif tipo == 6:
                bloques.append(CartaVerde(x, y, tipo='azul'))  # Bloque azul
            elif tipo == 7:
                bloques.append(CartaVerde(x, y, tipo='rojo'))  # Bloque rojo
            elif tipo == 8:
                bloques.append(CartaIrrompible(x, y, tipo='irrompible'))

    for k in range(cantidad_bloques):
        for l in range(3):
            x = k * (ancho // cantidad_bloques) - (espaciado)  + 30
            y = l * (alto// 3 - 420) + 1000 # Fila de bloques en la parte superior
            # Asignar un tipo aleatorio de bloque

            tipo = randint(0, 8)  # Aleatoriamente elegimos entre 4 tipos
            if tipo == 0 or tipo ==1 :
                bloques.append(CartaVerde(x, y, tipo='amarillo'))  # Bloque amarillo
            elif tipo == 2 or tipo ==  3 or tipo == 4 or tipo ==  5:
                bloques.append(CartaVerde(x, y, tipo='verde'))  # Bloque verde
            elif tipo == 6:
                bloques.append(CartaVerde(x, y, tipo='azul'))  # Bloque azul
            elif tipo == 7:
                bloques.append(CartaVerde(x, y, tipo='rojo'))  # Bloque rojo
            elif tipo == 8:
                bloques.append(CartaIrrompible(x, y, tipo='irrompible'))
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
        barrarect = barrarect.move(-30, 0)
    if keys[pygame.K_RIGHT] and barrarect.right < ancho:
        barrarect = barrarect.move(30, 0)

    if barrarect.colliderect(ballrect):
        # Ajustar la posición de la pelota para que no quede "dentro" de la barra
        if ballrect.bottom > barrarect.top and ballrect.top < barrarect.top:
            ballrect.bottom = barrarect.top
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
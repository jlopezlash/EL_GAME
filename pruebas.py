import pygame
import random

# Inicializar pygame
pygame.init()

# Configuración de la pantalla
ANCHO, ALTO = 800, 600
screen = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Arkanoid")

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
ROJO = (255, 0, 0)
AZUL = (0, 0, 255)

# Configuración de la paleta
paddle_ancho = 100
paddle_alto = 10
paddle_x = (ANCHO - paddle_ancho) // 2
paddle_y = ALTO - 30
paddle_vel = 8

# Configuración de la pelota
ball_radio = 10
ball_x = ANCHO // 2
ball_y = ALTO // 2
ball_vel_x = random.choice([-4, 4])
ball_vel_y = -4

# Configuración de los bloques
bloque_ancho = 75
bloque_alto = 20
bloques = []
for i in range(8):
    for j in range(5):
        bloque_x = i * (bloque_ancho + 5) + 35
        bloque_y = j * (bloque_alto + 5) + 50
        bloques.append(pygame.Rect(bloque_x, bloque_y, bloque_ancho, bloque_alto))

# Bucle principal
jugando = True
while jugando:
    pygame.time.delay(20)
    
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            jugando = False
    
    # Movimiento de la paleta
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and paddle_x > 0:
        paddle_x -= paddle_vel
    if keys[pygame.K_RIGHT] and paddle_x < ANCHO - paddle_ancho:
        paddle_x += paddle_vel
    
    # Movimiento de la pelota
    ball_x += ball_vel_x
    ball_y += ball_vel_y
    
    # Colisiones con las paredes
    if ball_x <= 0 or ball_x >= ANCHO - ball_radio * 2:
        ball_vel_x = -ball_vel_x
    if ball_y <= 0:
        ball_vel_y = -ball_vel_y
    
    # Colisión con la paleta
    if (paddle_x < ball_x < paddle_x + paddle_ancho) and (paddle_y < ball_y + ball_radio * 2 < paddle_y + paddle_alto):
        ball_vel_y = -ball_vel_y
    
    # Colisión con los bloques
    for bloque in bloques[:]:
        if bloque.collidepoint(ball_x + ball_radio, ball_y + ball_radio):
            bloques.remove(bloque)
            ball_vel_y = -ball_vel_y
            break
    
    # Verificar si la pelota cae
    if ball_y > ALTO:
        jugando = False
    
    # Dibujar elementos
    screen.fill(NEGRO)
    pygame.draw.rect(screen, BLANCO, (paddle_x, paddle_y, paddle_ancho, paddle_alto))
    pygame.draw.circle(screen, ROJO, (ball_x, ball_y), ball_radio)
    
    for bloque in bloques:
        pygame.draw.rect(screen, AZUL, bloque)
    
    pygame.display.update()

pygame.quit()
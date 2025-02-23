import pygame
import random

pygame.init()
ventana = pygame.display.set_mode((640, 480))
pygame.display.set_caption("Arkanoid")

# Cargar imágenes
fondo = pygame.image.load("nubes .jpg")
bate = pygame.image.load("huesito.png")
baterect = bate.get_rect()
baterect.move_ip(240, 450)

# Cargar imagen de victoria
winning_image = pygame.image.load("winning.gif")
winning_rect = winning_image.get_rect(center=(320, 240))

# Clase Pelota
class Pelota(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("25x25.png")
        self.rect = self.image.get_rect()
        self.rect.center = (250, 210)
        self.speed = [4, 4]

    def update(self):
        self.rect.x += self.speed[0]
        self.rect.y += self.speed[1]
        if self.rect.left < 0 or self.rect.right > ventana.get_width():
            self.speed[0] = -self.speed[0]
        if self.rect.top < 0:
            self.speed[1] = -self.speed[1]

# Clase Bloque
class Bloque(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        imagenes = ["kinder (1).png", "oreo (1).png", "filipinos.png"]
        self.image = pygame.image.load(random.choice(imagenes))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.resistencia = random.randint(1, 3)  # Algunos bloques requieren más golpes

    def golpeado(self):
        self.resistencia -= 1
        if self.resistencia <= 0:
            self.kill()

# Crear objetos
pelota = Pelota()
todos_sprites = pygame.sprite.Group()
todos_sprites.add(pelota)

bloques = pygame.sprite.Group()
for i in range(8):
    for j in range(5):
        bloque = Bloque(i * 80 + 10, j * 30 + 10)
        bloques.add(bloque)
        todos_sprites.add(bloque)

jugando = True
clock = pygame.time.Clock()
while jugando:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            jugando = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and baterect.left > 0:
        baterect.move_ip(-5, 0)
    if keys[pygame.K_RIGHT] and baterect.right < ventana.get_width():
        baterect.move_ip(5, 0)

    pelota.update()
   
    if baterect.colliderect(pelota.rect):
        pelota.speed[1] = -pelota.speed[1]
   
    bloques_colisionados = pygame.sprite.spritecollide(pelota, bloques, False)
    for bloque in bloques_colisionados:
        pelota.speed[1] = -pelota.speed[1]
        bloque.golpeado()
   
    if len(bloques) == 0:
        ventana.fill((252, 243, 207))
        ventana.blit(winning_image, winning_rect)
        pygame.display.flip()
        pygame.time.delay(2000)
        jugando = False
   
    if pelota.rect.bottom > ventana.get_height():
        jugando = False

    ventana.blit(fondo, (0, 0))  # Dibujar el fondo
    ventana.blit(bate, baterect)
    todos_sprites.draw(ventana)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
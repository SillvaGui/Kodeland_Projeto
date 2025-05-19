import pygame
from pygame import Rect

WIDTH = 800
HEIGHT = 600

# player
player = Rect((100, 500), (40, 40))
player_vel = [0, 0]
on_ground = False

platforms = [
    Rect((0, 580), (800, 20)),
    Rect((200, 450), (120, 20)),
    Rect((400, 350), (120, 20)),
    Rect((600, 250), (120, 20)),
]

GRAVITY = 0.5
JUMP_STRENGTH = -10  # Negativo para pular para cima
MOV_SPEED = 5

def main():
    global on_ground, player_vel
    pygame.init()
    tela = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and on_ground:
                    player_vel[1] = JUMP_STRENGTH

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player.x -= MOV_SPEED
        if keys[pygame.K_RIGHT]:
            player.x += MOV_SPEED

        player_vel[1] += GRAVITY
        player.y += player_vel[1]

        on_ground = False
        for plat in platforms:
            if player.colliderect(plat) and player_vel[1] >= 0:
                player.bottom = plat.top
                player_vel[1] = 0
                on_ground = True

        if player.left < 0:
            player.left = 0
        if player.right > WIDTH:
            player.right = WIDTH
        if player.top > HEIGHT:
            player.topleft = (100, 500)
            player_vel[1] = 0

        tela.fill((0, 0, 0))
        pygame.draw.rect(tela, (0, 120, 255), player)
        for plat in platforms:
            pygame.draw.rect(tela, (0, 200, 0), plat)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
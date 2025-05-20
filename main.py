import os
import random   
import math
import pygame   
from os import listdir
from os.path import isfile, join

pygame.init()

pygame.display.set_caption("Plataformer")

BG_COLOR = (222, 255, 255)
WIDTH, HEIGHT = 1000, 800
FPS = 60
PLAYER_VEL = 5

window = pygame.display.set_mode((WIDTH, HEIGHT))

# Essa função global serve para iniciar o jogo
def main(window):
    clock = pygame.time.Clock()

    # Criação de um loop while, onde ficará em loop contínuo e atuará como nosso loop de eventos
    run = True
    while run:
        clock.tick(FPS)
        # A linha de cima garante que nosso loop while execute por 60 quadros por segundo.

        # Aqui estou criando um evento aonde verifica se o usuário do jogo deseja sair.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

    pygame.quit()
    quit()

# A razão por essa linha aqui é para chamar apenas a função principal
if __name__ == "__main__":
    main(window)

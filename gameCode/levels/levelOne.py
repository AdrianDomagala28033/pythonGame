import pygame
from gameCode.Classes.playerClass import Player
from gameCode.Classes.coinClass import Coin
from gameCode.Classes.groundClass import Ground
from gameCode.Classes.enemyClass import Enemy

pygame.init()


def levelOne(window):
    run = True
    player = Player()
    player.tag = "player"
    clock = 0
    score = 0
    a = 0
    ground = []
    for g in range(26):
        ground.append(Ground(a, 670, pygame.image.load("./images/terrain/ground.PNG")))
        a += 50
    ghost = []
    ghost.append(Enemy(600, 600))
    ghost[0].tag = "enemy"

    while run:
        clock += pygame.time.Clock().tick(60)/1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        keys = pygame.key.get_pressed()

        player.tick(keys, ground)
        ghost[0].tick(player)


        window.fill((0, 204, 255))
        window.blit(pygame.font.Font.render(pygame.font.SysFont("arial", 48), f"Score: {score}", True, (0,0,0)), (1000, 0))
        player.healthBar(window)
        ghost[0].draw(window)
        for g in ground:
            g.draw(window)
        player.draw(window)
        pygame.display.update()
        if(player.health <= 0):
            from gameCode.levels.gameOver import gameOver
            gameOver(window)
            run = False
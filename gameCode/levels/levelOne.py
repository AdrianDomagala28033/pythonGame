import pygame
from gameCode.Classes.playerClass import Player
from gameCode.Classes.coinClass import Coin
from gameCode.Classes.groundClass import Ground
from gameCode.Classes.enemyClass import Enemy
from gameCode.Classes.bowClass import Bow

pygame.init()


def levelOne(window):
    run = True
    player = Player(window)
    player.tag = "player"
    clock = 0
    score = 0
    a = 0
    ground = []
    for g in range(26):
        ground.append(Ground(a, 670, pygame.image.load("./images/terrain/ground.PNG")))
        a += 50
    enemy = []
    enemy.append(Enemy(600, 600, pygame.image.load("./images/enemiesAnimation/ghost.png")))
    enemy.append(Enemy(600, 200, pygame.image.load("./images/enemiesAnimation/ghost.png")))
    for e in enemy:
        e.tag = "enemy"
    while run:
        clock += pygame.time.Clock().tick(60)/1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        keys = pygame.key.get_pressed()

        for e in enemy:
            e.tick(player, e, window)
        window.fill((0, 204, 255))
        window.blit(pygame.font.Font.render(pygame.font.SysFont("arial", 48), f"Score: {score}", True, (0,0,0)), (1000, 0))

        for g in ground:
            g.draw(window)
        player.draw(window)
        player.tick(keys, ground, enemy, window)
        for s in player.distanceWeapon.projectiles:
            s.draw(window)
            s.bulletColision(player, enemy)
        for e in enemy:
            e.draw(window)
        pygame.display.update()
        if(player.health <= 0):
            from gameCode.levels.gameOver import gameOver
            gameOver(window)
            run = False
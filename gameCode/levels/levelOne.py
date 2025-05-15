import pygame

from gameCode.Classes.playerClass import Player
from gameCode.Classes.groundClass import Ground
from gameCode.Classes.enemies.enemyClass import Enemy

from gameCode.Classes.levels.levelClass import Level

pygame.init()


def levelOne(window):
    run = True
    player = Player(window)
    player.tag = "player"
    clock = 0
    score = 0
    a = 0
    ground = []
    potion = []
    potion.append("")

    enemy = []
    enemy.append(Enemy(600, 600, pygame.image.load("./images/enemiesAnimation/ghost.png")))
    enemy.append(Enemy(600, 200, pygame.image.load("./images/enemiesAnimation/ghost.png")))
    level = Level(ground, player, enemy, 50 * 50)
    for g in range(level.levelWidth // 50):
        ground.append(Ground(a, 670, pygame.image.load("./images/terrain/ground.PNG")))
        a += 50
    for e in enemy:
        e.tag = "enemy"
    while run:
        clock += pygame.time.Clock().tick(60)/1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        keys = pygame.key.get_pressed()

        for e in enemy:
            e.tick(player)
        window.fill((0, 204, 255))
        window.blit(pygame.font.Font.render(pygame.font.SysFont("arial", 48), f"Score: {score}", True, (0,0,0)), (1000, 0))

        player.tick(keys, ground, enemy, window, level.cameraX)
        for s in player.distanceWeapon.projectiles:
            s.draw(window)
            s.bulletColision(player, enemy)
        for p in potion:
            pass
            level.update_camera()
            level.update()
            level.draw(window)
        pygame.display.update()
        if(player.health <= 0):
            from gameCode.levels.gameOver import gameOver
            gameOver(window)
            run = False
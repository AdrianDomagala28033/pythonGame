import pygame
from gameCode.Classes.playerClass import Player
from gameCode.Classes.coinClass import Coin
from gameCode.Classes.groundClass import Ground
from gameCode.Classes.enemyClass import Enemy

pygame.init()
window = pygame.display.set_mode((1280, 720))

def main():
    run = True
    player = Player()
    clock = 0
    score = 0
    coins = []
    ground = Ground()
    ghost = Enemy()
    while run:
        clock += pygame.time.Clock().tick(60)/1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        keys = pygame.key.get_pressed()

        if clock >= 2:
            clock = 0
            coins.append(Coin())
        for coin in coins:
            coin.tick()
        player.tick(keys)
        ghost.tick()

        for coin in coins:
            if (player.hitbox.colliderect(coin.hitbox)):
                coins.remove(coin)
                score += 1
        if(player.hitbox.colliderect(ghost.hitbox)):
            player.health -= 10
            ghost.positionY -= 5
            player.positionY = 580
            player.positionX = 0
        window.fill((0, 204, 255))
        window.blit(pygame.font.Font.render(pygame.font.SysFont("arial", 48), f"Score: {score}", True, (0,0,0)), (1100, 0))
        window.blit(pygame.font.Font.render(pygame.font.SysFont("arial", 48), f"Health: {player.health}", True, (0,0,0)), (0, 0))
        for coin in coins:
            coin.draw(window)
        player.draw(window)
        ghost.draw(window)
        ground.draw(window)
        pygame.display.update()
if __name__ == "__main__":
    main()


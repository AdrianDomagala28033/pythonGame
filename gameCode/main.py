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

        player.tick(keys)
        ghost.tick()
        for coin in coins:
            coin.tick()

        for coin in coins:
            if (player.hitbox.colliderect(coin.hitbox)):
                coins.remove(coin)
                score += 1
        if(player.hitbox.colliderect(ghost.hitbox)):
            player.health -= 10
        window.fill((0, 204, 255))
        text_image = pygame.font.Font.render(pygame.font.SysFont("arial", 48), f"Score: {score}", True, (0,0,0))
        text_health = pygame.font.Font.render(pygame.font.SysFont("arial", 48), f"Health: {player.health}", True, (0,0,0))
        window.blit(text_image, (1100, 0))
        window.blit(text_health, (0, 0))
        for coin in coins:
            coin.draw(window)
        player.draw(window)
        ghost.draw(window)
        ground.draw(window)
        pygame.display.update()
    print(score)

if __name__ == "__main__":
    main()


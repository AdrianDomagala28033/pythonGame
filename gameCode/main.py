import pygame
from playerClass import Player
from coinClass import Coin
pygame.init()
window = pygame.display.set_mode((1280, 720))

def main():
    run = True
    player = Player()
    clock = 0
    score = 0
    coins = []
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

        for coin in coins:
            coin.tick()

        for coin in coins:
            if (player.hitbox.colliderect(coin.hitbox)):
                coins.remove(coin)
                score += 1

        window.fill((0, 204, 255))
        for coin in coins:
            coin.draw(window)
        player.draw(window)
        pygame.display.update()
    print(score)

if __name__ == "__main__":
    main()
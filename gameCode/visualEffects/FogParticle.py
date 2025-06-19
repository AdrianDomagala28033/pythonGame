import os

from perlin_noise import PerlinNoise
import numpy as np
import pygame

def create_fog_texture_with_cache(w, h, filename="staticFog.png", scale=80.0, octaves=4, seed=0, use_cached=True):
    if use_cached and os.path.exists(filename):
        print("[mgła] Wczytywanie z cache:", filename)
        return pygame.image.load(filename).convert_alpha()
    print("[mgła] Generowanie nowej tekstury mgły...")
    small_w, small_h = w // 4, h // 4
    noise = PerlinNoise(octaves=octaves, seed=seed)
    fog_array = np.zeros((small_h, small_w, 4), dtype=np.uint8)

    for y in range(small_h):
        for x in range(small_w):
            nx = x / scale
            ny = y / scale
            val = noise([nx, ny])
            val = (val + 1) / 2
            alpha = int(val * 150)
            fog_array[y, x] = [200, 200, 200, alpha]

    surface = pygame.image.frombuffer(fog_array.flatten(), (small_w, small_h), "RGBA").convert_alpha()
    full_surface = pygame.transform.smoothscale(surface, (w, h))

    # Zapisz do pliku PNG
    pygame.image.save(full_surface, filename)
    print("[mgła] Zapisano teksturę mgły do pliku:", filename)

    return full_surface


def generate_dungeon_wall_texture(width, height, brick_size=16, base_color=(30, 20, 10), noise_strength=10, seed=0):
    np.random.seed(seed)
    surface = pygame.Surface((width, height))
    surface.fill(base_color)

    for y in range(0, height, brick_size):
        offset = (y // brick_size) % 2 * (brick_size // 2)
        for x in range(-offset, width, brick_size):
            brightness = np.random.randint(-noise_strength, noise_strength)
            color = (
                max(0, min(255, base_color[0] + brightness)),
                max(0, min(255, base_color[1] + brightness)),
                max(0, min(255, base_color[2] + brightness)),
            )
            brick_rect = pygame.Rect(x, y, brick_size, brick_size)
            pygame.draw.rect(surface, color, brick_rect)
            pygame.draw.rect(surface, (10, 10, 10), brick_rect, width=1)  # fuga

    return surface





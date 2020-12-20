import pygame
import os


pygame.init()
SIZE = WIDTH, HEIGHT = 1500, 700
screen = pygame.display.set_mode(SIZE)


def load_image(directory, name, color_key=None):
    fullname = os.path.join(directory, name)
    try:
        image = pygame.image.load(fullname).convert()
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)
    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()
    return image


def load_back_ground(directory, name):
    back_ground_sprite = load_image(directory, name)
    back_ground_surface = pygame.Surface(SIZE, pygame.SRCALPHA, 32)
    sprite_height = back_ground_sprite.get_height()
    sprite_width = back_ground_sprite.get_width()
    for y in range(0, (HEIGHT + sprite_height - 1) // sprite_height):
        for x in range(0, (WIDTH + sprite_width - 1) // sprite_width):
            back_ground_surface.blit(back_ground_sprite, (x * sprite_width, y * sprite_height))
    screen.blit(back_ground_surface, (0, 0))
    pygame.display.flip()


if __name__ == '__main__':
    running = True
    load_back_ground('Sprites/Background', 'Blue.png')
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        pygame.display.flip()
    pygame.quit()

import pygame
import os

print(1)

pygame.init()
SIZE = WIDTH, HEIGHT = 1500, 700
FPS = 60
MOVE_SPEED = 5
JUMP_POWER = 10
GRAVITY = 0.25
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption("Fruit Ninja 2.0")
clock = pygame.time.Clock()


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


hero_sprite = load_image('Sprites/MainCharacters/Ninja Frog', 'idle.png', -1)
grass_platform_image = load_image('Sprites/Terrain', 'grass.png')
all_sprites = pygame.sprite.Group()
hero_group = pygame.sprite.Group()
platforms_group = pygame.sprite.Group()
fruits_group = pygame.sprite.Group()
evil_dudes_group = pygame.sprite.Group()


def terminate():
    pygame.quit()
    exit()


class Platform(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__(all_sprites, platforms_group)
        self.image = grass_platform_image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x, self.rect.y = pos


class MainCharacter(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__(all_sprites, hero_group)
        self.image = hero_sprite
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x, self.rect.y = pos
        self.vx = 0
        self.vy = 0
        self.is_on_the_floor = False
        
    def update(self, left, right, up):
        if up:
            if self.is_on_the_floor:
                self.vy = -JUMP_POWER
        if left:
            self.vx = -MOVE_SPEED
        if right:
            self.vx = MOVE_SPEED
        if not (left or right):
            self.vx = 0
        if not self.is_on_the_floor:
            self.vy += GRAVITY
        self.is_on_the_floor = False
        self.rect.y += self.vy
        self.collide()
        self.rect.x += self.vx
        self.collide()

    def collide(self):
        for p in platforms_group:
            if pygame.sprite.collide_mask(self, p):
                if self.rect.bottom < p.rect.top:
                    if self.vx > 0:
                        self.rect.right = p.rect.left
                    if self.vx < 0:
                        self.rect.left = p.rect.right
                if self.vy > 0:
                    if p.rect.top + 20 >= self.rect.bottom >= p.rect.top:
                        self.rect.bottom = p.rect.top
                        self.is_on_the_floor = True
                        self.vy = 0
                    else:
                        self.vx = 0
                if self.vy < 0:
                    if p.rect.bottom - 20 <= self.rect.top <= p.rect.bottom:
                        self.rect.top = p.rect.bottom
                        self.vy = 0
                    else:
                        self.vx = 0
    

def load_menu():
    # Добавление интерфейса меню
    pygame.display.flip()
    while True:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                terminate()
            elif ev.type == pygame.KEYDOWN or ev.type == pygame.MOUSEBUTTONDOWN:
                return


def load_back_ground(directory, name):
    back_ground_sprite = load_image(directory, name)
    back_ground_surface = pygame.Surface(SIZE, pygame.SRCALPHA, 32)
    sprite_height = back_ground_sprite.get_height()
    sprite_width = back_ground_sprite.get_width()
    for y in range(0, (HEIGHT + sprite_height - 1) // sprite_height):
        for x in range(0, (WIDTH + sprite_width - 1) // sprite_width):
            back_ground_surface.blit(back_ground_sprite, (x * sprite_width, y * sprite_height))
    return back_ground_surface


if __name__ == '__main__':
    running = True
    background = load_back_ground('Sprites/Background', 'Blue.png')
    screen.blit(background, (0, 0))
    left, right, up = False, False, False
    hero = MainCharacter((100, 100))
    Platform((150, 300))
    for x in range(28):
        Platform((x * 50, 500))
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    left = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    right = True
            if event.type == pygame.KEYUP and event.key == pygame.K_RIGHT:
                right = False
            if event.type == pygame.KEYUP and event.key == pygame.K_LEFT:
                left = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                up = True
            if event.type == pygame.KEYUP and event.key == pygame.K_UP:
                up = False
        pygame.display.flip()
        screen.blit(background, (0, 0))
        platforms_group.draw(screen)
        hero_group.draw(screen)
        hero.update(left, right, up)
        clock.tick(FPS)
    pygame.quit()

# Импорт нужных библиотек
import pygame
import os
import random

# Инициализация pygame, создание окна и определение констант
pygame.init()
SIZE = WIDTH, HEIGHT = 800, 600
FPS = 60
MOVE_SPEED = 4
JUMP_POWER = 9
GRAVITY = 0.3
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption("Fruit Ninja 2.0")
clock = pygame.time.Clock()


# Загрузка картинки

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


# Спрайты героя
hero_standing_sheet = load_image('Sprites/MainCharacters/Ninja Frog', 'idle.png', -1)
hero_running_sheet = load_image('Sprites/MainCharacters/Ninja Frog', 'Run.png', -1)
hero_falling_sheet = load_image('Sprites/MainCharacters/Ninja Frog', 'Fall.png', -1)
hero_jumping_sheet = load_image('Sprites/MainCharacters/Ninja Frog', 'Jump.png', -1)
hero_lstanding_sheet = load_image('Sprites/MainCharacters/Ninja Frog', 'idle_left.png', -1)
hero_lrunning_sheet = load_image('Sprites/MainCharacters/Ninja Frog', 'run_left.png', -1)
hero_lfalling_sheet = load_image('Sprites/MainCharacters/Ninja Frog', 'fall_left.png', -1)
hero_ljumping_sheet = load_image('Sprites/MainCharacters/Ninja Frog', 'jump_left.png', -1)

# Спрайты противников
mushroom_running_right_sheet = load_image('Sprites/Enemies/Mushroom', 'Run_right.png', -1)
mushroom_running_left_sheet = load_image('Sprites/Enemies/Mushroom', 'Run.png', -1)

# Словарь картинок для фруктов
fruit_images = {
    'apple': load_image('Sprites/Items/Fruits', 'Apple.png', -1),
    'banana': load_image('Sprites/Items/Fruits', 'Bananas.png', -1),
    'melon': load_image('Sprites/Items/Fruits', 'Melon.png', -1),
    'strawberry': load_image('Sprites/Items/Fruits', 'Strawberry.png', -1)}
# Словарь картинок для природных объектов
platform_images = {
    'grass': load_image('Sprites/Terrain', 'grass.png'),
    'black_grass': load_image('Sprites/Terrain', 'black_grass.png'),
    'white_grass': load_image('Sprites/Terrain', 'white_grass.png'),
    'g_brown_stone': load_image('Sprites/Terrain/brown_stone', '1.png'),
    'v_brown_stone': load_image('Sprites/Terrain/brown_stone', '2.png'),
    'g_gold_stone': load_image('Sprites/Terrain/gold_stone', '1.png'),
    'v_gold_stone': load_image('Sprites/Terrain/gold_stone', '2.png'),
    'g_gray_stone': load_image('Sprites/Terrain/gray_stone', '1.png'),
    'v_gray_stone': load_image('Sprites/Terrain/gray_stone', '2.png'),
    'g_orange_stone': load_image('Sprites/Terrain/orange_stone', '1.png'),
    'v_orange_stone': load_image('Sprites/Terrain/orange_stone', '2.png')}
# Создание всех груп спрайтов
mushroom_group = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
hero_group = pygame.sprite.Group()
fruit_group = pygame.sprite.Group()
platforms_group = pygame.sprite.Group()
evil_dudes_group = pygame.sprite.Group()
bg_group = pygame.sprite.Group()


# Функция выхода из программы
def terminate():
    pygame.quit()
    exit()


# Класс 'Грибы-Убийцы'
class Mushroom(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__(all_sprites, mushroom_group)
        self.frame = []
        self.pos = pos
        self.sheet = mushroom_running_left_sheet
        self.cut_sheets(self.sheet, 16, 1)
        self.cur_frame = 0
        self.image = self.frame[self.cur_frame]
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x, self.rect.y = pos
        self.vx = 0
        self.vy = 0
        self.collide_fl = 0
        self.left = True
        self.is_on_the_floor = False
        self.temp = 0
        self.empty = []

    def hero_collide(self, obj):
        if pygame.sprite.collide_mask(self, obj):
            terminate()

    def cut_sheets(self, sheet, columns, rows):
        self.frame.clear()
        if not hasattr(self, 'rect'):
            self.rect = pygame.Rect(self.pos[0], self.pos[1], sheet.get_width() // columns,
                                    sheet.get_height() // rows)
        else:
            self.rect = pygame.Rect(self.rect.x, self.rect.y, sheet.get_width() // columns,
                                    sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_coords = (self.rect.w * i, self.rect.h * j)
                self.frame.append(sheet.subsurface(pygame.Rect(frame_coords, self.rect.size)))

    def update_animation(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frame)
        self.image = self.frame[self.cur_frame]

    def run(self):
        if self.vx == 0 and self.left:
            self.change_sheet(mushroom_running_right_sheet, 16, 1)
            self.left = False
        elif self.vx == 0 and not self.left:
            self.change_sheet(mushroom_running_left_sheet, 16, 1)
            self.left = True
        if self.collide_fl != 1 and self.left:
            self.vx = -MOVE_SPEED
        if self.collide_fl != 2 and not self.left:
            self.vx = MOVE_SPEED
        if not self.is_on_the_floor:
            self.vy += GRAVITY
        self.is_on_the_floor = False
        self.rect.y += self.vy
        self.collide(0, self.vy)
        self.rect.x += self.vx
        self.collide(self.vx, 0)
        self.collide_fl = 0

    def collide(self, x, y):
        for p in platforms_group:
            if pygame.sprite.collide_mask(self, p):
                if self.rect.bottom - 5 > p.rect.top:
                    if x > 0:
                        self.rect.right = p.rect.left + 2
                    elif x < 0:
                        self.rect.left = p.rect.right - 1
                    self.vx = 0
                else:
                    self.collide_fl = 0
                if y > 0:
                    if p.rect.top + 20 >= self.rect.bottom >= p.rect.top:
                        self.rect.bottom = p.rect.top + 1
                        self.is_on_the_floor = True
                        self.vy = 0
                    else:
                        self.vx = 0
                if y < 0:
                    if p.rect.bottom - 20 <= self.rect.top <= p.rect.bottom:
                        self.rect.top = p.rect.bottom - 1
                        self.vy = 0
                    else:
                        self.vx = 0

    def change_sheet(self, new_sheet, cols, rows):
        self.sheet = new_sheet
        self.cut_sheets(self.sheet, cols, rows)
        self.cur_frame = 0
        self.image = self.frame[self.cur_frame]


# Класс фруктов
class Fruit(pygame.sprite.Sprite):
    def __init__(self, pos, pic):
        super().__init__(fruit_group, all_sprites)
        self.sheet = fruit_images[pic]
        self.name = pic
        self.pos = pos
        self.frame = []
        self.cur_frame = 0
        self.cut_sheets(self.sheet, 17, 1)
        self.image = self.frame[self.cur_frame]
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x, self.rect.y = pos

    def cut_sheets(self, sheet, columns, rows):
        self.rect = pygame.Rect(self.pos[0], self.pos[1], sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_coords = (self.rect.w * i, self.rect.h * j)
                self.frame.append(sheet.subsurface(pygame.Rect(frame_coords, self.rect.size)))

    def update_animation(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frame)
        self.image = self.frame[self.cur_frame]

    def collide(self, obj):
        if pygame.sprite.collide_mask(obj, self):
            if self.name == 'apple':
                obj.apple_counter += 1
            if self.name == 'banana':
                obj.banana_counter += 1
            if self.name == 'apple':
                obj.melon_counter += 1
            if self.name == 'apple':
                obj.strawberry_counter += 1
            self.kill()


# Класс платформ
class Platform(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(platforms_group, all_sprites)
        self.image = platform_images[tile_type]
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = pos_x, pos_y


class Background(pygame.sprite.Sprite):
    def __init__(self, pic):
        super().__init__(bg_group, all_sprites)
        self.image = pic
        self.rect = self.image.get_rect()
        self.rect.x = -300
        self.rect.y = -600


# Класс персонажа
class MainCharacter(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__(all_sprites, hero_group)
        self.frame = []
        self.pos = pos
        self.sheet = hero_standing_sheet
        self.cut_sheets(self.sheet, 11, 1, 0)
        self.cur_frame = 0
        self.image = self.frame[self.cur_frame]
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x, self.rect.y = pos
        self.vx = 0
        self.vy = 0
        self.collide_fl = 0
        self.apple_counter = 0
        self.banana_counter = 0
        self.melon_counter = 0
        self.strawberry_counter = 0
        self.is_on_the_floor = False

    def cut_sheets(self, sheet, columns, rows, num):
        self.frame.clear()
        if not hasattr(self, 'rect'):
            self.rect = pygame.Rect(self.pos[0], self.pos[1], sheet.get_width() // columns,
                                    sheet.get_height() // rows)
        else:
            self.rect = pygame.Rect(self.rect.x, self.rect.y + num, sheet.get_width() // columns,
                                    sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_coords = (self.rect.w * i, self.rect.h * j)
                self.frame.append(sheet.subsurface(pygame.Rect(frame_coords, self.rect.size)))

    def update_animation(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frame)
        self.image = self.frame[self.cur_frame]

    def update(self, left, right, up):
        if up:
            if self.is_on_the_floor:
                self.vy = -JUMP_POWER
        if left and self.collide_fl != 1:
            self.vx = -MOVE_SPEED
        if right and self.collide_fl != 2:
            self.vx = MOVE_SPEED
        if not (left or right):
            self.collide_fl = 0
            self.vx = 0
        if not self.is_on_the_floor:
            self.vy += GRAVITY
        self.is_on_the_floor = False
        self.rect.y += self.vy
        self.collide(0, self.vy)
        self.rect.x += self.vx
        self.collide(self.vx, 0)
        if self.vx == 0 and self.vy == 0:
            if self.sheet == hero_lfalling_sheet or self.sheet == hero_lrunning_sheet:
                self.change_sheet(hero_lstanding_sheet, 11, 1, 2)
                self.vx = 0
            if self.sheet == hero_falling_sheet or self.sheet == hero_running_sheet:
                self.change_sheet(hero_standing_sheet, 11, 1, 2)
                self.vx = 0
        else:
            if self.vy > 0:
                if self.vx > 0 or self.sheet == hero_jumping_sheet:
                    self.change_sheet(hero_falling_sheet, 1, 1)
                if self.vx < 0 or self.sheet == hero_ljumping_sheet:
                    self.change_sheet(hero_lfalling_sheet, 1, 1)
            elif self.vy < 0:
                if (self.sheet == hero_running_sheet or self.sheet == hero_standing_sheet or
                        self.vx > 0):
                    self.change_sheet(hero_jumping_sheet, 1, 1)
                if (self.sheet == hero_lrunning_sheet or self.sheet == hero_lstanding_sheet or
                        self.vx < 0):
                    self.change_sheet(hero_ljumping_sheet, 1, 1)
            elif self.vy == 0 and self.vx > 0 and self.collide_fl != 1:
                if (self.sheet == hero_standing_sheet or self.sheet == hero_falling_sheet or
                        self.sheet == hero_lstanding_sheet or self.sheet == hero_lfalling_sheet or
                        self.sheet == hero_lrunning_sheet):
                    self.change_sheet(hero_running_sheet, 12, 1)
            elif self.vy == 0 and self.vx < 0 and self.collide_fl != 2:
                if (self.sheet == hero_lstanding_sheet or self.sheet == hero_lfalling_sheet or
                        self.sheet == hero_standing_sheet or self.sheet == hero_falling_sheet or
                        self.sheet == hero_running_sheet):
                    self.change_sheet(hero_lrunning_sheet, 12, 1)
        self.collide(self.vx, 0)
        self.collide_fl = 0

    def collide(self, x, y):
        for p in platforms_group:
            if pygame.sprite.collide_mask(self, p):
                if self.rect.bottom - 5 > p.rect.top:
                    if x > 0:
                        self.rect.right = p.rect.left + 2
                    elif x < 0:
                        self.rect.left = p.rect.right - 1
                    self.vx = 0
                else:
                    self.collide_fl = 0
                if y > 0:
                    if p.rect.top + 20 >= self.rect.bottom >= p.rect.top:
                        self.rect.bottom = p.rect.top + 1
                        self.is_on_the_floor = True
                        self.vy = 0
                    else:
                        self.vx = 0
                if y < 0:
                    if p.rect.bottom - 20 <= self.rect.top <= p.rect.bottom:
                        self.rect.top = p.rect.bottom - 1
                        self.vy = 0
                    else:
                        self.vx = 0

    def change_sheet(self, new_sheet, cols, rows, num=0):
        self.sheet = new_sheet
        self.cut_sheets(self.sheet, cols, rows, num)
        self.cur_frame = 0
        self.image = self.frame[self.cur_frame]


# Класс камеры
class Camera:
    def __init__(self, field_size):
        self.dx = 0
        self.dy = 0
        self.field_size = field_size

    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    def update(self, target):
        self.dx = -(target.rect.x + target.rect.width // 2 - WIDTH // 2)
        self.dy = -(target.rect.y + target.rect.height // 2 - HEIGHT // 2)


# Функция для загрузки меню
def load_menu():
    menu = load_image('Sprites/Terrain', 'menu.png')
    button = load_image('Sprites/Terrain', 'button_pressed.png', -1)
    screen.blit(menu, (0, 0))
    pygame.display.flip()
    fl = 0
    while True:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                terminate()
            elif ev.type == pygame.MOUSEBUTTONDOWN:
                if 487 >= ev.pos[0] >= 312 and 357 >= ev.pos[1] >= 281:
                    screen.blit(button, (312, 281))
                    pygame.display.flip()
                    fl = 1
            elif ev.type == pygame.MOUSEBUTTONUP:
                if fl:
                    return


# Функция для загрузки уровня из текстового файла
def load_level(filename):
    filename = 'levels/' + filename
    with open(filename, 'r') as map_file:
        level_map = [line.strip() for line in map_file]
        max_width = max(map(len, level_map))
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


# Функция для загрузки заднего фона
def load_back_ground(directory, name):
    back_ground_sprite = load_image(directory, name)
    back_ground_surface = pygame.Surface((WIDTH * 20, HEIGHT * 20), pygame.SRCALPHA, 32)
    sprite_height = back_ground_sprite.get_height()
    sprite_width = back_ground_sprite.get_width()
    for y in range(((HEIGHT + sprite_height - 1) // sprite_height) * 3):
        for x in range(((WIDTH + sprite_width - 1) // sprite_width + 10) * 3):
            back_ground_surface.blit(back_ground_sprite, (x * sprite_width, y * sprite_height))
    return back_ground_surface


# Создание всех объектов, главный игровой цикл и отслеживание всех событий в игре
if __name__ == '__main__':
    load_menu()
    running = True
    fruits = ['apple', 'banana', 'melon', 'strawberry']
    background = load_back_ground('Sprites/Background', 'Blue.png')
    Background(background)
    left, right, up = False, False, False
    Mushroom((600, 250))
    hero = MainCharacter((100, 100))
    for i in range(23):
        Platform('grass', i * 48, 300)
    Platform('grass', 288, 252)
    Platform('grass', 800, 252)
    for i in range(23):
        Fruit((i * 30, 200), random.choice(fruits))
    camera = Camera((hero.rect.x, hero.rect.y))
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
        screen.fill((0, 0, 0))
        camera.update(hero)
        for sprite in all_sprites:
            camera.apply(sprite)
        bg_group.draw(screen)
        platforms_group.draw(screen)
        fruit_group.draw(screen)
        hero_group.draw(screen)
        hero.update(left, right, up)
        hero.update_animation()
        mushroom_group.draw(screen)
        for mush in mushroom_group:
            mush.update_animation()
            mush.run()
            mush.hero_collide(hero)
        for fruit in fruit_group:
            fruit.update_animation()
            fruit.collide(hero)
        clock.tick(FPS)
    pygame.quit()

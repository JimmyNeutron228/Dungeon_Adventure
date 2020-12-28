# Импорт нужных библиотек
import pygame
import os

# Инициализация pygame, создание окна и определение констант
pygame.init()
SIZE = WIDTH, HEIGHT = 800, 600
FPS = 60
MOVE_SPEED = 5
JUMP_POWER = 10
GRAVITY = 0.25
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
all_sprites = pygame.sprite.Group()
hero_group = pygame.sprite.Group()
fruit_group = pygame.sprite.Group()
platforms_group = pygame.sprite.Group()
evil_dudes_group = pygame.sprite.Group()


# Функция выхода из программы
def terminate():
    pygame.quit()
    exit()


# Класс яблок
class Apple(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__(all_sprites, fruit_group)
        self.frame = []
        self.sheet = fruit_images['apple']
        self.pos = pos
        self.cut_sheets(self.sheet, 17, 1)
        self.cur_frame = 0
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
            obj.apple_counter += 1
            self.kill()


# Класс бананов
class Banana(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__(all_sprites, fruit_group)
        self.frame = []
        self.sheet = fruit_images['banana']
        self.pos = pos
        self.cut_sheets(self.sheet, 17, 1)
        self.cur_frame = 0
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
            obj.banana_counter += 1
            self.kill()


# Класс арбузов
class Melon(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__(all_sprites, fruit_group)
        self.frame = []
        self.sheet = fruit_images['melon']
        self.pos = pos
        self.cut_sheets(self.sheet, 17, 1)
        self.cur_frame = 0
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
            obj.melon_counter += 1
            self.kill()


# Класс клубничек
class Strawberry(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__(all_sprites, fruit_group)
        self.frame = []
        self.sheet = fruit_images['strawberry']
        self.pos = pos
        self.cut_sheets(self.sheet, 17, 1)
        self.cur_frame = 0
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
            obj.strawberry_counter += 1
            self.kill()


# Класс платформ
class Platform(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(platforms_group, all_sprites)
        self.image = platform_images[tile_type]
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = pos_x * 48, pos_y * 48


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
        if not self.sheet == hero_running_sheet:
            self.collide()
        if self.vx == 0 and self.vy == 0:
            if self.sheet == hero_lfalling_sheet or self.sheet == hero_lrunning_sheet:
                self.change_sheet(hero_lstanding_sheet, 11, 1, 2)
            if self.sheet == hero_falling_sheet or self.sheet == hero_running_sheet:
                self.change_sheet(hero_standing_sheet, 11, 1, 2)
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
            elif self.vy == 0 and self.vx > 0:
                if (self.sheet == hero_standing_sheet or self.sheet == hero_falling_sheet or
                        self.sheet == hero_lstanding_sheet or self.sheet == hero_lfalling_sheet or
                        self.sheet == hero_lrunning_sheet):
                    self.change_sheet(hero_running_sheet, 12, 1)
            elif self.vy == 0 and self.vx < 0:
                if (self.sheet == hero_lstanding_sheet or self.sheet == hero_lfalling_sheet or
                        self.sheet == hero_standing_sheet or self.sheet == hero_falling_sheet or
                        self.sheet == hero_running_sheet):
                    self.change_sheet(hero_lrunning_sheet, 12, 1)
        self.collide()
    
    def collide(self):
        fl = 0
        for p in platforms_group:
            if pygame.sprite.collide_mask(self, p):
                if self.rect.bottom < p.rect.top:
                    if self.vx > 0:
                        self.rect.right = p.rect.left
                    if self.vx < 0:
                        self.rect.left = p.rect.right
                    fl = 1
                if not fl:
                    if self.vy > 0:
                        if p.rect.top + 20 >= self.rect.bottom >= p.rect.top:
                            self.rect.bottom = p.rect.top + 1
                            self.is_on_the_floor = True
                            self.vy = 0
                        else:
                            self.vx = 0
                    if self.vy < 0:
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
    # Добавление интерфейса меню
    pygame.display.flip()
    while True:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                terminate()
            elif ev.type == pygame.KEYDOWN or ev.type == pygame.MOUSEBUTTONDOWN:
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
    back_ground_surface = pygame.Surface(SIZE, pygame.SRCALPHA, 32)
    sprite_height = back_ground_sprite.get_height()
    sprite_width = back_ground_sprite.get_width()
    for y in range(0, (HEIGHT + sprite_height - 1) // sprite_height):
        for x in range(0, (WIDTH + sprite_width - 1) // sprite_width):
            back_ground_surface.blit(back_ground_sprite, (x * sprite_width, y * sprite_height))
    return back_ground_surface


# Создание всех объектов, главный игровой цикл и отслеживание всех событий в игре
if __name__ == '__main__':
    running = True
    background = load_back_ground('Sprites/Background', 'Blue.png')
    screen.blit(background, (0, 0))
    left, right, up = False, False, False
    hero = MainCharacter((100, 100))
    for i in range(23):
        Platform('grass', i, 300 // 48)
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
        camera.update(hero)
        for sprite in all_sprites:
            camera.apply(sprite)
        screen.blit(background, (0, 0))
        platforms_group.draw(screen)
        fruit_group.draw(screen)
        hero_group.draw(screen)
        hero.update(left, right, up)
        hero.update_animation()
        for fruit in fruit_group:
            fruit.update_animation()
            fruit.collide(hero)
        clock.tick(FPS)
    pygame.quit()

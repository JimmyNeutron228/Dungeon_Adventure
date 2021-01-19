# Импорт нужных библиотек
import pygame
import os
import random
import time

# Инициализация pygame, создание окна и определение констант
pygame.init()
SIZE = WIDTH, HEIGHT = 800, 600
FPS = 60
MOVE_SPEED = 4
JUMP_POWER = 7
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
hitted_hero_sheet = load_image('Sprites/MainCharacters/Ninja Frog', 'hitted_hero.png', -1)

# Спрайты противников
mushroom_running_right_sheet = load_image('Sprites/Enemies/Mushroom', 'Run_right.png', -1)
mushroom_running_left_sheet = load_image('Sprites/Enemies/Mushroom', 'Run.png', -1)
plant_idle_sheet = load_image('Sprites/Enemies/Plant', 'Idle.png', -1)
plant_bullet_sheet = load_image('Sprites/Enemies/Plant', 'Bullet.png', -1)

# Словарь картинок для фруктов
fruit_images = {
    'apple': load_image('Sprites/Items/Fruits', 'Apple.png', -1),
    'banana': load_image('Sprites/Items/Fruits', 'Bananas.png', -1),
    'melon': load_image('Sprites/Items/Fruits', 'Melon.png', -1),
    'strawberry': load_image('Sprites/Items/Fruits', 'Strawberry.png', -1)}

# Словарь картинок для ловушек
traps_images = {
    'spikes': load_image('Sprites/Traps/Spikes', 'Idle.png', -1)}
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

return_to_menu_white = load_image('Sprites/Menu/Buttons', 'white_menu_button.png', -1)
return_to_menu_black = load_image('Sprites/Menu/Buttons', 'black_menu_button.png', -1)
return_to_play_white = load_image('Sprites/Menu/Buttons', 'white_return_button.png', -1)
return_to_play_black = load_image('Sprites/Menu/Buttons', 'black_return_button.png', -1)
black_next_level = load_image('Sprites/Menu/Buttons', 'white_nextlevel_button.png', -1)
white_next_level = load_image('Sprites/Menu/Buttons', 'black_nextlevel_button.png', -1)

start_point_sheet = load_image('Sprites/Items/Checkpoints/Start', 'start.png', -1)
finish_point_sheet = load_image('Sprites/Items/Checkpoints/End', 'finish.png', -1)

# Создание всех груп спрайтов
mushroom_group = pygame.sprite.Group()
plant_group = pygame.sprite.Group()
plant_bullet_group = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
hero_group = pygame.sprite.Group()
fruit_group = pygame.sprite.Group()
traps_group = pygame.sprite.Group()
platforms_group = pygame.sprite.Group()
evil_dudes_group = pygame.sprite.Group()
bg_group = pygame.sprite.Group()
start_point_group = pygame.sprite.Group()
finish_point_group = pygame.sprite.Group()


# Функция выхода из программы
def terminate():
    pygame.quit()
    exit()


# Класс Шарик
class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__(all_sprites, plant_bullet_group)
        self.pos = pos
        self.image = plant_bullet_sheet
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x, self.rect.y = pos

    def collide(self):
        for p in platforms_group:
            if pygame.sprite.collide_mask(self, p):
                self.kill()

    def fly(self):
        if self.rect.x == -16:
            self.kill()
        else:
            self.rect.x -= 5

    def hero_collide(self, obj):
        if pygame.sprite.collide_mask(self, obj) and obj.death is False and obj.finish is False:
            self.kill()
            obj.death = True
            obj.game_over()


# Класс 'Цветы'
class Plant(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__(all_sprites, plant_group)
        self.pos = pos
        self.frame = []
        self.sheet = plant_idle_sheet
        self.cut_sheets(self.sheet, 1, 1)
        self.cur_frame = 0
        self.image = self.frame[self.cur_frame]
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x, self.rect.y = pos
        self.shoot_time = time.monotonic()
        self.death = False
        self.up_anim_time = time.monotonic()

    def shoot(self):
        if not self.death:
            if self.shoot_time + 3 <= time.monotonic():
                self.shoot_time = time.monotonic()
                poss = (self.rect.x + 5, self.rect.y + 10)
                Bullet(poss)

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
        if self.up_anim_time + 0.03 <= time.monotonic():
            self.up_anim_time = time.monotonic()
            self.cur_frame = (self.cur_frame + 1) % len(self.frame)
            self.image = self.frame[self.cur_frame]

    def is_death(self, obj):
        if pygame.sprite.collide_mask(self, obj) and self.rect.bottom >= obj.rect.top - 5:
            self.kill()

    def hero_collide(self, obj):
        if pygame.sprite.collide_mask(self, obj) and obj.death is False:
            obj.death = True
            obj.game_over()


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
        self.up_anim_time = time.monotonic()
        
    
    def is_death(self, obj):
        if (pygame.sprite.collide_mask(self, obj) and self.rect.bottom >= obj.rect.top - 20 and
                obj.death is False):
            self.kill()
    
    def hero_collide(self, obj):
        if pygame.sprite.collide_mask(self, obj) and obj.death is False:
            obj.death = True
            obj.game_over()
    
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
        if self.up_anim_time + 0.03 <= time.monotonic():
            self.up_anim_time = time.monotonic()
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
                        pass
    
    def change_sheet(self, new_sheet, cols, rows):
        self.sheet = new_sheet
        self.cut_sheets(self.sheet, cols, rows)
        self.cur_frame = 0
        self.image = self.frame[self.cur_frame]
        self.vx = 0


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
        self.up_anim_time = time.monotonic()
    
    def cut_sheets(self, sheet, columns, rows):
        self.rect = pygame.Rect(self.pos[0], self.pos[1], sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_coords = (self.rect.w * i, self.rect.h * j)
                self.frame.append(sheet.subsurface(pygame.Rect(frame_coords, self.rect.size)))
    
    def update_animation(self):
        if self.up_anim_time + 0.03 <= time.monotonic():
            self.up_anim_time = time.monotonic()
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
        

def game_over_sign(k):
    font = pygame.font.Font(None, 100)
    text = font.render("GAME OVER", True, (0, 0, 0))
    text_x = WIDTH // 2 - text.get_width() // 2
    text_y = HEIGHT // 2 - text.get_height() // 2
    ans1 = (text, text_x, text_y - 140)
    if not k:
        return ans1
    text = font.render("GAME OVER", True, (240, 240, 240))
    text_x = WIDTH // 2 - text.get_width() // 2
    text_y = HEIGHT // 2 - text.get_height() // 2
    ans2 = (text, text_x, text_y - 140)
    return ans2


def some_finish_word(word, k):
    font = pygame.font.Font(None, 100)
    text = font.render(word, True, (0, 0, 0))
    text_x = WIDTH // 2 - text.get_width() // 2
    text_y = HEIGHT // 2 - text.get_height() // 2
    ans1 = (text, text_x, text_y - 140)
    if not k:
        return ans1
    text = font.render(word, True, (240, 240, 240))
    text_x = WIDTH // 2 - text.get_width() // 2
    text_y = HEIGHT // 2 - text.get_height() // 2
    ans2 = (text, text_x, text_y - 140)
    return ans2


# Класс платформ
class Platform(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(platforms_group, all_sprites)
        self.image = platform_images[tile_type]
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = pos_x, pos_y


# Класс шипов
class Traps(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(traps_group, all_sprites)
        self.image = traps_images[tile_type]
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = pos_x, pos_y

    def hero_collide(self, obj):
        if pygame.sprite.collide_mask(self, obj) and obj.death is False:
            obj.game_over()


# Класс шипов
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
        self.can_jump = False
        self.finish_fl = 0
        self.can_double_jump = False
        self.is_on_the_floor = False
        self.death = False
        self.finish = False
        self.up_anim_time = time.monotonic()
    
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
        if self.up_anim_time + 0.03 <= time.monotonic():
            self.up_anim_time = time.monotonic()
            self.cur_frame = (self.cur_frame + 1) % len(self.frame)
            self.image = self.frame[self.cur_frame]
    
    def update(self, left, right, up):
        if not self.death and not self.finish:
            if up:
                self.jump()
            if left and self.collide_fl != 1:
                self.vx = -MOVE_SPEED
            if right and self.collide_fl != 2:
                self.vx = MOVE_SPEED
            if not (left or right):
                self.collide_fl = 0
                self.vx = 0
        if self.finish:
            self.vx = 0
        if not self.is_on_the_floor:
            self.vy += GRAVITY
        self.is_on_the_floor = False
        self.rect.y += self.vy
        if not self.death:
            self.collide(0, self.vy)
        self.rect.x += self.vx
        if not self.death:
            self.collide(self.vx, 0)
        if not self.death and not self.finish:
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
                            self.vx > 0 or self.sheet == hero_falling_sheet):
                        self.change_sheet(hero_jumping_sheet, 1, 1)
                    if (self.sheet == hero_lrunning_sheet or self.sheet == hero_lstanding_sheet or
                            self.vx < 0 or self.sheet == hero_lfalling_sheet):
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
            if self.is_on_the_floor:
                self.can_jump = True
                self.can_double_jump = True
        else:
            if self.death:
                self.change_sheet(hitted_hero_sheet, 1, 1)
            if self.finish and not self.finish_fl:
                self.change_sheet(hero_standing_sheet, 11, 1, 2)
                self.finish_fl = 1
        if self.rect.top > HEIGHT:
            self.kill()
    
    def jump(self):
        if self.can_jump:
            self.can_jump = False
            self.vy = -JUMP_POWER
        elif self.can_double_jump:
            self.can_double_jump = False
            self.vy = -JUMP_POWER
    
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

    def game_over(self):
        self.vx = random.choice([-1, 1]) * 3
        self.vy = -5
        self.death = True


class FinishPlatform(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__(all_sprites, finish_point_group)
        self.frame = []
        self.pos = pos
        self.sheet = finish_point_sheet
        self.cut_sheets(self.sheet, 10, 1, 0)
        self.cur_frame = 0
        self.image = self.frame[self.cur_frame]
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x, self.rect.y = pos
        self.up_anim_time = time.monotonic()
    
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
        if self.up_anim_time + 0.03 <= time.monotonic():
            self.up_anim_time = time.monotonic()
            self.cur_frame = (self.cur_frame + 1) % len(self.frame)
            self.image = self.frame[self.cur_frame]
    
    def change_sheet(self, new_sheet, cols, rows, num=0):
        self.sheet = new_sheet
        self.cut_sheets(self.sheet, cols, rows, num)
        self.cur_frame = 0
        self.image = self.frame[self.cur_frame]
    
    def hero_collide(self, obj):
        if pygame.sprite.collide_mask(self, obj) and not hero.death:
            hero.finish = True
        
        
class StartPlatform(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__(all_sprites)
        self.image = 1


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
        if not target.death:
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
    back_ground_surface = pygame.Surface((WIDTH * 10, HEIGHT * 10), pygame.SRCALPHA, 32)
    sprite_height = back_ground_sprite.get_height()
    sprite_width = back_ground_sprite.get_width()
    for y in range(((HEIGHT + sprite_height - 1) // sprite_height) * 3):
        for x in range(((WIDTH + sprite_width - 1) // sprite_width + 10) * 3):
            back_ground_surface.blit(back_ground_sprite, (x * sprite_width, y * sprite_height))
    return back_ground_surface


def game():
    global hero, seconds_counter, mode
    words = ["YOU'RE GREAT!!!", 'GOOD JOB!!!', 'YOU DA BEST!!!', "WHO'S AWESOME?!!"]
    word = random.choice(words)
    menu_fl = 0
    return_fl = 0
    next_lvl_fl = 0
    game_over = False
    left, right, up = False, False, False
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if not game_over and not hero.finish:
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
            elif game_over and not hero.finish:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if hero.death or game_over:
                        if 487 - 60 >= event.pos[0] >= 312 - 60 and 457 >= event.pos[1] >= 381:
                            screen.blit(return_to_menu_black, (312 - 60, 381))
                            pygame.display.flip()
                            menu_fl = 1
                    else:
                        if 487 - 90 >= event.pos[0] >= 312 - 90 and 457 >= event.pos[1] >= 381:
                            screen.blit(return_to_menu_black, (312 - 90, 381))
                            pygame.display.flip()
                            menu_fl = 1
                elif event.type == pygame.MOUSEBUTTONUP:
                    if menu_fl:
                        menu_fl = 2
                        break
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if hero.death or game_over:
                        if 489 + 10 >= event.pos[0] >= 420 + 10 and 454 >= event.pos[1] >= 381:
                            screen.blit(return_to_play_black, (430, 381))
                            pygame.display.flip()
                            return_fl = 1
                    else:
                        if 489 - 30 >= event.pos[0] >= 420 - 30 and 454 >= event.pos[1] >= 381:
                            screen.blit(return_to_play_black, (390, 381))
                            pygame.display.flip()
                            return_fl = 1
                elif event.type == pygame.MOUSEBUTTONUP:
                    if return_fl:
                        return_fl = 2
                        break
            elif hero.finish and not game_over:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if 489 + 120 >= event.pos[0] >= 420 + 60 and 457 >= event.pos[1] >= 381:
                        screen.blit(black_next_level, (480, 381))
                        pygame.display.flip()
                        next_lvl_fl = 1
                elif event.type == pygame.MOUSEBUTTONUP:
                    if next_lvl_fl:
                        next_lvl_fl = 2
                        break
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if hero.death or game_over:
                        if 487 - 60 >= event.pos[0] >= 312 - 60 and 457 >= event.pos[1] >= 381:
                            screen.blit(return_to_menu_black, (312 - 60, 381))
                            pygame.display.flip()
                            menu_fl = 1
                    else:
                        if 487 - 90 >= event.pos[0] >= 312 - 90 and 457 >= event.pos[1] >= 381:
                            screen.blit(return_to_menu_black, (312 - 90, 381))
                            pygame.display.flip()
                            menu_fl = 1
                elif event.type == pygame.MOUSEBUTTONUP:
                    if menu_fl:
                        menu_fl = 2
                        break
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if hero.death or game_over:
                        if 489 + 10 >= event.pos[0] >= 420 + 10 and 454 >= event.pos[1] >= 381:
                            screen.blit(return_to_play_black, (430, 381))
                            pygame.display.flip()
                            return_fl = 1
                    else:
                        if 489 - 30 >= event.pos[0] >= 420 - 30 and 454 >= event.pos[1] >= 381:
                            screen.blit(return_to_play_black, (390, 381))
                            pygame.display.flip()
                            return_fl = 1
                elif event.type == pygame.MOUSEBUTTONUP:
                    if return_fl:
                        return_fl = 2
                        break
                
        if menu_fl == 2:
            answer = 'menu'
            break
        if return_fl == 2:
            answer = 'restart'
            break
        if next_lvl_fl == 2:
            answer = 'next'
            break
        pygame.display.flip()
        screen.fill((0, 0, 0))
        camera.update(hero)
        if not hero.death:
            for sprite in all_sprites:
                camera.apply(sprite)
        bg_group.draw(screen)
        traps_group.draw(screen)
        platforms_group.draw(screen)
        finish_point_group.draw(screen)
        fruit_group.draw(screen)
        hero_group.draw(screen)
        plant_group.draw(screen)
        plant_bullet_group.draw(screen)
        hero.update(left, right, up)
        up = False
        hero.update_animation()
        mushroom_group.draw(screen)
        for finish in finish_point_group:
            finish.update_animation()
            finish.hero_collide(hero)
        for h in traps_group:
            h.hero_collide(hero)
        for bul in plant_bullet_group:
            bul.fly()
            bul.collide()
            bul.hero_collide(hero)
        for plant in plant_group:
            plant.is_death(hero)
        for plant in plant_group:
            plant.update_animation()
            plant.hero_collide(hero)
            plant.shoot()
        for mush in mushroom_group:
            mush.is_death(hero)
        for mush in mushroom_group:
            mush.update_animation()
            mush.run()
            mush.hero_collide(hero)
        for fruit in fruit_group:
            fruit.update_animation()
            if not (hero.death or game_over):
                fruit.collide(hero)
        if (hero.death or game_over) and not hero.finish:
            game_over = True
            gms = game_over_sign(mode)
            screen.blit(gms[0], (gms[1], gms[2]))
            if menu_fl:
                screen.blit(return_to_menu_black, (312 - 60, 381))
            else:
                screen.blit(return_to_menu_white, (312 - 60, 381))
            if return_fl:
                screen.blit(return_to_play_black, (430, 381))
            else:
                screen.blit(return_to_play_white, (430, 381))
        elif hero.finish and not (hero.death or game_over):
            greeting_sign = some_finish_word(word, mode)
            screen.blit(greeting_sign[0], (greeting_sign[1], greeting_sign[2]))
            if menu_fl:
                screen.blit(return_to_menu_black, (312 - 90, 381))
            else:
                screen.blit(return_to_menu_white, (312 - 90, 381))
            if return_fl:
                screen.blit(return_to_play_black, (430 - 40, 381))
            else:
                screen.blit(return_to_play_white, (430 - 40, 381))
            if next_lvl_fl:
                screen.blit(black_next_level, (480, 381))
            else:
                screen.blit(white_next_level, (480, 381))
        if seconds_counter % 30 == 1:
            mode = 1 - mode
        seconds_counter += 1
        clock.tick(FPS)
    return answer


def restart_level():
    for sprite in all_sprites:
        sprite.kill()
    fruits = ['apple', 'banana', 'melon', 'strawberry']
    background = load_back_ground('Sprites/Background', 'Blue.png')
    Background(background)
    Mushroom((600, 250))
    Plant((1000, 258))
    Traps('spikes', 288, 235)
    hero = MainCharacter((100, 100))
    for i in range(23):
        Platform('grass', i * 48, 300)
    FinishPlatform((860, 252))
    Platform('grass', 288, 252)
    Platform('grass', 800, 252)
    for i in range(23):
        Fruit((i * 30, 200), random.choice(fruits))
    return hero


def start_game():
    for sprite in all_sprites:
        sprite.kill()
    load_menu()
    fruits = ['apple', 'banana', 'melon', 'strawberry']
    background = load_back_ground('Sprites/Background', 'Blue.png')
    Background(background)
    Mushroom((600, 250))
    Plant((1000, 258))
    Traps('spikes', 288, 235)
    FinishPlatform((860, 240))
    hero = MainCharacter((100, 100))
    for i in range(23):
        Platform('grass', i * 48, 300)
    Platform('grass', 288, 252)
    Platform('grass', 800, 252)
    for i in range(23):
        Fruit((i * 30, 200), random.choice(fruits))
    return hero


# Создание всех объектов, главный игровой цикл и отслеживание всех событий в игре
if __name__ == '__main__':
    hero = start_game()
    running = True
    left, right, up = False, False, False
    seconds_counter = 0
    camera = Camera((hero.rect.x, hero.rect.y))
    mode = 0
    while True:
        answer = game()
        if answer == 'menu':
            hero = start_game()
        elif answer == 'restart':
            hero = restart_level()
        elif answer == 'next':
            terminate()

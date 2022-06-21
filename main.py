import pygame, sys, random


def draw_bg():
    screen.blit(bg_surface, (bg_x_pos, 0))
    screen.blit(bg2_surface, (bg_x_pos + 288, 0))


def draw_floor():
    screen.blit(floor_surface, (floor_x_pos, 450))
    screen.blit(floor_surface, (floor_x_pos + 285, 450))


def create_ice():
    random_ice_pos = random.choice(ice_height)
    bottom_ice = ice_surface.get_rect(midtop=(500, random_ice_pos))
    top_ice = ice_surface.get_rect(midbottom=(500, random_ice_pos - 150))
    return bottom_ice, top_ice


def move_ices(ices):
    for ice in ices:
        ice.centerx -= 3
    return ices


def draw_ices(ices):
    for ice in ices:
        if ice.bottom >= 512:
            screen.blit(ice_surface, ice)
        else:
            flip_ice = pygame.transform.flip(ice_surface, False, True)
            screen.blit(flip_ice, ice)


def check_collision(ices):
    for ice in ices:
        if box_rect.colliderect(ice):
            death_sound.play()
            return False

    if box_rect.top <= -100 or box_rect.bottom >= 450:
        return False

    return True


def rotate_box(box):
    new_box = pygame.transform.rotozoom(box, box_movement * 3, 1)
    return new_box


def box_animation():
    new_box = box_frames[box_index]
    new_box_rect = new_box.get_rect(center=(100, box_rect.centery))
    return new_box, new_box_rect


def score_display(game_state):
    if game_state == 'main_game':
        score_surface = game_font.render(str(int(score)), True, (0, 0, 0))
        score_rect = score_surface.get_rect(center=(150, 40))
        screen.blit(score_surface, score_rect)
    if game_state == 'game_over':
        score_surface = game_font.render(f'SCORE : {int(score)}', True, (0, 0, 0))
        score_rect = score_surface.get_rect(center=(150, 70))
        screen.blit(score_surface, score_rect)

        high_score_surface = game_font.render(f'HIGH SCORE : {int(high_score)}', True, (0, 0, 0))
        high_score_rect = high_score_surface.get_rect(center=(140, 420))
        screen.blit(high_score_surface, high_score_rect)


def update_score(score, high_score):
    if score > high_score:
        high_score = score
    return high_score


pygame.mixer.pre_init(frequency=44100, size=16, channels=1, buffer=512)
pygame.init()
screen = pygame.display.set_mode((288, 512))
clock = pygame.time.Clock()
game_font = pygame.font.Font("assets/PixelGameFont.ttf", 20)

# Game Variables
gravity = 0.25
box_movement = 0
game_active = True
score = 0
high_score = 0

bg_surface = pygame.image.load("assets/background1.png").convert()
bg2_surface = pygame.image.load("assets/background2.png").convert()
bg_x_pos = 0

floor_surface = pygame.image.load("assets/base.png").convert()
floor_x_pos = 0

box_downflap = pygame.image.load("assets/downflap.png").convert_alpha()
box_midflap = pygame.image.load("assets/midflap.png").convert_alpha()
box_upflap = pygame.image.load("assets/upflap.png").convert_alpha()
box_frames = [box_downflap, box_midflap, box_upflap]
box_index = 0
box_surface = box_frames[box_index]
box_rect = box_surface.get_rect(center=(50, 255))

BOXFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BOXFLAP, 200)

ice_surface = pygame.image.load("assets/ice.png")
ice_list = []
SPAWNICE = pygame.USEREVENT
pygame.time.set_timer(SPAWNICE, 1000)
ice_height = [200, 300, 400]

game_over_surface = pygame.image.load("assets/message.png").convert_alpha()
game_over_rect = game_over_surface.get_rect(center=(144, 255))

flap_sound = pygame.mixer.Sound('assets/sound/wing.wav')
death_sound = pygame.mixer.Sound('assets/sound/hit.wav')
score_sound = pygame.mixer.Sound('assets/sound/point.wav')
score_sound_countdown = 100

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                box_movement = 0
                box_movement -= 7
                flap_sound.play()
            if event.key == pygame.K_SPACE and game_active == False:
                game_active = True
                ice_list.clear()
                box_rect.center = (50, 256)
                box_movement = 0
                score = 0

        if event.type == SPAWNICE:
            ice_list.extend(create_ice())

        if event.type == BOXFLAP:
            if box_index < 2:
                box_index += 1
            else:
                box_index = 0

            box_surface, box_rect = box_animation()
    # bg

    bg_x_pos -= 1
    draw_bg()
    if bg_x_pos <= -288:
        bg_x_pos = 0

    if game_active:

        # Box

        box_movement += gravity
        rotated_box = rotate_box(box_surface)
        box_rect.centery += box_movement
        screen.blit(rotated_box, box_rect)
        game_active = check_collision(ice_list)

        # Ices

        ice_list = move_ices(ice_list)
        draw_ices(ice_list)

        score += 0.01
        score_display('main_game')
        score_sound_countdown -= 1
        if score_sound_countdown <= 0:
            score_sound.play()
            score_sound_countdown = 100
    else:
        screen.blit(game_over_surface, game_over_rect)
        high_score = update_score(score, high_score)
        score_display('game_over')

    # Floor

    floor_x_pos -= 1
    draw_floor()
    if floor_x_pos <= -285:
        floor_x_pos = 0

    pygame.display.update()
    clock.tick(90)



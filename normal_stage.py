import threading
from pico2d import *
import game_framework
import game_world
import boss_stage
from PlayerClass import Player
from SkeletonClass import Skeleton
from BansheeClass import Banshee
# from BackGround import BackGround
from Scrolling import FixedBackground as BackGround

name = "NormalStage"

M_x, M_y = 0, 0
running = True
d_timer_run = False

player = None
background = None
blackimage = None
monsters = []
next_portal = False
cursor = None
d_count = None
d_board = None
bgm = None

which_stage = 1


def get_angle(start_x, start_y, end_x, end_y):
    dx = end_x - start_x
    dy = end_y - start_y
    return math.atan2(dy, dx) * (180 / math.pi)


def get_distant(x1, y1, x2, y2):
    return math.sqrt(pow(x2 - x1, 2) + pow(y2 - y1, 2))


def dash_timer_start():
    global player
    global d_timer_run
    timer = threading.Timer(2, dash_timer_start)

    if player.dash_count < 6:
        if not d_timer_run:
            d_timer_run = True
        else:
            player.dash_count += 1
        timer.start()
    else:
        d_timer_run = False
        timer.cancel()


def change_stage():
    global player
    global next_portal
    global monsters
    global which_stage

    which_stage = 2
    player.x = 15
    next_portal = False
    monsters = [Skeleton(1) for i in range(5)] + [Banshee(200+(300 * i)) for i in range(5)]
    for m in monsters:
        m.set_background(background)
    game_world.add_objects(monsters, 1)


def enter():
    global player
    global background
    global monsters
    global cursor
    global d_count, d_board
    global blackimage
    global bgm

    player = Player()
    background = BackGround(False)
    monsters = [Skeleton(1) for i in range(5)]
    game_world.add_object(player, 1)
    game_world.add_objects(monsters, 1)
    game_world.add_object(background, 0)

    background.set_center_object(player)
    player.set_background(background)
    for i in range(2):
        player.weapons[i].set_background(background)
    for m in monsters:
        m.set_background(background)

    blackimage = load_image('Black_Image.png')
    cursor = load_image("Cursor.png")
    d_count = load_image("DashCount.png")
    d_board = load_image("DashCountBase.png")
    bgm = load_wav('normal_stage.wav')
    bgm.set_volume(64)
    bgm.repeat_play()
    update()


def exit():
    global player
    global bgm

    del bgm
    del player
    game_world.clear()


def pause():
    pass


def resume():
    pass


def handle_events():
    global player
    global monsters
    global running
    global M_x, M_y
    global d_timer_run

    events = get_events()

    for event in events:
        cx, cy = player.x - player.bg.window_left, player.y - player.bg.window_bottom
        if event.type == SDL_QUIT:
            game_framework.quit()

        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()

        elif event.type == SDL_MOUSEMOTION:
            M_x, M_y = event.x, 600 - 1 - event.y
            for i in range(2):
                if not player.weapons[i].isswing:
                    player.weapons[i].angle = get_angle(cx, cy, M_x, M_y)
            if player.x % 800 < M_x:
                player.stand_dir = 1
            elif player.x % 800 > M_x:
                player.stand_dir = -1

        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_k):
            for monster in monsters:
                game_world.remove_object(monster)
            monsters.clear()

        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_BACKQUOTE):
            player.selected_weapon = (player.selected_weapon + 1) % 2

        else:
            player.handle_event(event)


def update():
    global next_portal
    global monsters
    global player

    if player.hp <= 0:
        game_framework.quit()

    for game_object in game_world.all_objects():
        game_object.update()

    if len(monsters) == 0 and not next_portal:
        next_portal = True

    if player.x >= 1500 and next_portal:
        if which_stage == 1:
            blackimage.draw(750, 300, 1500, 600)
            change_stage()
        else:
            game_framework.change_state(boss_stage)


def draw():
    clear_canvas()
    for game_object in game_world.all_objects():
        game_object.draw()

    d_board.draw(48, 593, 96, 14)
    for n in range(player.dash_count):
        d_count.draw(((n + 1) * 16) - 8, 593, 14, 8)

    cursor.draw(M_x, M_y, 30, 30)
    update_canvas()

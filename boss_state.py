import threading
import enum
from pico2d import *
import game_framework
import game_world
from PlayerClass import Player
from BelialClass import Belial
from BackGround import BackGround

name = "BossState"

M_x, M_y = 0, 0
running = True
d_timer_run = False

player = None
background = None
monsters = []
belial_sword = []
sword_drop_timer = None
cursor = None
d_count = None
d_board = None


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


def attack_timer():
    global player
    player.attack = True


def Drop_Sword():
    global belial_sword
    global sword_drop_timer

    if len(belial_sword) > 0:
        if not belial_sword[0].state == 0:
            belial_sword[0].state = 0
            return
    sword_drop_timer = threading.Timer(3, Drop_Sword)
    sword_drop_timer.start()


def enter():
    global player
    global background
    global monsters
    global cursor
    global d_count, d_board
    global sword_drop_timer

    resize_canvas(800, 600)
    player = Player()
    background = BackGround()
    monsters = [Belial()]
    game_world.add_object(background, 0)
    game_world.add_object(player, 1)
    game_world.add_objects(monsters, 1)
    cursor = load_image("Cursor.png")
    d_count = load_image("DashCount.png")
    d_board = load_image("DashCountBase.png")


def exit():
    global player

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
        if event.type == SDL_QUIT:
            game_framework.quit()

        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()

        elif event.type == SDL_MOUSEMOTION:
            M_x, M_y = event.x, 600 - 1 - event.y
            for i in range(2):
                player.weapons[i].angle = get_angle(player.x, player.y, M_x, M_y)
            if player.x < M_x:
                player.stand_dir = 1
            elif player.x > M_x:
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
    global monsters
    global belial_sword

    for game_object in game_world.all_objects():
        game_object.update()

    if not len(belial_sword) == 0:
        for s in belial_sword:
            s.update()

    if len(monsters) == 0:
        delay(1)
        game_framework.quit()


def draw():
    global belial_sword

    clear_canvas()
    for game_object in game_world.all_objects():
        game_object.draw()

    d_board.draw(48, 593, 96, 14)
    for n in range(player.dash_count):
        d_count.draw(((n + 1) * 16) - 8, 593, 14, 8)

    if not len(belial_sword) == 0:
        for s in belial_sword:
            s.draw()

    cursor.draw(M_x, M_y, 30, 30)
    update_canvas()
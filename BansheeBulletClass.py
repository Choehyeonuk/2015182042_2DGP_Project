from pico2d import *
import math
import game_world
import game_framework
import normal_stage


class Banshee_Bullet:
    image = None
    d_image = None
    hit_player_sound = None

    def __init__(self, x, y, angle):
        if Banshee_Bullet.image is None:
            Banshee_Bullet.image = load_image("BanShee_Bullet(13x16).png")
        if Banshee_Bullet.d_image is None:
            Banshee_Bullet.d_image = load_image("Banshee_Bullet_Del(20x27).png")
        if Banshee_Bullet.hit_player_sound is None:
            Banshee_Bullet.hit_player_sound = load_wav('hit_player.wav')
            Banshee_Bullet.hit_player_sound.set_volume(64)

        self.atk = 5
        self.r = 0
        self.cen_x, self.cen_y = x, y
        self.x, self.y = 0, 0
        self.angle = angle
        self.frame = 0

        self.set_background()

    def set_background(self):
        self.bg = normal_stage.background

    def attack_collide(self):
        left_a, bottom_a, right_a, top_a = self.x - 6.5, self.y - 8, self.x + 6.5, self.y + 8

        left_b, bottom_b, right_b, top_b = normal_stage.player.x - 15, normal_stage.player.y - 30, \
                                           normal_stage.player.x + 15, normal_stage.player.y

        if normal_stage.player.opacity_mode: return False
        if left_a > right_b: return False
        if right_a < left_b: return False
        if top_a < bottom_b: return False
        if bottom_a > top_b: return False
        return True

    def update(self):
        self.x = (self.r * math.cos(self.angle / 360 * 2 * math.pi)) + self.cen_x
        self.y = (self.r * math.sin(self.angle / 360 * 2 * math.pi)) + self.cen_y
        self.r += 100 * game_framework.frame_time

        if self.attack_collide():
            Banshee_Bullet.hit_player_sound.play()
            normal_stage.player.hp -= self.atk
            game_world.remove_object(self)

        if self.r >= 300:
            game_world.remove_object(self)
        self.frame = (self.frame + 4 * (1.0/0.5) * game_framework.frame_time) % 4

    def draw(self):
        cx, cy = self.x - self.bg.window_left, self.y - self.bg.window_bottom
        Banshee_Bullet.image.clip_draw(int(self.frame) * 13, 0, 13, 16,  cx, cy, 20, 20)

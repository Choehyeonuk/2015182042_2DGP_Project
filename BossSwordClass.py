from pico2d import *
import math
import boss_stage
import game_framework


class Boss_Sword:
    Atk = 3
    image = None

    def __init__(self, x):
        if Boss_Sword.image is None:
            Boss_Sword.image = load_image("BossSword.png")
        self.x, self.y = 300 + x, 500
        self.angle = 0
        self.state = 1
        self.start_x, self.start_y = self.x, self.y
        self.end_x, self.end_y = boss_stage.player.x, boss_stage.player.y - 40
        self.hit_point_x, self.hit_point_y = self.x, self.y - 60
        self.fall_distant = 0
        self.hit_player_sound = load_wav('hit_player.wav')
        self.hit_player_sound.set_volume(64)
        self.hit_player = False

    def update(self):
        if self.state == 1:
            self.angle = boss_stage.get_angle(self.x, self.y, boss_stage.player.x, boss_stage.player.y) + 90
            self.end_x, self.end_y = boss_stage.player.x, boss_stage.player.y - 40
            self.hit_point_x = self.x + (60 * math.cos((self.angle - 90) / 360 * 2 * math.pi))
            self.hit_point_y = self.y + (60 * math.sin((self.angle - 90) / 360 * 2 * math.pi))
        else:
            self.x = (1 - self.fall_distant) * self.start_x + self.fall_distant * self.end_x
            self.y = (1 - self.fall_distant) * self.start_y + self.fall_distant * self.end_y
            self.hit_point_x = self.x + (60 * math.cos((self.angle - 90) / 360 * 2 * math.pi))
            self.hit_point_y = self.y + (60 * math.sin((self.angle - 90) / 360 * 2 * math.pi))
            self.fall_distant += 1 * game_framework.frame_time
            if boss_stage.player.x - 15 <= self.hit_point_x <= boss_stage.player.x + 15 and boss_stage.player.y - 30 <= self.hit_point_y <= boss_stage.player.y:
                if not self.hit_player and not boss_stage.player.opacity_mode:
                    self.hit_player_sound.play()
                    boss_stage.player.hp -= Boss_Sword.Atk
                    self.hit_player = True
            if self.fall_distant >= 1:
                boss_stage.belial_sword.remove(self)
                if len(boss_stage.belial_sword) > 0:
                    boss_stage.belial_sword[0].state = 0

    def draw(self):
        if self.state == 1:
            Boss_Sword.image.rotate_draw(self.angle / 360 * 2 * math.pi, self.x, self.y, 30, 120)
        else:
            Boss_Sword.image.rotate_draw(self.angle / 360 * 2 * math.pi, self.x, self.y, 30, 120)

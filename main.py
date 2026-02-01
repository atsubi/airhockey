import pyxel
import numpy as np
import configparser
import time

from gameManager import GameManager
from mallet import Mallet
from puck import Puck
from score import Score

class GameApp:

    def __init__(self):

        # config
        config_ini = configparser.ConfigParser()
        config_ini.read('config.ini', encoding='utf-8')

        pyxel.init(int(config_ini['DEFAULT']['Width']), 
                int(config_ini['DEFAULT']['Height']), 
                title="Air Hockey",
                fps=60,
                capture_scale=1)
        pyxel.mouse(True)
        
        self.wall_width = int(config_ini['DEFAULT']['WallWidth'])        
        self.goal_width = int(config_ini['DEFAULT']['GoalWidth'])
        self.goal_left = pyxel.width / 2 - self.goal_width / 2
        self.goal_right = pyxel.width / 2 + self.goal_width / 2

        self.win_score = int(config_ini['DEFAULT']['WinScore'])
        
        ### インスタンス生成
        self.puck = Puck(
            np.array((pyxel.width//2, pyxel.height//2)),
            np.array((int(config_ini['PUCK']['VelocityX']), int(config_ini['PUCK']['VelocityY']))),
            int(config_ini['PUCK']['Radius'])
        )

        self.mallet1 = Mallet(np.array((pyxel.width//2, pyxel.height - 10)), int(config_ini['MALLET']['Radius'])) 
        self.mallet2 = Mallet(np.array((pyxel.width//2, 10)), int(config_ini['MALLET']['Radius'])) 
        self.score = Score()
        self.manager = GameManager(self.puck, self.mallet1, self.mallet2, self.score, pyxel.width, pyxel.height, self.wall_width, self.goal_left, self.goal_right, self.win_score)        
        self.last_time = time.time()
        
        pyxel.run(self.update, self.draw)

    def update(self):
        now_time = time.time()
        dt = now_time - self.last_time

        self.manager.update(dt)

        if self.manager.is_game_over and pyxel.btnp(pyxel.KEY_R):
            self.manager.reset_game()
        
        # mallet1入力
        if not self.manager.is_game_over and pyxel.btn(pyxel.MOUSE_BUTTON_LEFT):
            mallet1_target = np.array((pyxel.mouse_x, pyxel.mouse_y))
            self.manager.update_mallet1_pos(mallet1_target, dt)

        # 終了
        if pyxel.btn(pyxel.KEY_ESCAPE):
            pyxel.quit()

        self.last_time = now_time

    def draw(self):
        self.draw_background()
        self.draw_objects()
        self.draw_score()


    def draw_background(self):
        # 背景
        pyxel.cls(11)

        # 中心線
        pyxel.line(self.wall_width, pyxel.height//2, pyxel.width - self.wall_width, pyxel.height//2, 3)

        # 壁
        pyxel.rect(0, 0, self.wall_width, pyxel.height, 7)
        pyxel.rect(pyxel.width - self.wall_width, 0, self.wall_width, pyxel.height, 7)
        pyxel.rect(self.wall_width, 0, self.goal_left - self.wall_width, self.wall_width, 7) 
        pyxel.rect(self.goal_right, 0, pyxel.width - self.wall_width - self.goal_right, self.wall_width, 7)
        pyxel.rect(self.wall_width, pyxel.height - self.wall_width, self.goal_left - self.wall_width, self.wall_width, 7)
        pyxel.rect(self.goal_right, pyxel.height - self.wall_width, pyxel.width - self.wall_width - self.goal_right, self.wall_width, 7)



    def draw_objects(self):
        # puck
        pyxel.circ(self.puck.pos[0], self.puck.pos[1], self.puck.radius, 7)
        pyxel.circb(self.puck.pos[0], self.puck.pos[1], self.puck.radius, 13)

        # mallet1
        pyxel.circ(self.mallet1.pos[0], self.mallet1.pos[1], self.mallet1.radius, 7)
        pyxel.circb(self.mallet1.pos[0], self.mallet1.pos[1], self.mallet1.radius, 9)
        pyxel.circ(self.mallet1.pos[0], self.mallet1.pos[1], self.mallet1.radius - 4, 9)

        # mallet1
        pyxel.circ(self.mallet2.pos[0], self.mallet2.pos[1], self.mallet2.radius, 7)
        pyxel.circb(self.mallet2.pos[0], self.mallet2.pos[1], self.mallet2.radius, 9)
        pyxel.circ(self.mallet2.pos[0], self.mallet2.pos[1], self.mallet2.radius - 4, 9)

    def draw_score(self):
        # score
        pyxel.text(self.wall_width//2 + 1, pyxel.height - 15, str(self.score.score1), 0)
        pyxel.text(self.wall_width//2, pyxel.height - 15, str(self.score.score1), 8)
        pyxel.text(self.wall_width//2 + 1, 10, str(self.score.score2), 0)
        pyxel.text(self.wall_width//2, 10, str(self.score.score2), 8)

        if self.manager.is_game_over:
            msg = "GAME SET"
            pyxel.text(pyxel.width//2 - len(msg)*2 + 1, pyxel.height//2 - 10, msg, 0)
            pyxel.text(pyxel.width//2 - len(msg)*2, pyxel.height//2 - 10, msg, 7)
            
            if self.score.score1 >= self.win_score:
                win_msg = "YOU WIN!"
            else:
                win_msg = "YOU LOSE"
            pyxel.text(pyxel.width//2 - len(win_msg)*2 + 1, pyxel.height//2, win_msg, 0)
            pyxel.text(pyxel.width//2 - len(win_msg)*2, pyxel.height//2, win_msg, 7)

            restart_msg = "PRESS R TO RESTART"
            pyxel.text(pyxel.width//2 - len(restart_msg)*2 + 1, pyxel.height//2 + 10, restart_msg, 0)
            pyxel.text(pyxel.width//2 - len(restart_msg)*2, pyxel.height//2 + 10, restart_msg, 7)


GameApp()

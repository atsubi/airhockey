from puck import Puck
from mallet import Mallet

from score import Score
import numpy as np

class GameManager:

    def __init__(self, 
                puck: Puck, 
                mallet1: Mallet, 
                mallet2: Mallet, 
                score: Score,
                width: int = 120,
                height: int = 160,
                wallWidth: int = 10,
                goalLeft: int = 50,
                goalRight: int = 50,
                winScore: int = 1):
        
        self.puck = puck
        self.mallet1 = mallet1
        self.mallet2 = mallet2
        self.score = score
    
        self.width = width
        self.height = height

        self.wall_width = wallWidth

        self.goal_left = goalLeft
        self.goal_right = goalRight

        self.win_score = winScore

        self.is_game_over = False

    def reset_game(self):
        self.score.reset()
        self.puck.reset()
        self.mallet1.reset()
        self.mallet2.reset()

        self.is_game_over = False

    def update(self, dt: float = 1/60):
        if self.is_game_over:
            return
        self.puck.update(dt)
        self._update_mallet2_ai(dt)
        self._check_puck_collision_wall()
        self._check_puck_collision_mallet()
        self._check_goal()

    def _check_puck_collision_wall(self):
        # X
        if self.puck.pos[0] < self.puck.radius + self.wall_width:
            self.puck.setPos(np.array((self.puck.radius + self.wall_width, self.puck.pos[1])))
            self.puck.bounceX_for_wall()

        if self.puck.pos[0] + self.puck.radius > self.width - self.wall_width:
            self.puck.setPos(np.array((self.width - self.puck.radius - self.wall_width, self.puck.pos[1])))
            self.puck.bounceX_for_wall()

        # Y
        # 上
        if self.puck.pos[1] < self.puck.radius + self.wall_width:
            if self.puck.pos[0] < self.goal_left + self.puck.radius:
                self.puck.setPos(np.array((self.puck.pos[0], self.puck.radius + self.wall_width)))
                self.puck.bounceY_for_wall()
            elif self.puck.pos[0] > self.goal_right - self.puck.radius:
                self.puck.setPos(np.array((self.puck.pos[0], self.puck.radius + self.wall_width)))
                self.puck.bounceY_for_wall()
        # 下
        elif self.puck.pos[1] + self.puck.radius + self.wall_width > self.height:
            if self.puck.pos[0] < self.goal_left + self.puck.radius:
                self.puck.setPos(np.array((self.puck.pos[0], self.height - self.puck.radius - self.wall_width)))
                self.puck.bounceY_for_wall()
            elif self.puck.pos[0] > self.goal_right - self.puck.radius:
                self.puck.setPos(np.array((self.puck.pos[0], self.height - self.puck.radius - self.wall_width)))
                self.puck.bounceY_for_wall()


    def update_mallet1_pos(self, target: np.array, dt: float = 1/60):
        target[0] = min(self.width - self.mallet1.radius - self.wall_width, max(self.mallet1.radius + self.wall_width, target[0]))
        target[1] = min(self.height - self.mallet1.radius - self.wall_width, max(self.height//2 + self.mallet1.radius, target[1]))
        self.mallet1.move_to(target, dt)

    def _update_mallet2_ai(self, dt: float):
        old_pos = self.mallet2.pos.copy()

        # パックのX座標に追従する簡易AI
        target_x = self.puck.pos[0]

        # パックが四隅（自陣コーナー）にある場合のスタック回避
        # 自陣（画面上半分）かつ壁際の場合、ターゲットを少し中央に寄せてスペースを空ける
        if self.puck.pos[1] < self.height / 2:
            corner_margin = 30  # 壁際とみなす範囲
            avoid_dist = 20     # マレットが離れる距離

            if self.puck.pos[0] < self.wall_width + self.puck.radius + corner_margin:
                target_x = self.wall_width + self.puck.radius + corner_margin + avoid_dist
            elif self.puck.pos[0] > self.width - (self.wall_width + self.puck.radius + corner_margin):
                target_x = self.width - (self.wall_width + self.puck.radius + corner_margin + avoid_dist)

        speed = 1.0
        if abs(self.mallet2.pos[0] - target_x) > speed:
            if self.mallet2.pos[0] < target_x:
                self.mallet2.pos[0] += speed
            elif self.mallet2.pos[0] > target_x:
                self.mallet2.pos[0] -= speed

        # Y座標が壁にめり込まないように補正
        if self.mallet2.pos[1] < self.wall_width + self.mallet2.radius:
            self.mallet2.pos[1] = self.wall_width + self.mallet2.radius

        # 移動範囲制限
        self.mallet2.pos[0] = max(self.wall_width + self.mallet2.radius, min(self.width - self.wall_width - self.mallet2.radius, self.mallet2.pos[0]))

        if dt > 0:
            self.mallet2.vel = (self.mallet2.pos - old_pos) / dt
        else:
            self.mallet2.vel = np.array((0.0, 0.0))

    def _check_puck_collision_mallet(self):
        self._check_puck_collision_mallet1()
        self._check_puck_collision_mallet2()

    def _check_puck_collision_mallet1(self):
        min_dist = self.mallet1.radius + self.puck.radius
        diff = self.puck.pos - self.mallet1.pos
        n, dist = self._norm(diff)        
        if dist > min_dist:
            return
        
        # めり込みを解消する位置へ移動 (マレットの位置 + 半径分の距離)
        self.puck.setPos(self.mallet1.pos + n * min_dist)
        self.puck.bounce_mallet(n, self.mallet1.vel)
    
    def _check_puck_collision_mallet2(self):
        min_dist = self.mallet2.radius + self.puck.radius
        diff = self.puck.pos - self.mallet2.pos
        n, dist = self._norm(diff)
        if dist > min_dist:
            return
        
        self.puck.setPos(self.mallet2.pos + n * min_dist)
        self.puck.bounce_mallet(n, self.mallet2.vel)
    
    def _norm(self, v : np.array, eps: float = 1e-6):
        length = np.linalg.norm(v)
        if length > eps:
            return v / length, length
        else:
            return np.array((0, 0)), 0         

    def _check_goal(self):

        if self.puck.pos[1] + self.puck.radius >= 0 and self.puck.pos[1] - self.puck.radius <= self.height:
            return        
        
        if self.puck.pos[0] >= self.goal_left + self.puck.radius and self.puck.pos[0] <= self.goal_right - self.puck.radius:
            if self.puck.pos[1] < 0:
                self.score.goal_score1()
                self.puck.reset()              
                if self.score.score1 >= self.win_score:
                    self.is_game_over = True
            else:
                self.score.goal_score2()
                self.puck.reset()
                if self.score.score2 >= self.win_score:
                    self.is_game_over = True

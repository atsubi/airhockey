import numpy as np
import random

class Puck:

    def __init__(self, pos: np.array, vel: np.array, radius: float = 10):
        self.__init_pos = pos.astype(float)
        self.__init_vel = vel.astype(float)
        self.reset()
        self.radius = radius

    def reset(self):
        self.pos = self.__init_pos.copy()
        self.vel =  np.array((
            random.randint(-30 + int(self.__init_vel[0]), 30 + int(self.__init_vel[0])),
            random.choice([random.randint(-int(self.__init_vel[1]), -int(self.__init_vel[1]) + 30), random.randint(int(self.__init_vel[1]) - 30, int(self.__init_vel[1]))])
        ), dtype=float)

    def update(self, dt: float = 1/60):        
        self.pos += self.vel * dt

    def setPos(self, pos: np.array):
        self.pos = pos.copy()
        
    def bounceX_for_wall(self):
        self.vel[0] = -self.vel[0] 
        self.vel *= 0.9

    def bounceY_for_wall(self):
        self.vel[1] = -self.vel[1] 
        self.vel *= 0.9

    def bounce_mallet(self, n: np.array, mallet_vel: np.array = np.array((0.0, 0.0))):
        speed = np.linalg.norm(self.vel)
        speed *= 0.9
        
        # マレットの速度ベクトルを法線ベクトルnに射影して加算
        impact = np.dot(mallet_vel, n)
        if impact > 0:
            speed += impact * 0.5  # 0.5は影響度の係数（調整可能）

        # ヒット感を出すために最低速度を保証する
        self.vel = max(speed, 150.0) * n

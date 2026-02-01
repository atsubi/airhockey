import numpy as np


class Mallet:
    
    def __init__(self, pos: np.array = np.array((0, 0)), radius: float = 10):
        self.init_pos = pos.astype(float)
        self.pos = self.init_pos.copy()
        self.radius = radius
        self.vel = np.array((0.0, 0.0))

    def reset(self):
        self.pos = self.init_pos.copy()
        self.vel = np.array((0.0, 0.0))

    def move_to(self, target: np.array, dt: float = 1/60):
        if dt > 0:
            self.vel = (target - self.pos) / dt
        else:
            self.vel = np.array((0.0, 0.0))
        self.pos = target

    
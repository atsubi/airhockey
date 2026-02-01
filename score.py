
class Score:
    
    def __init__(self):
        self.reset()

    def reset(self):
        self.score1 = 0
        self.score2 = 0

    def goal_score1(self):
        self.score1 += 1

    def goal_score2(self):
        self.score2 += 1

        

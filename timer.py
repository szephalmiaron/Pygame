import pygame

class Timer():
    current_time = 0
    def __init__(self, surface, font, rect, clock):
        self.surface = surface
        self.font = font
        self.timer_rect = rect
        self.clock = clock

    def time_print(self):
        self.current_time += self.clock.get_time() / 1000
        self.surface.blit((self.font.render(f"Eltelt idő: {int(self.current_time)}", True, (0, 0, 0))), self.timer_rect)
    
    def reset_timer(self):
        self.current_time -= self.current_time

class Score():
    def __init__(self, surface, font, rect):
        self.surface = surface
        self.font = font
        self.score_rect = rect
        self.score = 0

    def score_print(self):
        self.surface.blit((self.font.render(f"Pontszám: {self.score}", True, (0, 0, 0))), self.score_rect)
    
    def add_score(self, amount):
        self.score += amount

    def win(self, time):
        self.score += (90 - int(time))
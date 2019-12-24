import pygame
import sys
from rocket import Rocket


class Game(object):

    def __init__(self):

        max_fps = 100
        screen_width = 1280
        screen_high = 720

        # INITIALIZATION

        pygame.init()
        self.screen = pygame.display.set_mode((screen_width, screen_high))
        self.fps_clock = pygame.time.Clock()
        self.fps_delta = 0.0
        self.player = Rocket(self)

        while True:

            # HANDLE EVENTS

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit(0)
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    sys.exit(0)

            # TICKING

            self.fps_delta += self.fps_clock.tick() / 1000.0
            while self.fps_delta > 1 / max_fps:
                self.tick()
                self.fps_delta -= 1 / max_fps

            # DRAWING
            self.screen.fill((0, 0, 0))
            self.draw()
            pygame.display.flip()

    def tick(self):

        # CHECKING INPUTS
        self.player.tick()
        keys = pygame.key.get_pressed()

    def draw(self):

        # DRAWING
        self.player.draw()


if __name__ == '__main__':
    Game()
    print("END")

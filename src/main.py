from settings import *
from game_state import game_state
import sys

class game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.display_surface = pygame.display.set_mode((winWidth, winHeight))
        pygame.display.set_caption("Geometry War")
        self.cloak = pygame.time.Clock()

        self.game_state = game_state()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            dt = self.cloak.tick(60)/1000
            self.game_state.run(dt)

            pygame.display.update()
            
if __name__ == '__main__':
    GeometryWar = game()
    GeometryWar.run()

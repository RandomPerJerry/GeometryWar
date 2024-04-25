from settings import *
from level import level
import sys

class game:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((winWidth, winHeight))
        pygame.display.set_caption("Geometry War")
        self.cloak = pygame.time.Clock()

        self.level = level()
		
    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.level.run()

            self.cloak.tick(60)
            pygame.display.update()

if __name__ == '__main__':
    GeometryWar = game()
    GeometryWar.run()

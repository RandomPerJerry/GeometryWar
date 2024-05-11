from settings import *
from game_state import GameState
import sys

class game:
    def __init__(self):
        """
        Initialize the game

        :rtype: None
        """
        pygame.init()
        pygame.mixer.init()
        self.display_surface = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Geometry War")
        self.cloak = pygame.time.Clock()

        self.game_state = GameState()

    def run(self):
        """
        Run the game

        :rtype: None
        """
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            dt = self.cloak.tick(FPS)/1000 # delta time in seconds
            self.game_state.run(dt)

            pygame.display.update()

# the two lines of code that runs the entire game lol.
if __name__ == '__main__':
    GeometryWar = game()
    GeometryWar.run()

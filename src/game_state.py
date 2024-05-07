from settings import *
from text_shape import Text
from level import level

class starting_menu:
    def __init__(self):

        self.display_surface = pygame.display.get_surface()

        self.title = Text(self.display_surface, winWidth//2, winHeight//2, 50, "GEOMETRY WARS", clrWhite)
        self.instruction1 = Text(self.display_surface, winWidth//2, winHeight//2 - 50, 30, "Press enter to play", clrWhite)
        self.instruction2 = Text(self.display_surface, winWidth//2, winHeight//2 - 80, 30, "WASD to move, Space for Bomb, Left shigt for Dash", clrWhite)
        self.instruction3 = Text(self.display_surface, winWidth//2, winHeight//2 - 110, 30, "Move mouse to aim, click to shoot", clrWhite)
        self.text_list = [self.title, self.instruction1, self.instruction2, self.instruction3]

        self.moveon = False

    def input(self):

        keys = pygame.key.get_pressed()

        if keys[pygame.K_KP_ENTER]:
            pass

    def run(self):
        self.display_surface.fill(clrBlack)
        
        for text in self.text_list:
            text.draw()

class ingame:
    def __init__(self):

        self.level 

class win_menu:
    def __init__(self):
        pass

    


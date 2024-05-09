from settings import *
from text_shape import Text
from level import level
from timer import Timer


class game_state:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()

        self.start = starting_menu(self.display_surface)
        self.in_game = ingame()
        self.win = win_menu(self.display_surface)

        self.state_list = [self.start, self.in_game, self.win]
        self.current_index = 0
        self.current_state = self.state_list[self.current_index]

    def update(self):
        self.start = starting_menu(self.display_surface)
        self.in_game = ingame()
        self.win = win_menu(self.display_surface)

    def run(self, dt): 
        res = 0

        if self.current_index == 1:
            res = self.current_state.run(dt)
        else:
            res = self.current_state.run()

        if res != 0:
            self.current_state.reset()
            pygame.mixer.music.stop()
            self.current_index += res
            self.current_state = self.state_list[self.current_index]

class starting_menu:
    def __init__(self, display_surface):

        self.display_surface = display_surface

        self.title = Text(self.display_surface, None, 200, 60, "GEOMETRY WARS", clrWhite)
        self.instruction1 = Text(self.display_surface, None, 250, 30, "Press enter to play", clrWhite)
        self.instruction2 = Text(self.display_surface, None, 300, 30, "WASD to move, Space for Bomb, Left shift for Dash", clrWhite)
        self.instruction3 = Text(self.display_surface, None, 350, 30, "Move mouse to aim, click to shoot", clrWhite)
        self.text_list = [self.title, self.instruction1, self.instruction2, self.instruction3]

        self.first_iteration = True
        self.input_block_timer = Timer(200)

    def reset(self):
        self.first_iteration = True

    def input(self):

        keys = pygame.key.get_pressed()

        if keys[pygame.K_RETURN] and self.input_block_timer.active == False:
            return 1
        
        return 0

    def run(self):
        if self.first_iteration:
            pygame.mixer.music.load(join("data", "sounds", "Menu_MUSIC.mp3"))
            pygame.mixer.music.set_volume(0.5)
            pygame.mixer.music.play(-1)
            self.input_block_timer.activate()
            self.first_iteration = False

        self.input_block_timer.update()
        self.display_surface.fill(clrBlack)
        for text in self.text_list:
            text.draw()

        return self.input()

class ingame:
    def __init__(self):
        self.level = level()
        self.first_iteration = True


    def reset(self):
        self.level = level()
        self.first_iteration = True

    def run(self, dt):
        if self.first_iteration:
            pygame.mixer.music.load(join("data", "sounds", "MainGame_MUSIC.mp3"))
            pygame.mixer.music.play(-1)
            self.level.setup()
            self.first_iteration = False

        res = self.level.run(dt)
        
        return res

class win_menu:
    def __init__(self, display_surface):
        self.win_text = Text(display_surface, None, None, 70, "You Win!", clrWhite)
        self.retry_text = Text(display_surface, None, winHeight//2 + 100, 30, "Press Enter to play again", clrWhite)
        self.input_block_timer = Timer(200)
        self.first_iteration = True

    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RETURN] and self.input_block_timer.active == False:
            return -2

        return 0

    def reset(self):
        self.first_iteration = True
        
    def run(self):
        if self.first_iteration:
            pygame.mixer.music.load(join("data", "sounds", "Win_MUSIC.mp3"))
            pygame.mixer.music.play(-1)
            self.input_block_timer.activate()
            self.first_iteration = False

        self.input_block_timer.update()

        self.win_text.draw()
        self.retry_text.draw()
        return self.input()

if __name__ == '__main__':
    game_state = game_state()
    game_state.run(0)

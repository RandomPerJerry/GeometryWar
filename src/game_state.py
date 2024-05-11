from settings import *
from text_shape import Text, Button
from level import Level
from timer import Timer


class GameState:
    def __init__(self):
        """
        Class that manages the states of the game

        rtype: None
        """

        self.display_surface = pygame.display.get_surface()

        # tnitialize the different states
        self.start = StartingMenu(self.display_surface)
        self.in_game = InGame(self.start.test_mode_button.state)
        self.win = WinMenu(self.display_surface)

        # for easier management
        self.state_list = [self.start, self.in_game, self.win]
        self.current_index = 0
        self.current_state = self.state_list[self.current_index]

    def update_state_parameters(self):
        """
        Update game state parameters based on the difficulty button state.

        :rtype: None
        """
        testmode = self.start.test_mode_button.state
        self.in_game.update_testmode(testmode)

    def run(self, dt):
        """
        Run the state machine

        :peram float dt: Delta time, used for sprite movemets
        :rtype: None
        """
        if isinstance(self.current_state, StartingMenu):
            # Update difficulty state before starting the game
            self.update_state_parameters()

        # Get the state and run the state, pass argument dt if its level
        res = self.current_state.run(dt) if self.current_index == 1 else self.current_state.run()

        # if there is a change in state, apply change
        if res != 0:
            self.current_state.reset()
            pygame.mixer.music.stop()
            self.current_index += res
            self.current_state = self.state_list[self.current_index]

class StartingMenu:

    def __init__(self, display_surface):

        """
        The class for the staring menu of the game

        :peram pygame.surface.Surface display_surface: The surface that the class draws on
        :rtype: None
        """        

        self.display_surface = display_surface

        # create menu texts
        self.title = Text(self.display_surface, None, 200, 60, "GEOMETRY WARS", clrWhite)
        self.instruction1 = Text(self.display_surface, None, 250, 30, "Press Enter to play", clrWhite)
        self.instruction2 = Text(self.display_surface, None, 300, 30, "WASD to move, Space for Bomb, Left Shift for Dash", clrWhite)
        self.instruction3 = Text(self.display_surface, None, 350, 30, "Move mouse to aim, click to shoot", clrWhite)

        # difficulty button and text
        self.test_mode_button = Button(self.display_surface, WIDTH // 2 - 80, 450, 30, 30)
        self.test_mode_tect = Text(self.display_surface, WIDTH // 2 - 45, 440, 25, "Test Mode", clrWhite, "topleft")

        # text list for easy drawing
        self.text_list = [self.title, self.instruction1, self.instruction2, self.instruction3, self.test_mode_tect]

        # state control
        self.first_iteration = True
        self.input_block_timer = Timer(200) # used to prevent stick keys

    def reset(self):
        """
        Reset the nessecary attributes in the class
        :rtype: none
        """

        self.first_iteration = True

    def input(self):

        """
        Get the player inputs for the menu to function
        :return: the menu activity
        :rtype: int
        """

        # Press enter to enter game (+1)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN] and not self.input_block_timer.active:
            return 1
        return 0

    def run(self):
        """
        Run the starting menu
        :return: the menu activity
        :rtype: int
        """

        # if true, load music and activate timer.
        if self.first_iteration:
            pygame.mixer.music.load(join("data", "sounds", "Menu_MUSIC.mp3"))
            pygame.mixer.music.set_volume(0.5)
            pygame.mixer.music.play(-1)
            self.input_block_timer.activate()
            self.first_iteration = False

        self.display_surface.fill(clrBlack)

        # Update button state
        self.test_mode_button.update()
        self.input_block_timer.update()

        # Draw all texts
        for text in self.text_list:
            text.draw()

        return self.input()


class InGame:
    def __init__(self, testmode):
        """
        Intilize the class that controls the game

        :param bool testmode: whaether the game is runned in test mode
        :rtype: None
        """
        self.testmode = testmode
        self.level = Level(self.testmode)
        self.first_iteration = True

    def update_testmode(self, testmode):
        """
        Update test mode parameter.
        
        :peram bool testmode: update the status of testmode if modfied
        :rtype: None
        """

        # if theres a change in testmode, overwrite it and reset to apply change
        if self.testmode != testmode:
            self.testmode = testmode
            self.reset()

    def reset(self):
        """
        Reset Nessecary attributes in the class.

        :rtype: None
        """
        self.level = Level(self.testmode)
        self.first_iteration = True

    def run(self, dt):
        """
        Run the game state, the level

        :peram float dt: Delta Time, for movements on the screen
        :return: menu activity
        :rtype: int
        """

        # if true, load music and set up level
        if self.first_iteration:
            pygame.mixer.music.load(join("data", "sounds", "MainGame_MUSIC.mp3"))
            pygame.mixer.music.play(-1)
            self.level.setup()
            self.first_iteration = False

        return self.level.run(dt)


class WinMenu:
    def __init__(self, display_surface):
        """
        The game state for winning the game

        :peram pygame.surface.Surface display_surface: the surface for the class to operate on
        :rtype: None
        """

        # intilize text and timer
        self.win_text = Text(display_surface, None, None, 70, "You Win!", clrWhite)
        self.retry_text = Text(display_surface, None, HEIGHT // 2 + 100, 30, "Press Enter to play again", clrWhite)
        self.input_block_timer = Timer(200)
        self.first_iteration = True

    def input(self):
        """
        Get player input to determine the menu activity.

        :return: menu activity based on user input.
        :rtype: int
        """

        # Press enter to return to starting menu (-2)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN] and not self.input_block_timer.active:
            return -2
        return 0

    def reset(self):
        """
        Reset nessecary attributes in the class.

        :rtype: None
        """
        self.first_iteration = True

    def run(self):
        """
        Run the game state, win menu.

        :return: menu activity
        :rtype: int 
        """

        # if true, load music and activate time
        if self.first_iteration:
            pygame.mixer.music.load(join("data", "sounds", "Win_MUSIC.mp3"))
            pygame.mixer.music.set_volume(1.0)
            pygame.mixer.music.play(-1)
            self.input_block_timer.activate()
            self.first_iteration = False

        # run state
        self.input_block_timer.update()
        self.win_text.draw()
        self.retry_text.draw()
        return self.input()

# used for testing
if __name__ == '__main__':
    Testing = GameState()

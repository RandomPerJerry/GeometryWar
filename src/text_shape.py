from settings import *
from timer import Timer

class Text:
    def __init__(self, surf, x, y, size : int, text : str, colour : tuple, allign = "center"):
        """
        Class for creating text objects

        :param pygame.Surface surf: The surface to draw the text on
        :param int x: The x position of the text
        :param int y: The y position of the text
        :param int size: The size of the text
        :param str text: The text to display
        :param tuple[int, int, int] colour: The colour of the text
        :param str allign: The allignment of the text

        :rtype: None
        """

        # setting up the text object
        self.surf = surf
        self.x = x
        self.y = y
        self.colour = colour
        self.size = size
        self.text = text
        self.allign = allign
        self.font = pygame.font.SysFont("", self.size)

   

    def change_text(self, text):
        """
        Change the text of the text object

        :param str text: The new text to display
        :rtype: None
        """
        self.text = text
    
    def draw(self):
        """
        Draw the text object on the surface

        :rtype: None
        """

        text = self.font.render(self.text, True, self.colour)

        # if x and y are not set, set them to the center of the screen (used to simplify the class)
        if not self.x:
            self.x = WIDTH//2

        if not self.y:
            self.y = HEIGHT//2

        # draw the text
        rect = text.get_rect()
        setattr(rect, self.allign, (self.x, self.y))
        self.surf.blit(text, rect)

class HealthBar:
    def __init__(self, surf, x, y, health, h, maxhealth, barwidth, colour):
        """
        Class for creating health bars

        :param pygame.Surface surf: The surface to draw the health bar on
        :param int x: The x position of the health bar
        :param int y: The y position of the health bar
        :param int health: The current health of the object
        :param int h: The height of the health bar
        :param int maxhealth: The maximum health of the object
        :param int barwidth: The width of the health bar
        :param tuple[int, int, int] colour: The colour of the health bar

        :rtype: None
        """

        # setting up the health bar
        self.surf = surf
        self.x = x
        self.y = y
        self.health = health
        self.maxhealth = maxhealth
        self.height = h
        self.barwidth = barwidth
        self.colour = colour

    def update_hp(self, health):
        """
        Update the health of the health bar

        :param int health: The new health of the object
        :rtype: None
        """

        self.health = health
        
    def draw(self):
        """
        Draw the health bar on the surface

        :rtype: None
        """
        display_health = self.health/self.maxhealth * self.barwidth

        pygame.draw.rect(self.surf, "BLACK", (self.x - 10, self.y - 10, self.barwidth + 20, self.height + 20), 0) # draw the background
        pygame.draw.rect(self.surf, self.colour, (self.x - 5, self.y - 5, display_health + 5, self.height + 10), 0) # draw the health bar
        pygame.draw.rect(self.surf, self.colour, (self.x - 5, self.y - 5, self.barwidth + 10, self.height + 10), 5) # draw the border

class Button:
    def __init__(self, surf, x, y, w, h, allign = "center"):
        """
        Class for creating buttons

        :param pygame.Surface surf: The surface to draw the button on
        :param int x: The x position of the button
        :param int y: The y position of the button
        :param int w: The width of the button
        :param int h: The height of the button
        :param str allign: The allignment of the button

        :rtype: None
        """

        # setting up the button
        self.surf = surf
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.allign = allign

        self.state = False
        self.click_cooldown = Timer(200)

        self.button = pygame.rect.Rect(self.x, self.y, self.w, self.h)
        setattr(self.button, self.allign, (self.x, self.y)) # set the allignment of the button

    def input(self):
        """
        Get the player inputs for the button to function

        :rtype: None
        """

        # get input
        mouse_pos = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        # check if the button is clicked
        if not self.click_cooldown.active and self.button.collidepoint(mouse_pos):
            if click[0]:
                # Flip the state value
                self.state = not self.state
                self.click_cooldown.activate()

    def update(self):
        """
        Update the button

        :rtype: None
        """
        self.input()
        self.click_cooldown.update()

        border_color = clrWhite  # Change this to the color you want for the border
        border_thickness = 5  # Change this to the thickness you want for the border

        # Draw the border
        pygame.draw.rect(self.surf, border_color, self.button)

        # Create a smaller rectangle for the fill
        fill_rect = self.button.inflate(-border_thickness * 2, -border_thickness * 2)

        # Choose the fill color based on the state
        if self.state:
            fill_color = clrGreen
        else:
            fill_color = clrRed

        # Draw the fill
        pygame.draw.rect(self.surf, fill_color, fill_rect)




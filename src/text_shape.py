from settings import *

class Text:
    def __init__(self, surf, x, y, size, text, colour):
        #Pre: Requires parameters for message
        #Post: Uses parameters to set variables
        self.surf = surf
        self.x = x
        self.y = y
        self.colour = colour
        self.size = size
        self.text = text
        self.font = pygame.font.SysFont("Segoe", self.size)

    def change_text(self, text):
        self.text = text
    
    def draw(self):
        #Pre: Function called, setup variables created
        #Post: Blits message onto pygame screen
        text = self.font.render(f"{self.text}%", True, self.colour)
        iTextWidth = text.get_width()
        iTextHeight = text.get_height()
        self.surf.blit(text, (self.x - (iTextWidth // 2), self.y - (iTextHeight // 2) ) )

class HealthBar:
    def __init__(self, surf, x, y, health, h, maxhealth, barwidth, colour):
        #Pre: Parameters for variables
        #Post: Gives local variables values from function call
        self.surf = surf
        self.x = x
        self.y = y
        self.health = health
        self.maxhealth = maxhealth
        self.height = h
        self.barwidth = barwidth
        self.colour = colour

    def update_hp(self, health):
        self.health = health
        
    def draw(self):
        #Pre: Function is called and setup variables have values
        #Post: Draws square / rectangle onto screen with set variables
        display_health = self.health/self.maxhealth * self.barwidth

        pygame.draw.rect(self.surf, "BLACK", (self.x - 10, self.y - 10, self.barwidth + 20, self.height + 20), 0)
        pygame.draw.rect(self.surf, self.colour, (self.x, self.y, display_health, self.height), 0)
        pygame.draw.rect(self.surf, self.colour, (self.x - 5, self.y - 5, self.barwidth + 10, self.height + 10), 5)
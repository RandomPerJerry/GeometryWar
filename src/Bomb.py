from settings import *

class clsBomb(pygame.sprite.Sprite):
    def __init__(self, pos, radius, groups = None):
        
        super().__init__(groups)
        self.radius = radius
        self.pos = pos

        self.thickness = 1

        self.image = pygame.Surface((2*radius, 2*radius), pygame.SRCALPHA)
        pygame.draw.circle(self.image, clrWhite, (radius, radius), radius, self.thickness)

        self.rect = self.image.get_frect(center = (self.pos))

    def explode(self):
        if self.thickness < 30:
            self.thickness += 1

        self.radius += 5

        if self.radius >= 300:
            self.kill()

        self.image = pygame.Surface((2*self.radius, 2*self.radius), pygame.SRCALPHA)
        pygame.draw.circle(self.image, clrWhite, (self.radius, self.radius), self.radius, self.thickness)
        self.rect = self.image.get_frect(center = (self.pos))

    def update(self):
        self.explode()

    

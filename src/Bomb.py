from settings import *

class clsBomb(pygame.sprite.Sprite):
    def __init__(self, pos, radius, groups = None):
        
        super().__init__(groups.all_sprites, groups.bomb_sprites)
        self.radius = radius
        self.pos = pos

        self.thickness = 1
        self.growthspeed = 500
        self.alpha = 255

        self.image = pygame.Surface((2*radius, 2*radius), pygame.SRCALPHA)
        pygame.draw.circle(self.image, clrWhite, (radius, radius), radius, self.thickness)
        self.image_copy = self.image.copy()

        self.rect = self.image.get_frect(center = (self.pos))

    def explode(self, dt):
        if self.thickness < 30:
            self.thickness += (self.growthspeed/5) * dt

        self.radius += self.growthspeed * dt

        if self.radius >= 150:
            self.alpha = max(0, self.alpha -10)  # alpha should never be < 0.
            self.growthspeed = 80

        if self.alpha <= 0:
            self.kill()

        self.image = pygame.Surface((2*self.radius, 2*self.radius), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (clrWhite[0], clrWhite[1], clrWhite[2], self.alpha), (self.radius, self.radius), self.radius, int(self.thickness))
        self.rect = self.image.get_frect(center = (self.pos))


    def update(self, dt):
        self.explode(dt)

# # # Create a new surface with per-pixel alpha
# temp_surface = pygame.Surface((2*self.radius, 2*self.radius), pygame.SRCALPHA)

# # Draw the circle on the new surface
# pygame.draw.circle(temp_surface, (clrWhite[0], clrWhite[1], clrWhite[2], alpha), (self.radius, self.radius), self.radius, int(self.thickness))

# # Blit the new surface onto the original one
# self.image.blit(temp_surface, (0, 0))
    

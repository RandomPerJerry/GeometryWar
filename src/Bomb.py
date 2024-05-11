from settings import *

class Bomb(pygame.sprite.Sprite):
    def __init__(self, pos, radius, groups = None):
        """
        Initialize the bomb object.

        :param tuple pos: The position of the bomb
        :param int radius: The radius of the bomb
        :param pygame.sprite.Group group: The group to add the bomb to
        :rtype: None
        """

        super().__init__(groups.all_sprites, groups.bomb_sprites)

        # create the bomb sprite
        self.radius = radius
        self.pos = pos

        self.thickness = 1
        self.growthspeed = 500
        self.alpha = 255 # 255 is the maximum alpha value, used for transparency

        self.image = pygame.Surface((2*radius, 2*radius), pygame.SRCALPHA)
        pygame.draw.circle(self.image, clrWhite, (radius, radius), radius, self.thickness)
        self.image_copy = self.image.copy()

        self.rect = self.image.get_frect(center = (self.pos))

    def explode(self, dt):
        """
        Explode the bomb.

        :param float dt: Delta time, used for sprite movemets
        :rtype: None
        """

        # Increase the thickness of the bomb and the radius
        if self.thickness < 30:
            self.thickness += (self.growthspeed/5) * dt

        self.radius += self.growthspeed * dt

        # Decrease the alpha value of the bomb, lower growth speed when reaching 150 radius
        if self.radius >= 150:
            self.alpha = max(0, self.alpha -10)  # alpha should never be < 0.
            self.growthspeed = 80

        # If the alpha value is 0, kill the bomb
        if self.alpha <= 0:
            self.kill()

        # Create a new surface with per-pixel alpha
        self.image = pygame.Surface((2*self.radius, 2*self.radius), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (clrWhite[0], clrWhite[1], clrWhite[2], self.alpha), (self.radius, self.radius), self.radius, int(self.thickness))
        self.rect = self.image.get_frect(center = (self.pos))


    def update(self, dt):
        """
        Update the bomb.

        :param float dt: Delta time, used for sprite movemets
        :rtype: None
        """

        self.explode(dt)

    

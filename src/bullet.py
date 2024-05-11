from settings import *

class bullet(pygame.sprite.Sprite):
    def __init__(self, pos, angle, radius, group = None):
        """
        Initialize the bullet object.

        :param tuple pos: The position of the bullet
        :param float angle: The angle of the bullet
        :param int radius: The radius of the bullet
        :param pygame.sprite.Group group: The group to add the bullet to
        :rtype: None
        """

        super().__init__(group.all_sprites, group.bullet_sprites)

        # create the bullet sprite
        self.image = pygame.Surface((2*radius, 2*radius), pygame.SRCALPHA)
        pygame.draw.circle(self.image, clrWhite, (radius, radius), radius)
        self.rect = self.image.get_frect(center = pos)

        self.group = group

        # set the angle and speed of the bullet
        self.angle = angle
        self.speed = 25
        self.direction = vector()
        self.direction.from_polar((self.speed, self.angle))

    def move(self, dt):
        """
        Move the bullet based on the direction and speed.

        :param float dt: Delta time, used for sprite movemets
        :rtype: None
        """
        self.rect.center += self.direction * self.speed * dt

    def update(self, dt):
        """
        Update the bullet.

        :param float dt: Delta time, used for sprite movemets
        :rtype: None
        """
        self.move(dt)
        if self.rect.bottom < 0 or self.rect.top > HEIGHT or self.rect.right < 0 or self.rect.left > WIDTH:
            self.kill()



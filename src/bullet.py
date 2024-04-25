from settings import *

class bullet(pygame.sprite.Sprite):
    def __init__(self, pos, angle, radius, group = None):

        super().__init__(group)

        self.image = pygame.Surface((2*radius, 2*radius), pygame.SRCALPHA)
        pygame.draw.circle(self.image, clrWhite, (radius, radius), radius)
        self.rect = self.image.get_frect(center = pos)

        self.group = group

        self.angle = angle
        self.speed = 10
        self.direction = vector()
        self.direction.from_polar((self.speed, self.angle))

    def move(self):
        self.rect.center += self.direction

    def update(self):
        self.move()
        if self.rect.bottom < 0 or self.rect.top > winHeight or self.rect.right < 0 or self.rect.left > winWidth:
            self.kill()



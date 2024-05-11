from settings import *

# collection of spritegoups, or else classes will need too much perameters.
class SpriteGroups:
    def __init__(self):
        """
        Initialize the sprite groups.

        :rtype: None
        """
        self.all_sprites = pygame.sprite.Group()
        self.bullet_sprites = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()
        self.bomb_sprites = pygame.sprite.Group()
        self.gravity_ball_sprites = pygame.sprite.Group()
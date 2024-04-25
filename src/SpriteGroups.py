from settings import *

class SpriteGroups:
    def __init__(self):
        self.all_sprites = pygame.sprite.Group()
        self.player_sprites = pygame.sprite.GroupSingle()  # GroupSingle ensures there's only one player
        self.bullet_sprites = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()
        self.bomb_sprites = pygame.sprite.Group()
        self.gravity_ball_sprites = pygame.sprite.Group()
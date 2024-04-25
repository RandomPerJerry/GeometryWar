from settings import *
import math

class enemy(pygame.sprite.Sprite):
    def __init__(self, pos, speed = 5, groups = None):
        super().__init__(groups.all_sprites, groups.enemy_sprites)
        #groups = None, bullet_sprites = None, bomb_sprites = None
        self.bullet_sprites = groups.bullet_sprites
        self.bomb_sprites = groups.bomb_sprites

        self.pos = pos
        self.image = pygame.image.load(join("data", "grunt.png"))
        self.image_copy = self.image.copy()
        self.rect = self.image.get_rect(topleft = self.pos)


        self.player_pos = (0, 0)

        self.angle = 0
        self.determine_vector = vector()
        self.direction = vector()
        self.speed = speed
    
    def movement(self):
        self.determine_vector = vector(self.player_pos[0] - self.rect.centerx, self.player_pos[1] - self.rect.centery)
        self.direction = self.determine_vector.normalize() if self.determine_vector else self.determine_vector
        self.rect.center += self.direction * self.speed

    def turn(self):
        rel_x, rel_y = self.player_pos[0] - self.rect.centerx, self.player_pos[1] - self.rect.centery
        self.angle = (180 / math.pi) * -math.atan2(rel_y, rel_x)
        self.image = pygame.transform.rotate(self.image_copy, self.angle)
        self.rect = self.image.get_rect(center = self.rect.center)

    def collision(self):
        for bullet in self.bullet_sprites:
            if self.rect.colliderect(bullet.rect):
                self.kill()
                bullet.kill()

        for bomb in self.bomb_sprites:
            if self.rect.colliderect(bomb.rect):
                self.kill()

    def update_player_pos(self, pos):
        self.player_pos = pos  
            
    
    def update(self):
        self.movement()
        self.collision()
        self.turn()


    

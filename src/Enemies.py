from settings import *
from timer import Timer
import math

class enemy(pygame.sprite.Sprite):
    def __init__(self, pos, health, speed = 5, dash = 5000, groups = None):
        super().__init__(groups.all_sprites, groups.enemy_sprites)
        #groups = None, bullet_sprites = None, bomb_sprites = None
        self.group = groups

        self.explosion_list = []

        self.pos = pos
        self.image = pygame.image.load(join("data", "grunt.png"))
        self.image_copy = self.image.copy()
        self.rect = self.image.get_frect(topleft = self.pos)


        self.player_pos = (0, 0)

        self.angle = 0
        self.determine_vector = vector()
        self.direction = vector()
        self.speed = speed
        self.health = health

        self.dash_multiplier = 1

        self.timer = {
            "dash" : Timer(dash),
            "dash_duration" : Timer(70)
        }

    
    def movement(self, dt):
        self.determine_vector = vector(self.player_pos[0] - self.rect.centerx, self.player_pos[1] - self.rect.centery)

        self.direction = self.determine_vector.normalize() if self.determine_vector else self.determine_vector

        if self.timer["dash"].active == False:
            self.timer["dash"].activate()
            self.timer["dash_duration"].activate()
            self.dash_multiplier = 4

        if self.timer["dash_duration"].active == False and self.timer["dash"].active:
            self.dash_multiplier = 1
 
        self.rect.center += self.direction * self.speed * self.dash_multiplier * dt 

    def turn(self):
        rel_x, rel_y = self.player_pos[0] - self.rect.centerx, self.player_pos[1] - self.rect.centery
        self.angle = (180 / math.pi) * -math.atan2(rel_y, rel_x)
        self.image = pygame.transform.rotate(self.image_copy, self.angle)
        self.rect = self.image.get_frect(center = self.rect.center)

    def collision(self):
        for bullet in self.group.bullet_sprites:
            if self.rect.colliderect(bullet.rect):
                self.health -= 1
                bullet.kill()

        for bomb in self.group.bomb_sprites:
            if self.rect.colliderect(bomb.rect) and bomb not in self.explosion_list:
                self.explosion_list.append(bomb)
                self.health -= 10

        if self.health <= 0:
            self.kill()

    def update_player_pos(self, pos):
        self.player_pos = pos  

    def update_timers(self):
        for timer in self.timer.values():
            timer.update()
            
    
    def update(self, dt):
        self.update_timers()
        self.movement(dt)
        self.collision()
        self.turn()


    

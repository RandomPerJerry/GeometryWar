from settings import *
from bullet import bullet
from Bomb import clsBomb
from timer import Timer
import math

# Player class
class player(pygame.sprite.Sprite):

    def __init__(self, pos, groups = None):

        #bullet_sprite = None, enemy_sprites = None, bomb_sprites = None
        super().__init__(groups.all_sprites)

        self.group = groups

        self.pos = pos
        self.image = pygame.image.load(join("data", "ship.png"))
        self.image_copy = self.image.copy()
        self.rect = self.image.get_rect(topleft = self.pos)
        self.old_rect = self.rect.copy()

        self.health = 100

        self.angle = 0
        self.direction = vector()
        self.speed = 500

        self.dash_multiplier = 1

        self.timer = {
            "shoot" : Timer(200),
            "bomb" : Timer(500),
            "dash" : Timer(1000),
            "dash_duration" : Timer(70)
        }

    def input(self):
        keys = pygame.key.get_pressed()
        input_vector = vector(0, 0)

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            input_vector.x -= 1
        
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            input_vector.x += 1

        if keys[pygame.K_UP] or keys[pygame.K_w]:
            input_vector.y -= 1

        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            input_vector.y += 1

        self.direction = input_vector.normalize() if input_vector else input_vector

        if keys[pygame.K_LSHIFT] and self.timer["dash"].active == False:
            self.dash_multiplier = 5
            self.timer["dash"].activate()
            self.timer["dash_duration"].activate()

        if self.timer["dash"].active and self.timer["dash_duration"].active == False:
            self.dash_multiplier = 1

        if keys[pygame.K_SPACE] and self.timer["bomb"].active == False:
            clsBomb(self.rect.center, 10, self.group)
            self.timer["bomb"].activate()

        if pygame.mouse.get_pressed()[0] and self.timer["shoot"].active == False:
            bullet(self.rect.center, -self.angle, 5, self.group)
            self.timer["shoot"].activate()

    def collision(self):
        for enemy in self.group.enemy_sprites:
            if self.rect.colliderect(enemy.rect):
                self.health -= 1

                
    def movement(self, dt):
        self.rect.center += self.direction * self.speed * self.dash_multiplier * dt

        if self.rect.left < 0:
            self.rect.center = self.old_rect.center

        if self.rect.right > winWidth:
            self.rect.center = self.old_rect.center
        
        if self.rect.top < 0:
            self.rect.center = self.old_rect.center

        if self.rect.bottom > winHeight:
            self.rect.center = self.old_rect.center

    def get_pos(self):
        return self.rect.center

    def ship_rotation(self):
        
        mouseX, mouseY = pygame.mouse.get_pos()
        rel_x, rel_y = mouseX - self.rect.centerx, mouseY - self.rect.centery
        self.angle = (180 / math.pi) * -math.atan2(rel_y, rel_x)
        self.image = pygame.transform.rotate(self.image_copy, self.angle)
        self.rect = self.image.get_rect(center = self.rect.center)

    def update_timers(self):
        for timer in self.timer.values():
            timer.update()  

    def update(self, dt):
        self.old_rect = self.rect.copy()
        self.collision()
        self.update_timers()
        self.input()
        self.movement(dt)
        self.ship_rotation()
        


    




    
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
        self.rect = self.image.get_frect(topleft = self.pos)
        self.old_rect = self.rect.copy()

        self.shoot_sound = pygame.mixer.Sound(join("data", "sounds", "LaserGun_SFX.mp3"))
        self.shoot_sound.set_volume(0.1)

        self.bomb_sound = pygame.mixer.Sound(join("data", "sounds", "Bomb_SFX.mp3"))

        self.health = 100

        self.angle = 0
        self.direction = vector()
        self.speed = 500

        self.gravity_pull = vector(0, 0)
        
        self.dash_multiplier = 1

        self.timer = {
            "shoot" : Timer(200),
            "bomb" : Timer(20000),
            "dash" : Timer(3000),
            "dash_duration" : Timer(70),
            "invincible" : Timer(200)
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
            self.bomb_sound.play()

        if pygame.mouse.get_pressed()[0] and self.timer["shoot"].active == False:
            bullet(self.rect.center, -self.angle, 5, self.group)
            self.timer["shoot"].activate()
            self.shoot_sound.play()

    def collision(self):

        if not self.timer["invincible"].active:
            for enemy in self.group.enemy_sprites:
                if self.rect.colliderect(enemy.hitbox):
                    self.health -= 5
                    self.timer["invincible"].activate()

        pull_vector = vector(0, 0)

        for gravity_ball in self.group.gravity_ball_sprites:
            if self.rect.colliderect(gravity_ball.gravity_hitbox):
                pull_vector = vector(gravity_ball.rect.center[0] - self.rect.centerx, 
                                        gravity_ball.rect.center[1] - self.rect.centery)
                if self.rect.colliderect(gravity_ball.hitbox) and not self.timer["invincible"].active:
                    self.health -= 10
                    self.timer["invincible"].activate()
                
        self.gravity_pull = pull_vector.normalize() if pull_vector else pull_vector

    def check_health(self):
        if self.health < 0:
            self.health = 0

        elif self.health > 100:
            self.health = 100
        
        return self.health
           
    def movement(self, dt):

        self.rect.center += self.direction * self.speed * self.dash_multiplier * dt
        self.rect.center += self.gravity_pull * 100 * dt

        if self.rect.left < 0:
            self.rect.left = 0

        if self.rect.right > winWidth:
            self.rect.right = winWidth
        
        if self.rect.top < 0:
            self.rect.top = 0

        if self.rect.bottom > winHeight:
            self.rect.bottom = winHeight

    def get_pos(self):
        return self.rect.center

    def ship_rotation(self):
        
        mouseX, mouseY = pygame.mouse.get_pos()
        rel_x, rel_y = mouseX - self.rect.centerx, mouseY - self.rect.centery
        self.angle = (180 / math.pi) * -math.atan2(rel_y, rel_x)
        self.image = pygame.transform.rotate(self.image_copy, self.angle)
        self.rect = self.image.get_frect(center = self.rect.center)

    def update_timers(self):
        for timer in self.timer.values():
            timer.update()  

    def update(self, dt):
        self.old_rect = self.rect.copy()
        self.direction = vector()
        self.collision()
        self.check_health()
        self.update_timers()
        self.input()
        self.movement(dt)
        self.ship_rotation()
        


    




    
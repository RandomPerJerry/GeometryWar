from settings import *
from timer import Timer
import math

class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, health, speed = 5, dash = 5000, groups = None):
        """
        Initilze a enemy in the game

        :peram tuple[int, int] pos: where the enemy is being spawned
        :peram int health: the emount of health the enemy has
        :peram int speed: the speed the enemy us moving at
        :peram int dash: the cooldown of the enemy dash
        :peram SpriteGroups groups: collection of sprite groups in the game
        :rtype: None 
        """
        super().__init__(groups.all_sprites, groups.enemy_sprites)
        #groups = None, bullet_sprites = None, bomb_sprites = None
        self.group = groups

        self.explosion_list = [] # remembering the bombs that damaged the enemy

        # setting up the enemy
        self.pos = pos
        self.image = pygame.image.load(join("data", "grunt.png"))
        self.image_copy = self.image.copy()
        self.rect = self.image.get_frect(center = self.pos)
        self.hitbox = self.rect.inflate(-20, -20)

        self.health = health

        # tracking the player   
        self.player_pos = (0, 0)

        # setting up the movement
        self.angle = 0
        self.determine_vector = vector()
        self.direction = vector()
        self.speed = speed
    

        self.dash_multiplier = 1

        # setting up the timers
        self.timer = {
            "dash" : Timer(dash),
            "dash_duration" : Timer(70),
            "start_cooldown" : Timer((dash - 1000))
        }
        self.timer["start_cooldown"].activate()


    
    def movement(self, dt):
        """
        Move the enemy towards the player

        :peram float dt: the change in time
        :rtype: None
        """

        # move towards the player
        self.determine_vector = vector(self.player_pos[0] - self.rect.centerx, self.player_pos[1] - self.rect.centery)

        self.direction = self.determine_vector.normalize() if self.determine_vector else self.determine_vector

        # dash towards the player
        if self.timer["dash"].active == False and self.timer["start_cooldown"].active == False:
            self.timer["dash"].activate()
            self.timer["dash_duration"].activate()
            self.dash_multiplier = 4

        # duration of the dash
        if self.timer["dash_duration"].active == False and self.timer["dash"].active:
            self.dash_multiplier = 1
 
        # update the position of the enemy
        self.rect.center += self.direction * self.speed * self.dash_multiplier * dt 
        self.hitbox.center = self.rect.center

    def turn(self):
        """
        Turn the enemy towards the player

        :rtype: None
        """

        # use trigonometry to determine the angle the enemy should be facing
        rel_x, rel_y = self.player_pos[0] - self.rect.centerx, self.player_pos[1] - self.rect.centery
        self.angle = (180 / math.pi) * -math.atan2(rel_y, rel_x)
        self.image = pygame.transform.rotate(self.image_copy, self.angle)
        self.rect = self.image.get_frect(center = self.rect.center)

    def collision(self):
        """
        Check for collision with the player bullets and bombs

        :rtype: None
        """

        # check for collision with the player bullets
        for bullet in self.group.bullet_sprites:
            if self.rect.colliderect(bullet.rect):
                self.health -= 1
                bullet.kill()

        # check for collision with the player bombs
        for bomb in self.group.bomb_sprites:
            if self.rect.colliderect(bomb.rect) and bomb not in self.explosion_list:
                self.explosion_list.append(bomb)
                self.health -= 10

        # check for collision with the player
        if self.health <= 0:
            self.kill()

    def update_player_pos(self, pos):
        """
        Update the position of the player

        :peram tuple[int, int] pos: the position of the player
        :rtype: None
        """
        self.player_pos = pos  

    def update_timers(self):
        """
        Update the timers of the enemy

        :rtype: None
        """
        for timer in self.timer.values():
            timer.update()
            
    
    def update(self, dt):
        """
        Update the enemy

        :peram float dt: the change in time
        :rtype: None
        """
        self.update_timers()
        self.movement(dt)
        self.collision()
        self.turn()


    

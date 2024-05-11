from settings import *
from bullet import bullet
from bomb import Bomb
from timer import Timer
import math

# Player class
class Player(pygame.sprite.Sprite):

    def __init__(self, pos, testmode, groups = None):

        """
        Initialize the player class.

        :peram tuple[int, int] pos: A tuple (x, y) representing the initial position of the player on the screen.
        :peram bool testmode: wheather or not the game is in test mode. 
        :peram SpriteGroups groups: A collection of all pygame.sprite.Group in the game.
        """

        super().__init__(groups.all_sprites)

        # intilize attributes
        self.group = groups
        self.pos = pos
        self.image = pygame.image.load(join("data", "ship.png"))
        self.image_copy = self.image.copy()
        self.rect = self.image.get_frect(topleft = self.pos)
        self.old_rect = self.rect.copy()

        # load sound
        self.shoot_sound = pygame.mixer.Sound(join("data", "sounds", "LaserGun_SFX.mp3"))
        self.shoot_sound.set_volume(0.1)

        self.bomb_sound = pygame.mixer.Sound(join("data", "sounds", "Bomb_SFX.mp3"))

        self.max_health = 1000000 if testmode else 100 # if test mode, you basically have inf hp
        self.health = self.max_health

        self.angle = 0
        self.direction = vector() # The direction for "intended movements"
        self.speed = 500

        self.gravity_pull = vector(0, 0) # direction for gravity pull
        
        self.dash_multiplier = 1

        # Timmers for functionalities
        self.timer = {
            "shoot" : Timer(200),
            "bomb" : Timer(20000),
            "dash" : Timer(3000),
            "dash_duration" : Timer(70),
            "invincible" : Timer(200)
        }

    def input(self):
        """
        Get the player inputs and transform to data for the player classs

        rtype: None
        """

        keys = pygame.key.get_pressed()

        # determining the players movement
        input_vector = vector(0, 0)

        # Determining direction movement
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            input_vector.x -= 1
        
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            input_vector.x += 1

        if keys[pygame.K_UP] or keys[pygame.K_w]:
            input_vector.y -= 1

        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            input_vector.y += 1

        self.direction = input_vector.normalize() if input_vector else input_vector # if no movement, dont normalize

        # player use dash if cooldown is over
        if keys[pygame.K_LSHIFT] and self.timer["dash"].active == False:
            self.dash_multiplier = 5
            self.timer["dash"].activate()
            self.timer["dash_duration"].activate()

        # deactivate dash when over
        if self.timer["dash"].active and self.timer["dash_duration"].active == False:
            self.dash_multiplier = 1

        # player use bomb if cooldown is over
        if keys[pygame.K_SPACE] and self.timer["bomb"].active == False:
            Bomb(self.rect.center, 10, self.group)
            self.timer["bomb"].activate()
            self.bomb_sound.play()

        # fire bullets if cooldown is over
        if pygame.mouse.get_pressed()[0] and self.timer["shoot"].active == False:
            bullet(self.rect.center, -self.angle, 5, self.group)
            self.timer["shoot"].activate()
            self.shoot_sound.play()

    def collision(self):
        """
        check for collisions from enemy sprites and gravity ball sprites

        rtype: None
        """

        # enemy collision
        if not self.timer["invincible"].active:
            for enemy in self.group.enemy_sprites:
                if self.rect.colliderect(enemy.hitbox):
                    self.health -= 5
                    self.timer["invincible"].activate()

        pull_vector = vector(0, 0)

        # gravity ball collision
        for gravity_ball in self.group.gravity_ball_sprites:

            # get pulled if collide with outer gravity ball ring
            if self.rect.colliderect(gravity_ball.gravity_hitbox):

                # determine pull direction
                pull_vector = vector(gravity_ball.rect.center[0] - self.rect.centerx, 
                                        gravity_ball.rect.center[1] - self.rect.centery)
                
                # Take damage if collide with inner ring
                if self.rect.colliderect(gravity_ball.hitbox) and not self.timer["invincible"].active:
                    self.health -= 10
                    self.timer["invincible"].activate()
            
        # apply change
        self.gravity_pull = pull_vector.normalize() if pull_vector else pull_vector

    def check_health(self):
        """
        Get player health, while also preventing abnormal health values from appearing

        :return: player health
        :rtype: int
        """

        # if player hp smaller than 0, it becomes 0
        if self.health < 0:
            self.health = 0

        # if player hp is bigger than intended max hp, become max hp
        elif self.health > self.max_health:
            self.health = self.max_health
        
        return self.health
           
    def movement(self, dt):

        """
        apply the movements to the player depending on direction

        :peram float dt: delta time, used for movements
        :rtype: None
        """

        # move player
        self.rect.center += self.direction * self.speed * self.dash_multiplier * dt
        self.rect.center += self.gravity_pull * 100 * dt

        # prevent player from exiting the screen
        if self.rect.left < 0:
            self.rect.left = 0

        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        
        if self.rect.top < 0:
            self.rect.top = 0

        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT

    def get_pos(self):
        """
        get the players cordinates (x, y)

        :return: player's cordinate 
        :rtype: tuple [int, int]
        """
        return self.rect.center

    def ship_rotation(self):
        """
        rotate the player sprite, so it always faces the mouse

        :rtype: None
        """

        # Knowing ur cord and target cord, get angle using triganometry
        mouseX, mouseY = pygame.mouse.get_pos()
        rel_x, rel_y = mouseX - self.rect.centerx, mouseY - self.rect.centery
        self.angle = (180 / math.pi) * -math.atan2(rel_y, rel_x)
        self.image = pygame.transform.rotate(self.image_copy, self.angle)
        self.rect = self.image.get_frect(center = self.rect.center)

    def update_timers(self):
        """
        update the timers in the class

        :rtype: None
        """

        for timer in self.timer.values():
            timer.update()  

    def update(self, dt):
        """
        call nessecary methods to update the player status

        :peram float dt: delta time, used for movements
        :rtype: None
        """

        self.old_rect = self.rect.copy()
        self.direction = vector()
        self.collision()
        self.check_health()
        self.update_timers()
        self.input()
        self.movement(dt)
        self.ship_rotation()
        


    




    
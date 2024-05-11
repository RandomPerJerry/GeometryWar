from settings import *
from timer import Timer

class GravityBallCenter(pygame.sprite.Sprite):
    def __init__(self, pos, width, height, groups = None):
        """
        the class for gravity balls

        :peram tuple [int, int] pos: the cordinate the gravityball spawns in.
        :peram int width: width of the ball
        :peram int height: height of the ball
        :groups SpriteGroups groups: collection of the sprite groups
        :rtype: None
        """

        super().__init__(groups.all_sprites, groups.gravity_ball_sprites)

        # intilize attributes
        self.pos = pos
        self.targetwidth = width
        self.targetheight = height
        self.group = groups

        # starting size of the balls
        self.bigcurrentwidth = 15
        self.bigcurrentheight = 15
        self.smallcurrentwidth = 5
        self.smallcurrentheight = 5

        # images
        self.image1 = pygame.image.load(join("data", "gravball.png"))
        self.image2 = pygame.image.load(join("data", "gravballback.png"))

        self.image1_copy = self.image1.copy()
        self.image2_copy = self.image2.copy()

        self.image1 = pygame.transform.scale(self.image1, (self.smallcurrentheight, self.smallcurrentheight))
        self.image2 = pygame.transform.scale(self.image2, (self.bigcurrentwidth, self.bigcurrentheight))

        # Create a new Surface that is as big as the larger of the two images
        self.image = pygame.Surface((self.targetwidth*3 + 20, self.targetheight*3 + 20), pygame.SRCALPHA) 
            
        # Calculate the top-left position of each image such that they are centered on the Surface
        image_center = (self.image.get_width() // 2, self.image.get_height() // 2)
        self.image1_pos = (image_center[0] - self.image1.get_width() // 2, image_center[1] - self.image1.get_height() // 2)
        self.image2_pos = (image_center[0] - self.image2.get_width() // 2, image_center[1] - self.image2.get_height() // 2)

        # Draw each image onto the Surface at the calculated position
        self.image.blit(self.image1, self.image1_pos)
        self.image.blit(self.image2, self.image2_pos)

        # update rects
        self.rect = self.image.get_frect(center = self.pos)
        self.hitbox = self.image1.get_frect(center = self.pos)
        self.gravity_hitbox = self.image2.get_frect(center = self.pos)

        # timers
        self.timer = {"Invincible" : Timer(1000),
                      "Regrow" : Timer(5000)}

        self.timer["Invincible"].activate()

        # other attributes
        self.grow_speed = 30
        self.bomb_hit = []

        self.dying = False
        self.keepgrow = True
        self.needupdate = False

    def update_timer(self):
        """
        update the timers

        :rtype: None
        """
        for timer in self.timer.values():
            timer.update()

    def check_regrow(self):
        """
        if dosent take damage for too long, regenerate the ball

        rtype: None
        """
        if not self.timer["Regrow"].active and not self.dying:
            self.keepgrow = True

    def grow(self, dt):
        """
        grows the ball

        :peram float dt: delta time, used for movements
        :rtype: None
        """

        # grows the outer ring untill the ball reaches its maximum size
        if self.bigcurrentwidth < self.targetwidth and self.bigcurrentheight < self.targetheight:

            self.bigcurrentwidth += self.grow_speed * 3 * dt
            self.bigcurrentheight += self.grow_speed * 3 * dt

            self.needupdate = True

        # grows the inner ring until the ball reaches its maximum size
        if self.smallcurrentwidth < self.targetwidth/3 and self.smallcurrentheight < self.targetheight/3:

            self.smallcurrentwidth += self.grow_speed * dt
            self.smallcurrentheight += self.grow_speed * dt

            self.needupdate = True

        else:
            self.keepgrow = False

    def collide(self):
        """
        check for nessecary collsions for the gravityball

        :rtype: None
        """
        # if ball collides with a bullet, shrinks inner circle size
        if not self.timer["Invincible"].active:
            for bullet in self.group.bullet_sprites:
                if self.hitbox.colliderect(bullet.rect):
                    self.smallcurrentwidth -= 15
                    self.smallcurrentheight -= 15

                    self.needupdate = True
                    self.keepgrow = False

                    self.timer["Regrow"].activate()

                    bullet.kill()
            
            # if ball collides with a bomb, shrinks inner circle size
            for bomb in self.group.bomb_sprites:
                if self.hitbox.colliderect(bomb.rect) and bomb not in self.bomb_hit:
                    self.smallcurrentwidth -= 60
                    self.smallcurrentheight -= 60

                    self.timer["Regrow"].activate()

                    self.needupdate = True
                    self.keepgrow = False
                    self.bomb_hit.append(bomb) # so the ball wont take damage from the same explosion
    

    def update_size(self):
        """
        display the size changes for both rings and update hitbox

        :rtype: None
        """

        # Shrink image1
        if self.smallcurrentwidth > 0 and self.smallcurrentheight > 0:
            self.image1 = pygame.transform.scale(self.image1_copy, (self.smallcurrentwidth, self.smallcurrentheight))

        # shrink image 2
        if self.bigcurrentwidth >  0 and self.bigcurrentheight > 0:
            self.image2 = pygame.transform.scale(self.image2_copy, (self.bigcurrentwidth, self.bigcurrentheight))

        # Update the hitbox
        if not self.dying:
            self.rect = self.image.get_frect(center = self.pos)
            self.hitbox = self.image1.get_frect(center = self.pos)

        self.gravity_hitbox = self.image2.get_frect(center = self.pos)

        # Clear the combined image
        self.image.fill((0, 0, 0, 0))

        # Calculate the top-left position of image1 such that it is centered on the Surface
        if not self.dying:
            self.image1_pos = (self.image.get_width() // 2 - self.image1.get_width() // 2, 
                            self.image.get_height() // 2 - self.image1.get_height() // 2)
        
        self.image2_pos = (self.image.get_width() // 2 - self.image2.get_width() // 2, 
                        self.image.get_height() // 2 - self.image2.get_height() // 2)

        # Draw image1 onto the Surface at the calculated position
        if not self.dying:
            self.image.blit(self.image1, self.image1_pos)

        # Draw image2 onto the Surface at its original position
        self.image.blit(self.image2, self.image2_pos)

        self.needupdate = False
        

    def check_death(self, dt):
        """
        if the inner ring is dead, shrink the outer ring till its also gone

        :peram float dt: delta time, for movements
        :rtype: None
        """

        if not self.timer["Invincible"].active:

            # if inner ring is dead
            if self.smallcurrentwidth < 15 or self.smallcurrentheight < 15:

                # kill the ball
                self.dying = True
                self.needupdate = True
                self.smallcurrentwidth = -1
                self.smallcurrentheight = -1
                self.bigcurrentwidth -= 200 * dt
                self.bigcurrentheight -= 200 * dt
                self.hitbox = pygame.Rect(0, 0, 0, 0)
                if self.bigcurrentwidth <= 0 or self.bigcurrentheight <= 0:
                    self.kill()

    def update(self, dt):

        """
        update the class with the methods

        :peram floar dt: delta time, used for movements
        :rtype: None
        """
        self.check_death(dt)
        self.collide()
        self.update_timer()
        self.check_regrow()

        if self.needupdate:
            self.update_size()

        if self.keepgrow:
            self.grow(dt)

    

        

        
from settings import *
from timer import Timer

class GravityBallCenter(pygame.sprite.Sprite):
    def __init__(self, pos, width, height, groups = None):
        super().__init__(groups.all_sprites, groups.gravity_ball_sprites)
        self.pos = pos
        self.targetwidth = width
        self.targetheight = height
        self.group = groups

        self.bigcurrentwidth = 15
        self.bigcurrentheight = 15
        self.smallcurrentwidth = 5
        self.smallcurrentheight = 5

        self.image1 = pygame.image.load('data/gravball.png')
        self.image2 = pygame.image.load('data/gravballback.png')

        self.image1_copy = self.image1.copy()
        self.image2_copy = self.image2.copy()

        self.image1 = pygame.transform.scale(self.image1, (self.smallcurrentheight, self.smallcurrentheight))
        self.image2 = pygame.transform.scale(self.image2, (self.bigcurrentwidth, self.bigcurrentheight))

        # Create a new Surface that is as big as the larger of the two images
        self.image = pygame.Surface((self.targetwidth*3 + 20, self.targetheight*3 + 20), pygame.SRCALPHA) 
            
        # Calculate the top-left position of each image such that they are centered on the Surface
        center = (self.image.get_width() // 2, self.image.get_height() // 2)
        self.image1_pos = (center[0] - self.image1.get_width() // 2, center[1] - self.image1.get_height() // 2)
        self.image2_pos = (center[0] - self.image2.get_width() // 2, center[1] - self.image2.get_height() // 2)

        # Draw each image onto the Surface at the calculated position
        self.image.blit(self.image1, self.image1_pos)
        self.image.blit(self.image2, self.image2_pos)

        self.rect = self.image.get_rect(center = pos)
        self.hitbox = self.image1.get_rect(center = pos)

        self.invincible = Timer(1000)
        self.invincible.activate()

        self.grow_speed = 30
        self.bomb_hit = []
        self.dying = False
        self.keepgrow = True
        self.needupdate = False


    def update(self, dt):
        self.check_death(dt)
        self.invincible.update()
        self.collide()

        if self.needupdate:
            self.update_size()

        if self.keepgrow:
            self.grow(dt)

    def grow(self, dt):

        if self.bigcurrentwidth < self.targetwidth and self.bigcurrentheight < self.targetheight:

            self.smallcurrentwidth += self.grow_speed * dt
            self.smallcurrentheight += self.grow_speed * dt
            self.bigcurrentwidth += self.grow_speed * 3 * dt
            self.bigcurrentheight += self.grow_speed * 3 * dt

            self.needupdate = True

        else:
            self.keepgrow = False

    def collide(self):
        if not self.invincible.active:
            for bullet in self.group.bullet_sprites:
                if self.hitbox.colliderect(bullet.rect):
                    self.smallcurrentwidth -= 15
                    self.smallcurrentheight -= 15

                    self.needupdate = True
                    self.keepgrow = False

                    bullet.kill()
            
            for bomb in self.group.bomb_sprites:
                if self.hitbox.colliderect(bomb.rect) and bomb not in self.bomb_hit:
                    self.smallcurrentwidth -= 60
                    self.smallcurrentheight -= 60

                    self.needupdate = True
                    self.keepgrow = False
                    self.bomb_hit.append(bomb)

    def get_center_pos(self):
        return self.rect.center

    def update_size(self):
        # Shrink image1

        if self.smallcurrentwidth > 0 and self.smallcurrentheight > 0:
            self.image1 = pygame.transform.scale(self.image1_copy, (self.smallcurrentwidth, self.smallcurrentheight))

        if self.bigcurrentwidth >  0 and self.bigcurrentheight > 0:
            self.image2 = pygame.transform.scale(self.image2_copy, (self.bigcurrentwidth, self.bigcurrentheight))

        # Update the hitbox
        if not self.dying:
            self.rect = self.image.get_rect(center = self.pos)
            self.hitbox = self.image1.get_rect(center = self.pos)

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
        if self.smallcurrentwidth < 5 or self.smallcurrentheight < 5:
            self.dying = True
            self.needupdate = True
            self.smallcurrentwidth = -1
            self.smallcurrentheight = -1
            self.bigcurrentwidth -= 60 * dt
            self.bigcurrentheight -= 60 * dt
            if self.bigcurrentwidth <= 0 or self.bigcurrentheight <= 0:
                self.kill()

    

        

        
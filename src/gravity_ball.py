from settings import *

class GravityBallCenter(pygame.sprite.Sprite):
    def __init__(self, pos, width, height, groups = None):
        super().__init__(groups.all_sprites, groups.gravity_ball_sprites)
        self.pos = pos
        self.targetwidth = width
        self.targetheight = height
        self.bullet_sprites = groups.bullet_sprites

        self.bigcurrentwidth = 10
        self.bigcurrentheight = 10
        self.smallcurrentwidth = 30
        self.smallcurrentheight = 30

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

        self.keepgrow = True
        self.needupdate = False

    def update(self):
        self.collide()
        self.check_death()

        if self.needupdate:
            self.update_size()

        if self.keepgrow:
            self.grow()

    def grow(self):

        if self.bigcurrentwidth < self.targetwidth and self.bigcurrentheight < self.targetheight:

            self.smallcurrentwidth += 10
            self.smallcurrentheight += 10
            self.bigcurrentwidth = self.smallcurrentwidth * 3
            self.bigcurrentheight = self.smallcurrentheight * 3

            self.needupdate = True

        else:
            self.keepgrow = False

    def collide(self):
        for bullet in self.bullet_sprites:
            if self.hitbox.colliderect(bullet.rect):
                self.smallcurrentwidth -= 10
                self.smallcurrentheight -= 10

                self.needupdate = True

                bullet.kill()

    def update_size(self):
        # Shrink image1


        self.image1 = pygame.transform.scale(self.image1_copy, (self.smallcurrentwidth, self.smallcurrentheight))


        self.image2 = pygame.transform.scale(self.image2_copy, (self.bigcurrentwidth, self.bigcurrentheight))

        # Update the hitbox
        self.rect = self.image.get_rect(center = self.pos)
        self.hitbox = self.image1.get_rect(center = self.pos)

        # Clear the combined image
        self.image.fill((0, 0, 0, 0))

        # Calculate the top-left position of image1 such that it is centered on the Surface
        self.image1_pos = (self.image.get_width() // 2 - self.image1.get_width() // 2, 
                        self.image.get_height() // 2 - self.image1.get_height() // 2)
        
        self.image2_pos = (self.image.get_width() // 2 - self.image2.get_width() // 2, 
                        self.image.get_height() // 2 - self.image2.get_height() // 2)

        # Draw image1 onto the Surface at the calculated position
        self.image.blit(self.image1, self.image1_pos)

        # Draw image2 onto the Surface at its original position
        self.image.blit(self.image2, self.image2_pos)

        self.needupdate = False
        

    def check_death(self):
        if self.smallcurrentwidth <= 5 or self.smallcurrentheight <= 5:
            self.needupdate = True
            self.bigcurrentwidth -= 20
            self.bigcurrentheight -= 20
            if self.bigcurrentwidth <= 0 or self.bigcurrentheight <= 0:
                self.kill()

    

        

        
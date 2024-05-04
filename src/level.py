from settings import *
from player import player 
from Enemies import enemy
from gravity_ball import GravityBallCenter
from SpriteGroups import SpriteGroups
from text_shape import HealthBar, Text
import random


class level:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()

        self.imgBackground = pygame.image.load(join("data", "background.png")).convert_alpha() #load background image
        self.imgBackgroundBehind = pygame.image.load(join("data", "background2.png")).convert_alpha()

        self.setup()

    def setup(self):

        self.level = 0

        self.SpriteGroups = SpriteGroups()
        self.player = player((winWidth/2, winHeight/2), self.SpriteGroups)
        self.healthBar = HealthBar(surf=self.display_surface, x=20, y=winHeight - 50, 
                                   health=self.player.health, h=30 , maxhealth=100, barwidth=500, colour=clrRed)
        
        self.healthText = Text(self.display_surface, 260, winHeight - 32, 50, self.player.health, clrWhite)


    def generate_enemies(self, amount):
        
        self.player.health += 10

        for _ in range(amount):
            cordinates = [(random.randint(0, winWidth), random.choice([0 - random.randint(20, 100), winHeight + random.randint(20, 100)])),
                        (random.choice([0 - random.randint(20, 100), winWidth + random.randint(20, 100)]), random.randint(0, winHeight))]
            enemy(random.choice(cordinates), 300, self.SpriteGroups)

            if len(self.SpriteGroups.gravity_ball_sprites) < 5:
                GravityBallCenter((random.randint(0, winWidth), random.randint(0, winHeight)), 300, 300, self.SpriteGroups)

    def draw_elements(self, health):
        self.healthBar.update_hp(health)
        self.healthBar.draw()
        self.healthText.change_text(health)
        self.healthText.draw()

    
    def draw_background(self):
        self.display_surface.fill(clrBlack)
        self.display_surface.blit(self.imgBackground,(0, 0))

    def next_level(self):
        self.level += 1
        self.generate_enemies(self.level * 2)

    def run(self, dt):
        self.SpriteGroups.all_sprites.update(dt)
        self.draw_background()
        self.SpriteGroups.all_sprites.draw(self.display_surface)
        self.draw_elements(self.player.health)

        for enemy in self.SpriteGroups.enemy_sprites:
            enemy.update_player_pos(self.player.get_pos())
        
        if not self.SpriteGroups.enemy_sprites and not self.SpriteGroups.gravity_ball_sprites:
            self.next_level()

        # print(self.SpriteGroups.all_sprites)
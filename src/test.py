from settings import *
from player import player 
from Enemies import enemy
from gravity_ball import GravityBallCenter
import random

class Level:
    def __init__(self, win_width, win_height):
        self.win_width = win_width
        self.win_height = win_height
        self.display_surface = pygame.display.get_surface()

        self.level = 0
        self.setup()

    def setup(self):
        self.sprite_groups = SpriteGroups()

        self.player = Player((self.win_width/2, self.win_height/2), self.sprite_groups)

        self.img_background = pygame.image.load(join("data", "background.png")).convert_alpha() #load background image
        self.img_background_behind = pygame.image.load(join("data", "background2.png")).convert_alpha()

    def generate_enemies(self, amount):
        for _ in range(amount):
            coordinates = self.generate_random_coordinates()
            Enemy(coordinates, 3, self.sprite_groups)

    def generate_gravity_balls(self, amount):
        for _ in range(amount):
            coordinates = (random.randint(0, self.win_width), random.randint(0, self.win_height))
            GravityBallCenter(coordinates, 300, 300, self.sprite_groups)

    def generate_random_coordinates(self):
        # Your existing code for generating random coordinates

    def draw_background(self):
        self.display_surface.fill(clrBlack)
        self.display_surface.blit(self.img_background,(0, 0))

    def next_level(self):
        self.level += 1
        self.generate_enemies(self.level * 2)
        self.generate_gravity_balls(self.level)

    def run(self):
        self.sprite_groups.all_sprites.update()
        self.draw_background()
        self.sprite_groups.all_sprites.draw(self.display_surface)
        print(len(self.sprite_groups.enemy_sprites))
        for enemy in self.sprite_groups.enemy_sprites:
            enemy.update_player_pos(self.player.get_pos())
        
        if not self.sprite_groups.enemy_sprites:
            self.next_level()
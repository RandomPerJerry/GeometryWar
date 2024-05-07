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
                                   health=self.player.health, h=10 , maxhealth=100, barwidth=500, colour=clrRed)

        self.boss = None
        self.bossBar = None
        self.dashtext = Text(self.display_surface, 20, winHeight - 100, 30, f"{round(self.player.timer['dash'].time_left/1000, 1)}", clrWhite)
        self.bombtext = Text(self.display_surface, 20, winHeight - 150, 30, f"{round(self.player.timer['bomb'].time_left/1000, 1)}", clrWhite)
        self.leveltext = Text(self.display_surface, 350, 20, 60, f"Level: {self.level}", clrWhite)

        self.element_list = [self.healthBar, self.dashtext, self.bombtext, self.leveltext]
 
    def draw_elements(self):
        self.healthBar.update_hp(self.player.health)
        self.leveltext.change_text(f"Level: {self.level}")
        
        if self.player.timer["dash"].active:
            self.dashtext.change_text(f"Dash: {round(self.player.timer['dash'].time_left/1000, 1)}")
        else:
            self.dashtext.change_text(f"Dash Ready")
            
        if self.player.timer["bomb"].active:
            self.bombtext.change_text(f"Bomb: {round(self.player.timer['bomb'].time_left/1000, 1)}")
        else:
            self.bombtext.change_text(f"Bomb Ready")
            
        for element in self.element_list:

            if self.level == 30:
                if self.bossBar is None:
                    self.bossBar = HealthBar(surf=self.display_surface, x=winWidth//2 - 250, y=20, 
                                             health=100, h=20 , maxhealth=100, barwidth=500, colour=clrRed)
                    self.element_list.append(self.bossBar)
                    self.element_list.remove(self.leveltext)
                else:
                    self.bossBar.update_hp(self.boss.health)

            element.draw()

    def update_enemy_player_pos(self):
        for enemy in self.SpriteGroups.enemy_sprites:
            enemy.update_player_pos(self.player.rect.center)

    def draw_background(self):
        self.display_surface.fill(clrBlack)
        self.display_surface.blit(self.imgBackground,(0, 0))

    def generate_spawn_cords(self):
        # Generate random off-screen x-coordinate
        x = random.choice([
            random.randint(-100, -20),
            random.randint(winWidth + 20, winWidth + 100)
        ])

        # Generate random off-screen y-coordinate
        y = random.choice([
            random.randint(-100, -20),
            random.randint(winHeight + 20, winHeight + 100)
        ])

        # Randomly choose whether to use off-screen x or y
        if random.choice([True, False]):
            x = random.randint(0, winWidth)
        else:
            y = random.randint(0, winHeight)

        return x, y

    def next_level(self):
        if not self.SpriteGroups.enemy_sprites:
            self.level += 1
            self.player.health += 10

            if self.level == 30:
                for grunts in self.SpriteGroups.enemy_sprites:
                    grunts.kill()

                for gravity_bomb in self.SpriteGroups.gravity_ball_sprites:
                    gravity_bomb.kill()

                self.boss = enemy((winWidth/2, -100), 100, 480, 4000, self.SpriteGroups)
            
            else:
                amount = self.level % 10 + 3
                health = self.level // 10 + 1

                for _ in range(amount):
                    x, y = self.generate_spawn_cords()
                    enemy((x, y), health, random.randint(200, 400), 3500, self.SpriteGroups)

                if len(self.SpriteGroups.gravity_ball_sprites) < 5:

                    for _ in range(random.randint(1, 2)):
                        GravityBallCenter((random.randint(0, winWidth), random.randint(0, winHeight)), 300, 300, self.SpriteGroups)

                return

    def run(self, dt):
        self.draw_background()
        self.update_enemy_player_pos()
        self.SpriteGroups.all_sprites.update(dt)

        self.SpriteGroups.all_sprites.draw(self.display_surface)
        self.draw_elements()
        self.next_level()

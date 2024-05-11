from settings import *
from player import Player
from enemies import Enemy
from gravity_ball import GravityBallCenter
from spritegroups import SpriteGroups
from text_shape import HealthBar, Text
from timer import Timer
import random

class Level:
    def __init__(self, test_mode) -> None:
        """
        Initialize the level and its elements.

        :param bool test_mode: Whether the game is in test mode or not.
        :rtype: None
        """

        # setting up the display and level
        self.display_surface = pygame.display.get_surface()
        self._load_backgrounds()
        self.spawn_timer = Timer(2000)
        self.initialize_spawn = False
        self.test_mode = test_mode
        self.level = 28
        self.setup()

    def _load_backgrounds(self) -> None:
        """
        Load the background images.

        :rtype: None
        """
        self.img_background = pygame.image.load(join("data", "background.png")).convert_alpha()
        self.img_background_behind = pygame.image.load(join("data", "background2.png")).convert_alpha()

    def setup(self) -> None:
        """
        Initialize the level and its elements.
        
        :rtype: None
        """
        self.sprite_groups = SpriteGroups()
        self.player = Player((WIDTH / 2, HEIGHT / 2), self.test_mode, self.sprite_groups)

        # setting up the player health bar
        self.health_bar = HealthBar(
            surf=self.display_surface,
            x=20,
            y=HEIGHT - 50,
            health=self.player.health,
            h=10,
            maxhealth=100,
            barwidth=500,
            colour=clrRed
        )

        # boss elements
        self.boss = None
        self.boss_bar = None

        # setting up the player dash text
        self.dash_text = Text(
            surf=self.display_surface,
            x=20,
            y=HEIGHT - 100,
            size=30,
            text=f"{round(self.player.timer['dash'].time_left / 1000, 1)}",
            colour=clrWhite,
            allign="topleft"
        )

        # setting up the player bomb text
        self.bomb_text = Text(
            surf=self.display_surface,
            x=20,
            y=HEIGHT - 150,
            size=30,
            text=f"{round(self.player.timer['bomb'].time_left / 1000, 1)}",
            colour=clrWhite,
            allign="topleft"
        )

        # setting up the level text
        self.level_text = Text(
            surf=self.display_surface,
            x=None,
            y=25,
            size=60,
            text=f"Level: {self.level}",
            colour=clrWhite
        )

        # list of elements to draw
        self.element_list = [self.health_bar, self.dash_text, self.bomb_text, self.level_text]

    def draw_elements(self) -> None:
        """
        Draw all UI elements on the display surface.
        
        :rtype: None
        """

        # update the health bar and level text
        self.health_bar.update_hp(self.player.health)
        self.level_text.change_text(f"Level: {self.level}")

        # update the dash and bomb text if the timers are active (cooldowns)
        if self.player.timer["dash"].active:
            self.dash_text.change_text(f"Dash: {round(self.player.timer['dash'].time_left / 1000, 1)}")
        else:
            self.dash_text.change_text(f"Dash Ready")

        if self.player.timer["bomb"].active:
            self.bomb_text.change_text(f"Bomb: {round(self.player.timer['bomb'].time_left / 1000, 1)}")
        else:
            self.bomb_text.change_text(f"Bomb Ready")

        # draw the boss health bar if the level is 30
        if self.level == 30:

            # if there is no boss, create one
            if self.boss_bar is None:
                self.boss_bar = HealthBar(
                    surf=self.display_surface,
                    x=WIDTH // 2 - 250,
                    y=20,
                    h=20,
                    health=self.boss.health,
                    maxhealth=self.boss.health,
                    barwidth=500,
                    colour=clrRed
                )

                # remove the level text and add the boss bar
                self.element_list.append(self.boss_bar)
                self.element_list.remove(self.level_text)
            else:
                self.boss_bar.update_hp(self.boss.health)

        # draw all elements
        for element in self.element_list:
            element.draw()

    def update_enemy_player_pos(self) -> None:
        """
        Update the position of the player relative to the enemies.
        
        :rtype: None
        """
        for enemy in self.sprite_groups.enemy_sprites:
            enemy.update_player_pos(self.player.rect.center)

    def draw_background(self) -> None:
        """
        Draw the background on the display surface.
        
        :rtype: None
        """
        self.display_surface.fill(clrBlack)
        self.display_surface.blit(self.img_background, (0, 0))

    @staticmethod
    def generate_spawn_coords():
        """
        Generate random off-screen coordinates for spawning enemies.
        
        :return: tuple of x and y coordinates.
        :rtype: tuple[int, int]
        """

        # possible x and y coordinates
        x = random.choice([
            random.randint(-100, -20),
            random.randint(WIDTH + 20, WIDTH + 100)
        ])
        y = random.choice([
            random.randint(-100, -20),
            random.randint(HEIGHT + 20, HEIGHT + 100)
        ])

        # choose either choice
        if random.choice([True, False]):
            x = random.randint(0, WIDTH)
        else:
            y = random.randint(0, HEIGHT)

        return x, y

    def next_level(self) -> None:
        """
        Proceed to the next level and spawn enemies accordingly.
        
        :rtype: None
        """

        # if there are no enemies, spawn new ones
        if not self.sprite_groups.enemy_sprites:

            # giving some time after a wave is cleared
            if not self.initialize_spawn:
                self.spawn_timer.activate()
                self.initialize_spawn = True
                return

            # update timer
            if self.spawn_timer.active:
                self.spawn_timer.update()
                return

            # increase level and spawn enemies, add 10 hp to player
            self.level += 1
            self.player.health = min(self.player.health + 10, self.player.max_health)

            # if level 30, spawn boss, delete all other enemies and gravity balls
            if self.level == 30:

                for enemy in self.sprite_groups.enemy_sprites:
                    enemy.kill()
                
                for gravity_ball in self.sprite_groups.gravity_ball_sprites:
                    gravity_ball.kill()

                self.boss = Enemy((WIDTH / 2, -100), 100, 470, 4000, self.sprite_groups)
            else:

                # Logic, amount of enemies increases by 1 every level, starting at 3
                # Health of enemies increases by 1 every 10 levels, amount resets to 3

                amount = self.level % 10 + 3
                health = self.level // 10 + 1

                # spawn enemies and gravity balls
                for _ in range(amount):
                    x, y = self.generate_spawn_coords()
                    Enemy((x, y), health, random.randint(200, 400), random.randint(3000, 5000), self.sprite_groups)

                # spawn gravity balls if there are less than 4
                if len(self.sprite_groups.gravity_ball_sprites) < 4:
                    GravityBallCenter((random.randint(0, WIDTH), random.randint(0, HEIGHT)), 300, 300, self.sprite_groups)

            self.initialize_spawn = False

    def run(self, dt: float) -> int:
        """
        Run the game loop and update the level state.

        :peram float dt: Delta time.

        :return: 0 if level continues, 1 if level 31 is reached, -1 if player dies.
        :rtype: int
        """

        # if player is alive, run the level
        if self.player.health > 0:
            self.draw_background()
            self.update_enemy_player_pos()
            self.sprite_groups.all_sprites.update(dt)
            self.sprite_groups.all_sprites.draw(self.display_surface)
            self.draw_elements()
            self.next_level()

            # if level 31 is reached, return 1, meaning the game is won
            if self.level == 31:
                return 1

            # return 0, meaning the level continues
            return 0

        # if player is dead, return -1, meaning the game is lost
        return -1

import pygame as pg
import sys
from settings import *
from map import *
from player import *
from raycasting import *
from object_renderer import *
from sprite_object import *
from object_handler import *
from weapon import *
from sound import *
from pathfinding import *


class Menu:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.clock = game.clock
        self.font = pg.font.SysFont('Arial', 40)
        self.options = ['Play', 'Quit']
        self.selected_option = 0

    def draw(self):
        self.screen.fill('black')
        for i, option in enumerate(self.options):
            color = 'red' if i == self.selected_option else 'white'
            text_surface = self.font.render(option, True, color)
            text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 + i * 60))
            self.screen.blit(text_surface, text_rect)
        pg.display.flip()

    def handle_input(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_UP:
                    self.selected_option = (self.selected_option - 1) % len(self.options)
                elif event.key == pg.K_DOWN:
                    self.selected_option = (self.selected_option + 1) % len(self.options)
                elif event.key == pg.K_RETURN:
                    if self.selected_option == 0:  # Play
                        return True
                    elif self.selected_option == 1:  # Quit
                        pg.quit()
                        sys.exit()

        return False

    def run(self):
        while True:
            if self.handle_input():
                break
            self.draw()
            self.clock.tick(60)

class Game:
    def __init__(self):
        pg.init()
        pg.mouse.set_visible(False)
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.event.set_grab(True)
        self.clock = pg.time.Clock()
        self.delta_time = 1
        self.global_trigger = False
        self.global_event = pg.USEREVENT + 0
        pg.time.set_timer(self.global_event, 40)
        self.menu = Menu(self)  # Initialize the menu
        self.new_game()

    def new_game(self):
        self.map = Map(self)
        self.player = Player(self)
        self.object_renderer = ObjectRenderer(self)
        self.raycasting = RayCasting(self)
        self.object_handler = ObjectHandler(self)
        self.weapon = Weapon(self)
        self.sound = Sound(self)
        self.pathfinding = PathFinding(self)
        pg.mixer.music.play(-1)

    def update(self):
        self.player.update()
        self.raycasting.update()
        self.object_handler.update()
        self.weapon.update()
        pg.display.flip()
        self.delta_time = self.clock.tick(FPS)
        pg.display.set_caption(f'{self.clock.get_fps() :.1f}')

    def draw(self):
        self.object_renderer.draw()
        self.weapon.draw()

    def check_events(self):
        self.global_trigger = False
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit()
            elif event.type == self.global_event:
                self.global_trigger = True
            self.player.single_fire_event(event)

    def run(self):
        # Show the main menu first
        self.menu.run()

        # After the menu loop, start the game loop
        while True:
            self.check_events()
            self.update()
            self.draw()

if __name__ == '__main__':
    game = Game()
    game.run()
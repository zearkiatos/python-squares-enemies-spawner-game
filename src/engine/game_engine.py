import pygame
import esper
from src.ecs.create.prefabric_creator import create_square
from src.ecs.systems.s_movement import system_movement
from src.ecs.systems.s_rendering import system_rendering
from src.ecs.systems.s_screen_bounce import system_screen_bounce
from src.utils.file_handler import read_json_file


class GameEngine:
    def __init__(self) -> None:
        pygame.init()
        self.window_config = read_json_file("assets/cfg/window.json")
        sizes = tuple(self.window_config["window"]["size"].values())
        pygame.display.set_caption(self.window_config["window"]["title"])
        self.screen = pygame.display.set_mode(sizes, pygame.SCALED)
        self.clock = pygame.time.Clock()
        self.is_running = False
        self.framerate = self.window_config["window"]["framerate"]
        self.delta_time = 0

        self.ecs_world = esper.World()

    def run(self) -> None:
        self._create()
        self.is_running = True
        while self.is_running:
            self._calculate_time()
            self._process_events()
            self._update()
            self._draw()
        self._clean()

    def _create(self):
        create_square(self.ecs_world, pygame.Vector2(50, 50), pygame.Vector2(
            150, 100), pygame.Vector2(150, 300), pygame.Color(255, 100, 100))

    def _calculate_time(self):
        self.clock.tick(self.framerate)
        self.delta_time = self.clock.get_time() / 1000.0

    def _process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False

    def _update(self):
        system_movement(self.ecs_world, self.delta_time)
        system_screen_bounce(self.ecs_world, self.screen)

    def _draw(self):
        color = tuple(self.window_config["window"]["bg_color"].values())
        self.screen.fill(color)

        system_rendering(self.ecs_world, self.screen)
        pygame.display.flip()

    def _clean(self):
        pygame.quit()

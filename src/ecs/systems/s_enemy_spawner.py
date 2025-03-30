import esper
import pygame
from src.ecs.create.prefabric_creator import create_enemies
from src.ecs.components.c_enemy_spawner import CEnemySpawner
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.utils.file_handler import read_json_file

def system_enemy_spawner(world: esper.World):
    enemies_json = read_json_file("assets/cfg/enemies.json")
    enemies_quantity_level_json = read_json_file("assets/cfg/level_01.json")
    enemies_list = []
    for enemy_level in enemies_quantity_level_json:
        for enemy in enemies_json:
            if enemy.get("name") == enemy_level.get("enemy_type"):
                enemy_component = CEnemySpawner(
                name=enemy["name"],
                velocity=CVelocity(
                    pygame.Vector2(enemy["speed"]["minimum"], enemy["speed"]["maximum"])
                ),
                transform=CTransform(
                    pygame.Vector2(enemy_level["position"]["x"], enemy_level["position"]["y"])
                ),
                surface=CSurface(
                    pygame.Vector2(enemy["size"]["width"], enemy["size"]["height"]),
                    pygame.Color(enemy["color"]["red"], enemy["color"]["green"], enemy["color"]["blue"]),
                ),
                color=pygame.Color(enemy["color"]["red"], enemy["color"]["green"], enemy["color"]["blue"]),
            )
                enemies_list.append(enemy_component)
                break
    create_enemies(world, enemies_list)
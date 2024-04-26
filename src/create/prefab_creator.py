import esper
import pygame
import random

from src.ecs.components.c_animation import CAnimation
from src.ecs.components.c_enemy_spawner import CEnemySpawner
from src.ecs.components.c_explosion_state import CExplosionState
from src.ecs.components.c_hunter_state import CHunterState
from src.ecs.components.c_input_command import CInputCommand
from src.ecs.components.c_player_state import CPlayerState
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.tags.c_tag_bullet import CTagBullet
from src.ecs.components.tags.c_tag_enemy import CTagEnemy, EnemyType
from src.ecs.components.tags.c_tag_explosion import CTagExplosion
from src.ecs.components.tags.c_tag_player import CTagPlayer
from src.engine.service_locator import ServiceLocator

def create_square(ecs_world:esper.World, size:pygame.Vector2,
                   pos:pygame.Vector2, vel:pygame.Vector2, col:pygame.Color) -> int:
    cuad_entity = ecs_world.create_entity()
    ecs_world.add_component(cuad_entity,
                                    CSurface(size, col))
    ecs_world.add_component(cuad_entity,
                                    CTransform(pos))
    ecs_world.add_component(cuad_entity,
                                    CVelocity(vel))
    return cuad_entity

def create_sprite(ecs_world:esper.World, pos:pygame.Vector2, vel:pygame.Vector2, 
                  surface:pygame.Vector2) -> int:
    sprite_entity = ecs_world.create_entity()
    ecs_world.add_component(sprite_entity, 
                            CTransform(pos))
    ecs_world.add_component(sprite_entity, 
                            CVelocity(vel))
    ecs_world.add_component(sprite_entity,
                            CSurface.from_surface(surface))
    return sprite_entity
    
def create_enemy(ecs_world:esper.World, pos:pygame.Vector2, enemy_info:dict, type:int):
    if type == EnemyType.ASTEROID:
        _create_asteroid(ecs_world, pos, enemy_info, type)
    elif type == EnemyType.HUNTER:
        _create_hunter(ecs_world, pos, enemy_info, type)


def _create_asteroid(ecs_world:esper.World, pos:pygame.Vector2, asteroid_info:dict, type:int):
    asteroid_surface = ServiceLocator.images_service.get(asteroid_info["image"])
    asteroid_size = asteroid_surface.get_rect().size
    pos = pygame.Vector2(pos.x - (asteroid_size[0] / 2), 
                         pos.y - (asteroid_size[1] / 2))
    vel_range = random.randrange(asteroid_info['velocity_min'],
                                 asteroid_info['velocity_max'])
    vel = pygame.Vector2(random.choice([-vel_range, vel_range]),
                        random.choice([-vel_range, vel_range]))
    enemy_entity = create_sprite(ecs_world, pos, vel, asteroid_surface)
    ecs_world.add_component(enemy_entity, CTagEnemy(type, pos.copy()))
    ServiceLocator.sounds_service.play(asteroid_info["sound"])

def _create_hunter(ecs_world:esper.World, pos:pygame.Vector2, hunter_info:dict, type:int):
    hunter_surface = ServiceLocator.images_service.get(hunter_info["image"])
    vel = pygame.Vector2(0,0)
    enemy_entity = create_sprite(ecs_world, pos, vel, hunter_surface)
    ecs_world.add_component(enemy_entity, CTagEnemy(type, pos.copy()))
    ecs_world.add_component(enemy_entity, CAnimation(hunter_info["animations"]))
    ecs_world.add_component(enemy_entity, CHunterState())

def create_enemy_spawner(ecs_world:esper.World, level_data:dict):
    spawner_entity = ecs_world.create_entity()
    ecs_world.add_component(spawner_entity, 
                            CEnemySpawner(level_data["enemy_spawn_events"]))
    
def create_player(ecs_world:esper.World, player_info:dict, player_lvl_info:dict) -> int:
    player_surface = ServiceLocator.images_service.get(player_info["image"])
    size = player_surface.get_size()
    size = (size[0] / player_info["animations"]["number_frames"], size[1])
    pos = pygame.Vector2(player_lvl_info["position"]["x"] - (size[0]/2),
                         player_lvl_info["position"]["y"] - (size[1]/2))
    vel = pygame.Vector2(0,0)
    player_entity = create_sprite(ecs_world, pos, vel, player_surface)
    ecs_world.add_component(player_entity, CTagPlayer()) # no olvidar ()
    ecs_world.add_component(player_entity, CAnimation(player_info["animations"]))
    ecs_world.add_component(player_entity, CPlayerState())
    return player_entity

def create_bullet(ecs_world:esper.World, click_pos:tuple, player_pos:pygame.Vector2, 
                         player_size:pygame.Vector2, bullet_info:dict):
    bullet_surface = ServiceLocator.images_service.get(bullet_info["image"])
    bullet_size = bullet_surface.get_rect().size
    pos = pygame.Vector2(player_pos.x + (player_size[0] / 2) - (bullet_size[0] / 2), 
                         player_pos.y + (player_size[1] / 2) - (bullet_size[1] / 2))
    player_pos_center = pygame.Vector2(player_pos.x + (player_size[0]/2), 
                                   player_pos.y + (player_size[1]/2))
    vel = (click_pos - player_pos_center)

    vel = vel.normalize() * bullet_info["velocity"]
    
    bullet_entity = create_sprite(ecs_world, pos, vel, bullet_surface)
    ecs_world.add_component(bullet_entity, CTagBullet()) # no olvidar ()
    ServiceLocator.sounds_service.play(bullet_info["sound"])

def create_input_player(ecs_world:esper.World):
    input_left = ecs_world.create_entity()
    input_right = ecs_world.create_entity()
    input_up = ecs_world.create_entity()
    input_down = ecs_world.create_entity()
    input_pause = ecs_world.create_entity()
    input_left_click = ecs_world.create_entity()

    ecs_world.add_component(input_left, CInputCommand("PLAYER_LEFT", [pygame.K_LEFT, pygame.K_a]))
    ecs_world.add_component(input_right, CInputCommand("PLAYER_RIGHT", [pygame.K_RIGHT, pygame.K_d]))
    ecs_world.add_component(input_up, CInputCommand("PLAYER_UP", [pygame.K_UP, pygame.K_w]))
    ecs_world.add_component(input_down, CInputCommand("PLAYER_DOWN", [pygame.K_DOWN, pygame.K_s]))
    ecs_world.add_component(input_down, CInputCommand("PLAYER_DOWN", [pygame.K_DOWN, pygame.K_s]))
    ecs_world.add_component(input_pause, CInputCommand("PLAYER_PAUSE", [pygame.K_p]))
    ecs_world.add_component(input_left_click, CInputCommand("PLAYER_FIRE", [pygame.BUTTON_LEFT]))

def create_explosion(ecs_world:esper.World, enemy_pos:pygame.Vector2, enemy_size:pygame.Vector2, explosion_info:dict):
    explosion_surface = ServiceLocator.images_service.get(explosion_info["image"])
    size = explosion_surface.get_size()
    size = (size[0] / explosion_info["animations"]["number_frames"], size[1])
    pos = pygame.Vector2(enemy_pos.x + (enemy_size[0] / 2) - (size[0] / 2), 
                         enemy_pos.y + (enemy_size[1] / 2) - (size[1] / 2))
    vel = pygame.Vector2(0,0)
    explosion_entity = create_sprite(ecs_world, pos, vel, explosion_surface)
    ecs_world.add_component(explosion_entity, CTagExplosion()) # no olvidar ()
    ecs_world.add_component(explosion_entity, CAnimation(explosion_info["animations"]))
    ecs_world.add_component(explosion_entity, CExplosionState())
    ServiceLocator.sounds_service.play(explosion_info["sound"])

def create_text(ecs_world:esper.World, text_cfg:dict):
    color = pygame.Color(text_cfg["color"]["r"],
                         text_cfg["color"]["g"],
                         text_cfg["color"]["b"])
    font = ServiceLocator.fonts_service.get(text_cfg["font"], text_cfg["size"]) 
    text_entity = ecs_world.create_entity()
    text_surface = CSurface.from_text(text_cfg["text"], font, color)
    size = text_surface.area.size
    pos = pygame.Vector2(text_cfg["position"]["x"], text_cfg["position"]["y"])
    if text_cfg["middle"]:
        final_pos = pygame.Vector2(pos.x - size[0]/2, pos.y - size[1]/2)
    else:
        final_pos = pos
    ecs_world.add_component(text_entity,
                            CTransform(final_pos))
    ecs_world.add_component(text_entity, text_surface)
    return text_entity
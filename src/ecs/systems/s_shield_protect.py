import esper
import pygame

from src.create.prefab_creator import create_explosion
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_enemy import CTagEnemy
from src.ecs.components.tags.c_tag_shield import CTagShield

def system_shield_protect(ecs_world:esper.World, shield_cfg:dict, explosion_cfg:dict, delta_time:float):
    shield_components = ecs_world.get_components(CTransform, CTagShield)
    enemy_components = ecs_world.get_components(CSurface, CTransform, CTagEnemy)

    shield_distance = shield_cfg["distance"]

    for _, (s_c_t, c_ts) in shield_components:
        c_ts.timer += delta_time
        for enemy_entity, (c_s, e_c_t, _) in enemy_components:
            distance_to_enemy = s_c_t.pos.distance_to(e_c_t.pos)
            ene_rect = CSurface.get_area_relative(c_s.area, e_c_t.pos)
            if distance_to_enemy < shield_distance:
                ecs_world.delete_entity(enemy_entity)
                create_explosion(ecs_world, ene_rect, c_s.area.size, explosion_cfg)

import esper

from src.create.prefab_creator import create_explosion
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_bullet import CTagBullet
from src.ecs.components.tags.c_tag_enemy import CTagEnemy

def system_collision_bullet_enemy(ecs_world:esper.World, explosion_cfg:dict):
    enemy_components = ecs_world.get_components(CSurface, CTransform, CTagEnemy)
    bullet_components = ecs_world.get_components(CSurface, CTransform, CTagBullet)

    for enemy_entity, (c_s, c_t, _) in enemy_components:
        ene_rect = CSurface.get_area_relative(c_s.area, c_t.pos)
        for bullet_entity, (c_b_s, c_b_t, _) in bullet_components:
            bl_rect = c_b_s.area.copy()
            bl_rect.topleft = c_b_t.pos
            if ene_rect.colliderect(bl_rect):
                ecs_world.delete_entity(enemy_entity)
                ecs_world.delete_entity(bullet_entity)
                create_explosion(ecs_world, ene_rect, c_s.area.size, explosion_cfg)
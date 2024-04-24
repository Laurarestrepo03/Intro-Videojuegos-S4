import esper
from src.create.prefab_creator import create_explosion
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_enemy import CTagEnemy

def system_collision_player_enemy(ecs_world:esper.World, player_entity:int, level_cfg:dict, explosion_cfg:dict):
    components = ecs_world.get_components(CSurface, CTransform, CTagEnemy)
    pl_t = ecs_world.component_for_entity(player_entity, CTransform)
    pl_s = ecs_world.component_for_entity(player_entity, CSurface)
    
    pl_rect = CSurface.get_area_relative(pl_s.area, pl_t.pos)

    for enemy_entity, (c_s, c_t, _) in components:
        ene_rect = CSurface.get_area_relative(c_s.area, c_t.pos)
        if ene_rect.colliderect(pl_rect):
            ecs_world.delete_entity(enemy_entity)
            create_explosion(ecs_world, ene_rect, c_s.area.size, explosion_cfg)
            size = pl_s.area.size
            pl_t.pos.x = level_cfg["player_spawn"]["position"]["x"] - (size[0]/2)
            pl_t.pos.y = level_cfg["player_spawn"]["position"]["y"] - (size[1]/2)
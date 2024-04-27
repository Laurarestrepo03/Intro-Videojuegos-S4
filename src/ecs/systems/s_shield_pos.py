import esper
import pygame
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_player import CTagPlayer
from src.ecs.components.tags.c_tag_shield import CTagShield

def system_shield_pos(ecs_world:esper.World, shield_cfg:dict):
    shield_components = ecs_world.get_components(CTransform, CSurface, CTagShield)

    if len(shield_components) > 0:
        player_components = ecs_world.get_components(CTransform, CSurface, CTagPlayer)
        for _, (c_t, c_s, _) in shield_components:
            for _, (p_c_t, p_c_s, _) in player_components:
                size = c_s.surf.get_size()
                shield_size = (size[0] / shield_cfg["animations"]["number_frames"], size[1])
                player_pos = p_c_t.pos
                player_size = p_c_s.area.size
                c_t.pos = pygame.Vector2(player_pos.x + (player_size[0] / 2) - (shield_size[0] / 2), 
                            player_pos.y + (player_size[1] / 2) - (shield_size[1] / 2))
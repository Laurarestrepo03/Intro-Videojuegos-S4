import esper
import pygame

from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.tags.c_tag_player import CTagPlayer

def system_player_limit(ecs_world:esper.World, screen:pygame.Surface):
    
    screen_rect = screen.get_rect()
    components = ecs_world.get_components(CTransform, CVelocity, CSurface, CTagPlayer)

    for _, (c_t, c_v, c_s, c_p) in components:
        player_rect = CSurface.get_area_relative(c_s.area, c_t.pos)
        if player_rect.left < 0:
            c_t.pos.x = 0 
        elif player_rect.right > screen_rect.width:
            c_t.pos.x = screen_rect.width - player_rect.width 

        if player_rect.top < 0:
            c_t.pos.y = 0
        elif player_rect.bottom > screen_rect.height:
            c_t.pos.y = screen_rect.height - player_rect.height 

    

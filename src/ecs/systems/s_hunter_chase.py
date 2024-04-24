import math
import pygame
import esper

from src.ecs.components.c_hunter_state import CHunterState, HunterState
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.tags.c_tag_enemy import CTagEnemy, EnemyType
from src.ecs.components.tags.c_tag_player import CTagPlayer

import math
import pygame.math
import esper
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.tags.c_tag_enemy import CTagEnemy, EnemyType
from src.ecs.components.tags.c_tag_player import CTagPlayer

def system_hunter_chase(ecs_world: esper.World, hunter_cfg: dict):
    hunter_components = ecs_world.get_components(CTransform, CVelocity, CTagEnemy, CHunterState)
    player_components = ecs_world.get_components(CTransform, CTagPlayer)

    for _, (c_t_h, c_v_h, c_t_e, c_h_st) in hunter_components:
        for _, (c_t_p, _) in player_components:
            if c_t_e.type == EnemyType.HUNTER:
                if c_h_st.state == HunterState.CHASE:
                    displacement_to_player = c_t_p.pos - c_t_h.pos
                    direction_to_player = displacement_to_player.normalize()
                    chase_velocity = hunter_cfg["velocity_chase"]
                    c_v_h.vel = direction_to_player * chase_velocity

                elif c_h_st.state == HunterState.RETURN:
                    displacement_to_origin = c_t_e.origin - c_t_h.pos
                    direction_to_origin = displacement_to_origin.normalize()
                    velocity_return = hunter_cfg["velocity_return"]
                    c_v_h.vel = direction_to_origin * velocity_return
                    
                elif c_h_st.state == HunterState.IDLE:
                     c_v_h.vel = pygame.Vector2(0,0)
                    
                


                


        
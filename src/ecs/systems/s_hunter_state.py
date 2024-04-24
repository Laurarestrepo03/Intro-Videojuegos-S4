import esper
from src.ecs.components.c_animation import CAnimation
from src.ecs.components.c_hunter_state import CHunterState, HunterState
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_enemy import CTagEnemy
from src.ecs.components.tags.c_tag_player import CTagPlayer
from src.engine.service_locator import ServiceLocator

def system_hunter_state(ecs_world:esper.World, hunter_cfg:dict):
    hunter_components = ecs_world.get_components(CTransform, CAnimation, CHunterState, CTagEnemy)
    player_components = ecs_world.get_components(CTransform, CTagPlayer)
    
    for _, (c_t, c_a, c_hst, c_te) in hunter_components:
        for _, (c_t_p, _) in player_components:
            if c_hst.state == HunterState.IDLE:
                _do_idle_state(c_t, c_a, c_hst, c_t_p, hunter_cfg)
            elif c_hst.state == HunterState.CHASE:
                _do_chase_state(c_t, c_a, c_hst, c_te, hunter_cfg)
            elif c_hst.state == HunterState.RETURN:
                _do_return_state(c_t, c_a, c_hst, c_te)
    
def _do_idle_state(c_t:CTransform, c_a:CAnimation, c_hst:CHunterState, 
                   c_t_p:CTransform, hunter_cfg:dict):
    _set_animation(c_a, 1)
    distance_to_player = c_t.pos.distance_to(c_t_p.pos)
    if distance_to_player <= hunter_cfg["distance_start_chase"]:
        ServiceLocator.sounds_service.play(hunter_cfg["sound_chase"])
        c_hst.state = HunterState.CHASE

def _do_chase_state(c_t:CTransform, c_a:CAnimation, c_hst:CHunterState, 
                   c_te:CTagEnemy, hunter_cfg:dict):
     _set_animation(c_a, 0)
     distance_to_origin = c_t.pos.distance_to(c_te.origin)
     if distance_to_origin >= hunter_cfg["distance_start_return"]:
        c_hst.state = HunterState.RETURN

def _do_return_state(c_t:CTransform, c_a:CAnimation, c_hst:CHunterState, 
                   c_te:CTagEnemy):
     _set_animation(c_a, 0)
     distance_to_origin = c_t.pos.distance_to(c_te.origin)
     if distance_to_origin < 1:
        c_hst.state = HunterState.IDLE
        
def _set_animation(c_a:CAnimation, num_anim:int):
    if c_a.curr_anim == num_anim:
        return
    c_a.curr_anim = num_anim
    c_a.curr_anim_time = 0
    c_a.curr_frame = c_a.curr_frame = c_a.animations_list[c_a.curr_anim].start
import esper
from src.ecs.components.c_animation import CAnimation
from src.ecs.components.c_explosion_state import CExplosionState, ExplosionState

def system_explosion_state(ecs_world:esper.World):
    components = ecs_world.get_components(CAnimation, CExplosionState)

    for entity, (c_a, c_est) in components:
        if c_est.state == ExplosionState.EXPLODE:
            _do_explode_state(ecs_world, entity,c_a)
            
def _do_explode_state(ecs_world: esper.World, entity:int, c_a:CAnimation):
     if c_a.curr_frame == c_a.animations_list[c_a.curr_anim].end:
        ecs_world.delete_entity(entity)
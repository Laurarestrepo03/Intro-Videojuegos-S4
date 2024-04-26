import esper
from src.ecs.components.c_shield_state import CShieldState, ShieldState
from src.ecs.components.tags.c_tag_shield import CTagShield

def system_shield_state(ecs_world:esper.World):
    components = ecs_world.get_components(CShieldState, CTagShield)

    for entity, (c_sst, c_ts) in components:
        if c_sst.state == ShieldState.PROTECT:
            _do_protect_state(ecs_world, entity, c_ts)
            
def _do_protect_state(ecs_world: esper.World, entity:int, c_ts:CTagShield):
     #TODO: destroy after 2s
     if c_ts.timer >= 2:
        ecs_world.delete_entity(entity)
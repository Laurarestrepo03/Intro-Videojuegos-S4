import esper
from src.ecs.components.c_shield_state import CShieldState, ShieldState
from src.ecs.components.tags.c_tag_shield import CTagShield

def system_shield_state(ecs_world:esper.World, shield_cfg:dict):
    components = ecs_world.get_components(CShieldState, CTagShield)

    for entity, (c_ss, c_ts) in components:
        if c_ss.state == ShieldState.PROTECT:
            _do_protect_state(ecs_world, entity, c_ts, shield_cfg)
            
def _do_protect_state(ecs_world: esper.World, entity:int, c_ts:CTagShield, shield_cfg:dict):
     if c_ts.timer >= shield_cfg["duration"]:
        ecs_world.delete_entity(entity)
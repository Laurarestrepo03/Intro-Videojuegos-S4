import esper
import pygame

from src.ecs.components.tags.c_tag_shield import CTagShield

def system_shield_protect(ecs_world:esper.World, delta_time:float):
    components = ecs_world.get_component(CTagShield)

    for _, (c_ts) in components:
        c_ts.timer += delta_time


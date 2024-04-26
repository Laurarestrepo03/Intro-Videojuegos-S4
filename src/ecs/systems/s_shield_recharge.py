import esper
import pygame

from src.ecs.components.c_surface import CSurface
from src.ecs.components.tags.c_tag_recharge import CTagRecharge
from src.engine.service_locator import ServiceLocator

def system_shield_recharge(ecs_world:esper.World, shield_cfg:dict, recharge_cfg:dict, delta_time:float):
    components = ecs_world.get_components(CSurface, CTagRecharge)
    font = ServiceLocator.fonts_service.get(recharge_cfg["font"], recharge_cfg["size"])

    for _, (c_s, c_tr) in components:
        if c_tr.value == 100:
            color = pygame.Color(0,255,0)
        else: 
            color = pygame.Color(255,0,0)

        if c_tr.value >= 0 and c_tr.value < 100:
            c_tr.timer += delta_time
            c_tr.value = round((c_tr.timer / shield_cfg["recharge"]) * 100)
            if c_tr.timer >= shield_cfg["recharge"]:
                c_tr.timer = 0
                c_tr.value = 100

        text = str(c_tr.value) + "%"
        c_s.surf = font.render(text, False, color)
        c_s.area = c_s.surf.get_rect()


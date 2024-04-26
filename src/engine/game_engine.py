import asyncio
import esper
import json
import pygame

from src.create.prefab_creator import create_bullet, create_enemy_spawner, create_input_player, create_player, create_text
from src.ecs.components.c_input_command import CInputCommand, CommandPhase
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.tags.c_tag_bullet import CTagBullet
from src.ecs.components.tags.c_tag_player import CTagPlayer
from src.ecs.systems.s_animation import system_animation
from src.ecs.systems.s_bullet_limit import system_bullet_limit
from src.ecs.systems.s_collision_bullet_enemy import system_collision_bullet_enemy
from src.ecs.systems.s_collision_player_enemy import system_collision_player_enemy
from src.ecs.systems.s_enemy_spawner import system_enemy_spawner
from src.ecs.systems.s_explosion_state import system_explosion_state
from src.ecs.systems.s_hunter_chase import system_hunter_chase
from src.ecs.systems.s_hunter_state import system_hunter_state
from src.ecs.systems.s_input_player import system_input_player
from src.ecs.systems.s_movement import system_movement
from src.ecs.systems.s_player_limit import system_player_limit
from src.ecs.systems.s_player_state import system_player_state
from src.ecs.systems.s_rendering import system_rendering
from src.ecs.systems.s_screen_bounce import system_screen_bounce
from src.engine.service_locator import ServiceLocator

class GameEngine:
    def __init__(self) -> None:
        self.load_config_files()

        pygame.init()    
        self.screen_w = self.window_cfg['size']['w']
        self.screen_h = self.window_cfg['size']['h']
        self.screen = pygame.display.set_mode((self.screen_w, self.screen_h), 0)
        screen_title = self.window_cfg['title']
        pygame.display.set_caption(screen_title)

        self.clock = pygame.time.Clock()
        self.is_running = False
        self.framerate = self.window_cfg['framerate']
        self.delta_time = 0
        self.current_time = 0

        self.game_state = "PLAYING"
        self.pause_entity = -1

        self.ecs_world = esper.World()

    def load_config_files(self):
        path = 'assets/cfg/'
        with open(path + 'interface.json', encoding="utf-8") as interface_file:
            self.interface_cfg = json.load(interface_file)
        with open(path + 'window.json', encoding="utf-8") as window_file:
            self.window_cfg = json.load(window_file)
        with open(path + 'enemies.json') as enemy_file:
            self.enemy_cfg = json.load(enemy_file)
        with open(path + 'level_01.json') as level_01_file:
            self.level_01_cfg = json.load(level_01_file)
        with open(path + 'player.json') as player_file:
            self.player_cfg = json.load(player_file)
        with open(path + 'bullet.json') as bullet_file:
            self.bullet_cfg = json.load(bullet_file)
        with open(path + 'explosion.json') as explosion_file:
            self.explosion_cfg = json.load(explosion_file)

    async def run(self) -> None:
        self._create()
        self.is_running = True
        while self.is_running:
            self._calculate_time()
            self._process_events()
            self._update()
            self._draw()
            await asyncio.sleep(0)
        self._clean()

    def _create(self):   
        self._player_entity = create_player(self.ecs_world, self.player_cfg, self.level_01_cfg["player_spawn"])
        self._player_c_v = self.ecs_world.component_for_entity(self._player_entity, CVelocity)
        self._player_c_t = self.ecs_world.component_for_entity(self._player_entity, CTransform)
        self._player_c_s = self.ecs_world.component_for_entity(self._player_entity, CSurface)
        self._player_tag = self.ecs_world.component_for_entity(self._player_entity, CTagPlayer)
        create_enemy_spawner(self.ecs_world, self.level_01_cfg)
        create_input_player(self.ecs_world)
        create_text(self.ecs_world, "Welcome", self.interface_cfg["name"]["font"], pygame.Vector2(100,100))

    def _calculate_time(self):
        self.clock.tick(self.framerate)
        self.delta_time = self.clock.get_time() / 1000.0
        if self.game_state == "PLAYING":
            self.current_time += self.delta_time

    def _process_events(self):
        for event in pygame.event.get():
            system_input_player(self.ecs_world, event, self._do_action)
            if event.type == pygame.QUIT:
                self.is_running = False

    def _update(self):
        if self.game_state == "PLAYING":
            system_enemy_spawner(self.ecs_world, self.current_time, self.enemy_cfg)
            system_movement(self.ecs_world, self.delta_time)

            system_player_state(self.ecs_world)
            system_explosion_state(self.ecs_world)
            system_hunter_state(self.ecs_world, self.enemy_cfg["Hunter"])

            system_screen_bounce(self.ecs_world, self.screen)
            system_player_limit(self.ecs_world, self.screen)
            system_bullet_limit(self.ecs_world, self.screen)

            system_hunter_chase(self.ecs_world, self.enemy_cfg["Hunter"])
        
            system_collision_player_enemy(self.ecs_world, self._player_entity, self.level_01_cfg, self.explosion_cfg)
            system_collision_bullet_enemy(self.ecs_world, self.explosion_cfg)

            system_animation(self.ecs_world, self.delta_time)
        
        self.ecs_world._clear_dead_entities()

    def _draw(self):
        screen_r = self.window_cfg['bg_color']['r']
        screen_g = self.window_cfg['bg_color']['g']
        screen_b = self.window_cfg['bg_color']['b']
        self.screen.fill((screen_r, screen_g, screen_b))

        system_rendering(self.ecs_world, self.screen)

        pygame.display.flip()

    def _clean(self):
        self.ecs_world.clear_database()
        pygame.quit()

    def _do_action(self, c_input:CInputCommand, click_pos:tuple=None):
        if c_input.name == "PLAYER_LEFT":
            if c_input.phase == CommandPhase.START:
               self._player_tag.keys_left += 1
               if self._player_tag.keys_left == 1:
                   self._player_c_v.vel.x -= self.player_cfg["input_velocity"]
            elif c_input.phase == CommandPhase.END:
                self._player_tag.keys_left -= 1
                if self._player_tag.keys_left == 0:
                    self._player_c_v.vel.x += self.player_cfg["input_velocity"]
                    
        if c_input.name == "PLAYER_RIGHT":
            if c_input.phase == CommandPhase.START:
                self._player_tag.keys_right += 1
                if self._player_tag.keys_right == 1:
                    self._player_c_v.vel.x += self.player_cfg["input_velocity"]
            elif c_input.phase == CommandPhase.END:
                self._player_tag.keys_right -= 1
                if self._player_tag.keys_right == 0:
                    self._player_c_v.vel.x -= self.player_cfg["input_velocity"]

        if c_input.name == "PLAYER_UP":
            if c_input.phase == CommandPhase.START:
                self._player_tag.keys_up += 1
                if self._player_tag.keys_up == 1:
                    self._player_c_v.vel.y -= self.player_cfg["input_velocity"]
            elif c_input.phase == CommandPhase.END:
                self._player_tag.keys_up -= 1
                if self._player_tag.keys_up == 0:
                    self._player_c_v.vel.y += self.player_cfg["input_velocity"]

        if c_input.name == "PLAYER_DOWN":
            if c_input.phase == CommandPhase.START:
                self._player_tag.keys_down += 1
                if self._player_tag.keys_down == 1:
                    self._player_c_v.vel.y += self.player_cfg["input_velocity"]
            elif c_input.phase == CommandPhase.END:
                self._player_tag.keys_down -= 1
                if self._player_tag.keys_down == 0:
                    self._player_c_v.vel.y -= self.player_cfg["input_velocity"]

        if self.game_state == "PLAYING": 
            if c_input.name == "PLAYER_FIRE":
                bullet_count = len(self.ecs_world.get_component(CTagBullet))
                if bullet_count < self.level_01_cfg["player_spawn"]["max_bullets"]:
                    create_bullet(self.ecs_world, click_pos, self._player_c_t.pos,
                                        self._player_c_s.area.size, self.bullet_cfg)

        if c_input.name == "PLAYER_PAUSE":
            if c_input.phase == CommandPhase.START:
                if self.game_state == "PLAYING":
                    self.game_state = "PAUSED"
                    self.pause_entity = create_text(self.ecs_world, self.interface_cfg["pause"]["text"], 
                                self.interface_cfg["pause"]["font"], 
                                pygame.Vector2((self.screen_w/2, self.screen_h/2)))
                else:
                    self.game_state = "PLAYING"
                    self.ecs_world.delete_entity(self.pause_entity)
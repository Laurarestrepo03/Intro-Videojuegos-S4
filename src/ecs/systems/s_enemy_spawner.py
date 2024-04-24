import esper

from src.create.prefab_creator import create_enemy
from src.ecs.components.c_enemy_spawner import CEnemySpawner
from src.ecs.components.tags.c_tag_enemy import EnemyType

def system_enemy_spawner(ecs_world:esper.World, current_time:float, enemies:dict):

    components = ecs_world.get_component(CEnemySpawner)

    for e, c_spawner in components:
        events = c_spawner.enemy_spawn_events
        spawned = c_spawner.spawned

        for enemy in events:
        
            time = events[enemy]['time']

            if enemy not in spawned and current_time >= time: 
                spawned.append(enemy)
                type = enemy.split("-")[0]
                pos = events[enemy]['pos']
                if "Hunter" in type:
                    create_enemy(ecs_world, pos, enemies[type], EnemyType.HUNTER)
                else:
                    create_enemy(ecs_world, pos, enemies[type], EnemyType.ASTEROID)
                
            
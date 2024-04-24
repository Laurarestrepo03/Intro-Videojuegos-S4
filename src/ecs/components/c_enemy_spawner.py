import pygame

class CEnemySpawner:
    def __init__(self, spawn_events_data:dict) -> None:
        self.enemy_spawn_events = {}
        i = 0

        for enemy in spawn_events_data:
            name = enemy['enemy_type']
            id = name + '-' + str(i)
            self.enemy_spawn_events[id] = {
                'time': enemy['time'],
                'pos': pygame.Vector2(enemy['position']['x'], 
                                  enemy['position']['y']),
            }
            i += 1
    
        self.spawned = []

            
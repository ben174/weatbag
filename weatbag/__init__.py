from collections import Counter
from importlib import import_module

from . import action

class Player:
    def __init__(self, name):
        self.name = name
        self.inventory = Counter()
        self.position = (0,0)
        self.hit_points = 6
    
    def has(self, item):
        "Does the player have any of item?"
        return self.inventory[item] > 0
    
    def give(self, item, n=1):
        "Put the item in the player's inventory."
        self.inventory.update([item]*n)
    
    def take(self, item, n=1):
        "Remove an item from the inventory. Raises KeyError if item isn't there."
        if self.inventory[item] >= n:
            self.inventory[item] -= n
        else:
            raise KeyError(item)

    def state_string(self): 
        "Returns a string reporting the players health."
        if self.hit_points >= 6: 
            return "feeling great"
        elif self.hit_points == 5: 
            return "feeling good"
        elif self.hit_points == 4: 
            return "feeling ok"
        elif self.hit_points == 3: 
            return "feeling poor"
        elif self.hit_points == 2: 
            return "feeling very unhealthy"
        elif self.hit_points == 1: 
            return "nearly dead"
        else: 
            return "dead"


class World:
    def __init__(self):
        self.tiles = {}
        from .tiles import centre
        self.tiles[(0,0)] = centre.Tile()
    
    def __getitem__(self, key):
        try:
            return self.tiles[key]
        except KeyError:
            e,n = key
            modname = 'weatbag.tiles.'
            if n > 0:
                modname += 'n'+str(n)
            elif n < 0:
                modname += 's'+str(abs(n))
            
            if e > 0:
                modname += 'e'+str(e)
            elif e < 0:
                modname += 'w'+str(abs(e))
            
            try:
                mod = import_module(modname)
            except ImportError:
                raise KeyError(key)
            
            tile = mod.Tile()
            self.tiles[key] = tile
            return tile

def main():
    name = input("What is your name? ")
    player = Player(name)
    world = World()
    tile = world[0,0]
    tile.describe()
    while True:
        do = action.get_action()
        if action.is_move(do):
            direction = do[1][0].lower()
            # check if we can leave tile
            if not getattr(tile, 'leave', lambda p,d: True)(player, direction):
                continue
            # move
            e,n = player.position
            de, dn = action.move_coords[direction]
            new_posn = e+de, n+dn
            try:
                tile = world[new_posn]
            except KeyError:
                print("The undergrowth in that direction is impassable. "
                      "You turn back.")
            else:
                player.position = new_posn
                tile.describe()
        else:
            action.handle_action(tile, player, do)


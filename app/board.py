"""Definition of Board"""
import random as r
from .tile import Tile, Hotel, Bridge

class Board:
    """Bored"""
    def __init__(self, size=64):
        """Initialize the board with tiles and random structures."""
        self.__tiles = [Tile(pos) for pos in range(1, size + 1)]
        for tile in r.sample(self.__tiles[1:-1], r.randint(1, int(size * 0.8))):
            struct = r.choice((Hotel, Bridge))
            self.__tiles[self.__tiles.index(tile)] = struct(tile.pos)

    def __repr__(self):
        """Return a readable representation of the board."""
        return repr(self.__tiles)

    def __getitem__(self, pos):
        """Allow subscriptable access to tiles."""
        return self.__tiles[pos]

    def __len__(self):
        """Return the number of tiles."""
        return len(self.__tiles)

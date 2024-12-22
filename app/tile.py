"""Tile generations"""
from random import randint as rint

class Tile:
    """Base Tile definition"""
    def __init__(self, pos):
        """Initialize a generic tile with its position."""
        self.pos = pos

    def __repr__(self):
        """Return a string representation of the tile."""
        return str(self.pos)

class Structure(Tile):
    """base structure definition"""
    def __init__(self, pos, name, action):
        """Initialize a structure with its position, name, and action."""
        super().__init__(pos)
        self.name = name.capitalize()
        self.action = action

    def __repr__(self):
        """Return a string representation of the structure."""
        return f"{self.name[0].upper()}{self.pos}"

class Hotel(Structure):
    """Hotels!!!"""
    def __init__(self, pos):
        """Initialize a hotel with a 'skip turn' action."""
        super().__init__(pos, "Hotel", "skip")

class Bridge(Structure):
    """dont fall off"""
    def __init__(self, pos):
        """Initialize a bridge with a random jump action."""
        super().__init__(pos, "Bridge", rint(1, 6))  # Random jump between 1 and 6

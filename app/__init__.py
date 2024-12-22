"""Definition of main game logic"""
from random import randint
from .board import Board
from .tile import Structure

class Game:
    """Game of GOOOSE"""
    def __init__(self, *players):
        self.board = Board()
        self.players = {player: 1 for player in players}  # Player positions
        self.skip_turn = set()  # Tracks players who need to skip their next turn

    def roll(self):
        """Simulate a dice roll (1 to 6)."""
        return randint(1, 6)

    def process(self, player):
        """Process actions based on the player's landing position."""
        pos = self.players[player]
        if pos < 1 or pos > 64:
            # Bounce player back to the 64th position if they go beyond the board
            self.players[player] = 64 - (pos - 64) if pos > 64 else 1
            return

        current_tile = self.board[pos - 1]  # Convert 1-based pos to 0-based index
        print(f"{player} landed on {current_tile}")

        # Detect infinite loops by maintaining a history of visited positions
        visited_positions = set()

        while isinstance(current_tile, Structure):
            if pos in visited_positions:
                print(f"{player} is stuck in a loop at position {pos}. Breaking recursion.")
                return  # Break out of the loop to prevent infinite recursion

            visited_positions.add(pos)

            if current_tile.action == "skip":
                print(f"{player} will skip their next turn...")
                self.skip_turn.add(player)
                return

            print(f"{player} takes action: {current_tile.action}")
            self.players[player] += current_tile.action

            # Clamp the player's position within bounds
            if self.players[player] > 64:
                overflow = self.players[player] - 64
                self.players[player] = 64 - overflow
            elif self.players[player] < 1:
                self.players[player] = 1

            pos = self.players[player]
            current_tile = self.board[pos - 1]  # Update current tile

    def generate_spiral(self, size):
        """Generate a list of tile positions in a spiral order for an `size` x `size` board."""
        # Initialize a 2D list of the same size
        spiral = [[0] * size for _ in range(size)]
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Right, Down, Left, Up
        x, y = 0, 0  # Start at the top-left corner
        current_dir = 0
        current_value = 1

        while current_value <= size * size:
            spiral[x][y] = current_value
            current_value += 1

            # Try to move in the current direction
            next_x, next_y = x + directions[current_dir][0], y + directions[current_dir][1]

            # If the next position is out of bounds or already filled, change directions
            if (0 <= next_x < size and 0 <= next_y < size and spiral[next_x][next_y] == 0):
                x, y = next_x, next_y
            else:
                current_dir = (current_dir + 1) % 4  # Turn to the next direction
                x, y = x + directions[current_dir][0], y + directions[current_dir][1]

        return spiral

    def show(self):
        """Display the board in a spiral with player and structure locations."""
        # Create a 2D array to represent the board in spiral order
        spiral_positions = self.generate_spiral(8)

        board_display = ""

        for i in range(8):
            row_display = ""
            for j in range(8):
                pos = spiral_positions[i][j]  # Get the spiral position for the current tile
                current_tile = self.board[pos - 1]  # Get the tile at the position

                player_on_tile = [
                    player
                    for player, player_pos in self.players.items()
                    if player_pos == pos
                ]

                if player_on_tile:
                    # Display player's name instead of the tile number
                    row_display += f" {player_on_tile[0]:^6} |"
                else:
                    # Display the tile's type (repr) if no player is on it
                    row_display += f" {str(current_tile):^6} |"

            # Remove trailing '|' and add the row to the board display
            board_display += row_display.rstrip('|') + "\n"

        print(board_display)

    def main(self):
        """Main game loop."""
        winner = None
        while winner is None:
            for player in self.players.keys():
                print(f"\n{player}'s turn! Current position: {self.players[player]}")
                self.show()

                # Check if the player needs to skip their turn
                if player in self.skip_turn:
                    print(f"{player} is skipping their turn (Hotel).")
                    self.skip_turn.remove(player)
                    continue

                # Roll the dice
                #input("Press Enter to roll the dice...")
                roll = self.roll()
                print(f"{player} rolled a {roll}!")
                self.players[player] += roll

                # Process the landing tile
                self.process(player)

                # Check for a winner
                if self.players[player] == 64:
                    winner = player
                    break

        print(f"\nCongratulations, {winner} wins!")

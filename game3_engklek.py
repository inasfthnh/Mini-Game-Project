"""
ROUND 3 - Engklek Survival (Path Selection Game)
Inspired by Engklek, the Indonesian hopscotch-like game.

The player must hop across 5 rows of tiles.
Each row has a LEFT tile and a RIGHT tile; one is safe, one is cracked.
Choose the safe tile to advance — choose wrong and you fall!
"""

import random
import time

NUM_ROWS      = 5     # total rows to cross
SAFE_SYMBOL   = "🟩"  # shown after the choice
CRACK_SYMBOL  = "🟥"
UNKNOWN_LEFT  = "[ L ]"
UNKNOWN_RIGHT = "[ R ]"


class EngklekSurvival:

    def __init__(self, player_no: str):
        self.player_no = player_no
        self.current_row = 0
        self.alive = True
        self.status = False

        # Pre-generate the board: list of dicts, one per row
        # Each dict: { "safe": "L" or "R", "revealed": False }
        self.board = self.generate_board()

    def generate_board(self) -> list:
        """Return a list of row configurations."""
        board = []
        for _ in range(NUM_ROWS):
            board.append({
                "safe": random.choice(["L", "R"]),
                "revealed": False,
            })
        return board

    def play(self) -> bool:
        print(f"\n  👤  Player {self.player_no} turn...")

        for row_index in range(NUM_ROWS):
            self.current_row = row_index
            survived = self.play_row(row_index)
            if not survived:
                self.alive = False
                break
        self.status = survived
        return self.finish()

    def play_row(self, row_index: int) -> bool:
        self.print_board(reveal_up_to=row_index)
        print(f"\n  ➡️  Row {row_index + 1} of {NUM_ROWS}  — Choose your tile:")
        print(f"      {UNKNOWN_LEFT}  or  {UNKNOWN_RIGHT}")

        choice = self.get_choice()
        safe_side = self.board[row_index]["safe"]
        self.board[row_index]["revealed"] = True   # mark for display

        time.sleep(0.5)
        self.print_board(reveal_up_to=row_index + 1)

        if choice == safe_side:
            print(f"\n  ✅  Safe! Player {self.player_no} hopped to the {choice} tile.\n")
            time.sleep(0.7)
            return True
        else:
            print(f"\n  💀  Cracked tile! Player {self.player_no} FELL through the floor!\n")
            time.sleep(0.8)
            return False

    def print_board(self, reveal_up_to: int) -> None:
        print("\n  ╔══════════════════════════╗")
        print("  ║   ENGKLEK BOARD          ║")
        print("  ╠══════════════════════════╣")

        for i in range(NUM_ROWS-1, -1, -1):   # print top→bottom (row 5 first)
            row = self.board[i]
            row_label = f"Row {i + 1}"

            if i < reveal_up_to and row["revealed"]:
                safe = row["safe"]
                left  = SAFE_SYMBOL  if safe == "L" else CRACK_SYMBOL
                right = SAFE_SYMBOL  if safe == "R" else CRACK_SYMBOL
                print(f"  ║  {row_label}:  {left}  {right}      ║")
            elif i == self.current_row and i < reveal_up_to:
                # Currently being revealed
                safe = row["safe"]
                left  = SAFE_SYMBOL  if safe == "L" else CRACK_SYMBOL
                right = SAFE_SYMBOL  if safe == "R" else CRACK_SYMBOL
                print(f"  ║   {row_label}:    {left}      {right}   ◀   ║")
            else:
                print(f"  ║   {row_label}:  {UNKNOWN_LEFT}  {UNKNOWN_RIGHT}   ║")

        print("  ╠══════════════════════════╣")
        print("  ║         🏁  START        ║")
        print("  ╚══════════════════════════╝")

    def get_choice(self) -> str:
        valid_inputs = {
            "l": "L", "left":  "L",
            "r": "R", "right": "R"
        }

        while True:
            raw = input(f"  Player {self.player_no} choice (L / R): ").strip().lower()
            if raw in valid_inputs:
                return valid_inputs[raw]
            print("  ⚠️  Please type L (left) or R (right).")

    def finish(self) -> bool:
        print("\n" + "─" * 45)
        if self.alive:
            print(f"  🎊  Player {self.player_no} crossed all {NUM_ROWS} rows!")
        else:
            print(f"  Row reached: {self.current_row} / {NUM_ROWS}")
        print("─" * 45)
        return self.status

    def print_intro() -> None:
        print("\n" + "╔" + "═" * 43 + "╗")
        print("║     🦘  ROUND 3 - ENGKLEK SURVIVAL          ║")
        print("╚" + "═" * 43 + "╝")
        print(f"""
  Hop across {NUM_ROWS} rows of tiles.
  Each row: one tile is SAFE {SAFE_SYMBOL}, one is CRACKED {CRACK_SYMBOL}.
  Choose LEFT or RIGHT — get it wrong and you fall!
""")
        time.sleep(1)

"""
ROUND 2 - Bekel Challenge (Memory Sequence Game)
Inspired by the traditional Indonesian game of bekel (jack-stones).

The computer shows a growing sequence of bekel items.
The player must recall and type the exact sequence back.
Sequences grow by 1 item each level.  Fail twice → eliminated.
"""

import random
import time

BEKEL_ITEMS = [
    "Bola",       # ball
    "Kupu",       # butterfly-shaped jack
    "Kerang",     # shell
    "Bintang",    # star piece
    "Daun"       # leaf
]

MAX_LEVELS   = 2    # sequence grows up
LIVES        = 2    # mistakes allowed before elimination


class BekelChallenge:

    def __init__(self, player_no: str):
        self.player_no = player_no
        self.sequence = []          # the master sequence (grows each level)
        self.level = 0
        self.lives_remaining = LIVES
        self.status = False

    def play(self) -> bool:
        print(f"\n  👤  Player {self.player_no} turn...")
        
        for level_num in range(1, MAX_LEVELS + 1):
            self.level = level_num
            survived = self.run_level()

            if not survived:
                break   # player was eliminated
        self.status = survived
        return self.finish()

    def run_level(self) -> bool:
        # Extend sequence with one new random item
        new_item = random.choice(BEKEL_ITEMS)
        self.sequence.append(new_item)

        print(f"\n  ─── Level {self.level}  (sequence length: {self.level}) ───")
        print(f"  Lives remaining: {'❤️ ' * self.lives_remaining}\n")

        # Show the sequence
        self.show_sequence()

        # Player attempts to recall
        attempt = self.get_player_input()

        # Validate
        if attempt == self.sequence:
            print("  ✅  Correct! Well done.\n")
            time.sleep(0.8)
            return True
        else:
            self.lives_remaining -= 1
            print("  ❌  Wrong sequence!")
            print(f"  Expected : {' → '.join(self.sequence)}")
            print(f"  Player {self.player_no} typed: {' → '.join(attempt)}\n")

            if self.lives_remaining > 0:
                print(f"  ⚠️  Player {self.player_no} has {self.lives_remaining} life/lives left. Try again!\n")
                time.sleep(0.8)
                # Allow one retry on the same level
                self.show_sequence()
                retry = self.get_player_input()
                if retry == self.sequence:
                    print("  ✅  Correct on retry!\n")
                    time.sleep(0.8)
                    return True
                else:
                    self.lives_remaining -= 1
                    print("  ❌  Retry failed.\n")

            if self.lives_remaining <= 0:
                print(f"  💀  No lives left. Player {self.player_no} is ELIMINATED from Bekel!")
                return False

            return False

    def show_sequence(self) -> None:
        display_time = max(1.5, 1 * len(self.sequence))   # longer = more time

        print("  📿  MEMORIZE the sequence: \n")
        # Build a numbered display
        for i, item in enumerate(self.sequence, start=1):
            print(f"      {i}. {item}")
        print()
        print(f"  (Player {self.player_no} has {display_time:.1f} seconds...)")
        time.sleep(display_time)

        # "Clear" the screen with blank lines so they can't peek
        print("\n" * 5)
        print("  🔲 " * 12)
        print("  Sequence hidden! What was it?\n")

    def get_player_input(self) -> list:
        print("  Available items:", "  |  ".join(BEKEL_ITEMS))
        print("  (Type each item name exactly, one per line)\n")

        player_answer = []
        for i in range(1, len(self.sequence) + 1):
            while True:
                answer = input(f"    Item {i}: ").strip().capitalize()
                if answer in BEKEL_ITEMS:
                    player_answer.append(answer)
                    break
                else:
                    print(f"    ⚠️  '{answer}' is not a valid item. Choose from the list above.")

        return player_answer

    def finish(self) -> bool:
        print("\n" + "─" * 45)
        print(f"  Player {self.player_no} bekel levels completed : {self.level}")
        print("─" * 45)
        return self.status

    def print_intro() -> None:
        print("\n" + "╔" + "═" * 43 + "╗")
        print("║       🎯  ROUND 2 - BEKEL CHALLENGE           ║")
        print("╚" + "═" * 43 + "╝")
        print(f"""
  A sequence of bekel items will flash before you.
  Memorise it, then type each item back in order.
  
  Sequences grow longer each level (up to {MAX_LEVELS} items).
  You have {LIVES} lives total.  Good luck!
""")
        time.sleep(1)

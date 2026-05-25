"""
ROUND 1 - Suit Jawa (Gajah - Orang - Semut)
A best-of-5 hand-gesture game (Indonesian rock-paper-scissors).

  Gajah  (Elephant) 🐘  beats  Orang (Human)  👤
  Orang  (Human)    👤  beats  Semut (Ant)    🐜
  Semut  (Ant)      🐜  beats  Gajah (Elephant) 🐘
  (The ant crawls into the elephant's ear and wins!)
"""

import random
import time

# ─────────────────────────────────────────────
#  Game constants stored in a dictionary
# ─────────────────────────────────────────────
CHOICES: dict = {
    "1": ("Gajah", "🐘"),
    "2": ("Orang", "👤"),
    "3": ("Semut", "🐜"),
}

# { winner > loser }
BEATS: dict = {
    "Gajah": "Orang",
    "Orang": "Semut",
    "Semut": "Gajah",
}

ROUNDS_TO_WIN = 3 

class SuitJawa:

    def __init__(self, player_no: str):
        self.player_no = player_no
        self.player_wins = 0
        self.computer_wins = 0
        self.ties = 0
        self.status = False

    def play(self) -> bool:
        # Main game loop
        print(f"\n  👤  Player {self.player_no} turn...")
        while self.player_wins < ROUNDS_TO_WIN and self.computer_wins < ROUNDS_TO_WIN:
            self.play_one_round()

        return self.finish()

    def play_one_round(self) -> None:
        print(f"  Score → Player {self.player_no}: {self.player_wins}  |  Budi: {self.computer_wins}\n")

        # Display menu
        for key, (name, emoji) in CHOICES.items():
            print(f"    [{key}] {emoji}  {name}")

        # Validate player input with a loop
        player_key = ""
        while player_key not in CHOICES:
            player_key = input(f"\n  Player {self.player_no}'s choice (1/2/3): ").strip()
            if player_key not in CHOICES:
                print("  ⚠️  Please enter 1, 2, or 3.")

        player_choice, player_emoji = CHOICES[player_key]

        # Computer picks randomly from the list of choice keys
        computer_key = random.choice(list(CHOICES.keys()))
        computer_choice, computer_emoji = CHOICES[computer_key]

        print(f"\n  Player {self.player_no} chose  : {player_emoji}  {player_choice}")
        time.sleep(0.4)
        print(f"  Budi   : {computer_emoji}  {computer_choice}")
        time.sleep(0.4)

        # Determine winner using the BEATS dictionary
        result = self.determine_result(player_choice, computer_choice)

        if result == "win":
            self.player_wins += 1
            print(f"  ✅  Player {self.player_no} WIN this round!\n")
        elif result == "lose":
            self.computer_wins += 1
            print(f"  ❌  Player {self.player_no} LOSE this round!\n")
        else:
            self.ties += 1
            print("  🤝  TIE - play again!\n")
            return

        time.sleep(0.6)

    def determine_result(self, player: str, computer: str) -> str:
        if player == computer:
            return "tie"
        elif BEATS[player] == computer:
            return "win"
        else:
            return "lose"

    def finish(self) -> bool:
        print("\n" + "─" * 55)
        if self.player_wins >= ROUNDS_TO_WIN:
            print(f"  🎉  Player {self.player_no} WINS the Suit Jawa match!")
            self.status = True
        else:
            print(f"  🤖🧒  Budi wins. Player {self.player_no} is ELIMINATED from Suit Jawa.")
            self.status = False

        print(f"  Final: Player [{self.player_no}] {self.player_wins} - {self.computer_wins} Budi  |  Ties: {self.ties}")
        print("─" * 55)
        return self.status

    def print_intro() -> None:
        print("\n" + "╔" + "═" * 52 + "╗")
        print("║   🎮  ROUND 1 - SUIT JAWA (GAJAH-ORANG-SEMUT)  ║")
        print("╚" + "═" * 52 + "╝")
        print("""
  Rules:
    🐘 Gajah  beats  👤 Orang  (elephant crushes human)
    👤 Orang  beats  🐜 Semut  (human squashes ant)
    🐜 Semut  beats  🐘 Gajah  (ant enters elephant's ear)

  Beat computer doll [Budi 🤖🧒] and WIN 3 rounds to survive!
""")
        time.sleep(1)
"""
Defines the Player class that tracks the player's number,
and survival status throughout the game collection.
"""

class Player:

    def __init__(self, player_no: str):
        self.player_no = player_no
        self.survived_rounds = 0
        self.eliminated = False
        self.round_results: dict = {} 

    def eliminate(self) -> None:
        self.eliminated = True

    def record(self, round_name: str, win: bool) -> None:
        if win:
            self.round_results[round_name] = "✅"
            self.survived_rounds += 1
        else:
            self.round_results[round_name] = "❌"
            self.eliminate()

    def summary(self) -> None:
        status = "❌  ELIMINATED" if self.eliminated else "✅  ALIVE"

        print("\n" + "=" * 46)
        print(f"  📋  PLAYER  [{self.player_no}]")
        print("=" * 46)
        print(f"  Status          : {status}")
        print(f"  Rounds survived : {self.survived_rounds} / 3")
        print("  Round results   :")

        for round_name, result in self.round_results.items():
            print(f"    {result}  {round_name}")

        print("=" * 46)

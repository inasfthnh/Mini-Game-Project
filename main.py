"""
INDONESIAN SQUID GAME - Mini-Game Collection
================================================
A three-round survival game inspired by traditional Indonesian children's
games in the style of Squid Game.

Round 1 → Suit Jawa    (Gajah - Orang - Semut)
Round 2 → Bekel        (Memory sequence challenge)
Round 3 → Engklek      (Hop across the board)

=== RUN this file (main.py) to start the game ===
"""

import time

from player import Player
from config import assign_player_number, save_player, list_player, display_playersboard, display_summary, reset_registry
from game1_suit_jawa import SuitJawa
from game2_bekel import BekelChallenge
from game3_engklek import EngklekSurvival

def print_banner() -> None:
    banner = """
╔═══════════════════════════════════════════════════╗
║                                                   ║
║            🦑  INDONESIAN SQUID GAME  🦑          ║
║                                                   ║
║   Welcome, Players!                               ║
║   Your fate now depends on your skill.            ║
║   Survive all rounds to win Rp 530,633,520,000!   ║
║                                                   ║
║                     ⭕ 🔺 🟥                       ║
╚═══════════════════════════════════════════════════╝
"""
    print(banner)

def show_round_transition(round_num: int, title: str) -> None:
    print("\n\n  " + "★" * 42)
    print(f"  ★{'ROUND ' + str(round_num) + ':  ' + title.upper():^40}★")
    print("  " + "★" * 42 + "\n")
    time.sleep(1.2)

def show_menu() -> str:
    menu_options = {
        "1": "🎮  Play the game",
        "2": "🏆  View players",
        "3": "❌  Quit"
    }

    print("\n  ┌─────────────────────────────┐")
    print("  │        MAIN MENU            │")
    print("  ├─────────────────────────────┤")
    for key, label in menu_options.items():
        print(f"  │  [{key}]  {label:<21}│")
    print("  └─────────────────────────────┘ \n")

    while True:
        choice = input("  Choose an option (1 / 2 / 3): ").strip()
        if choice in menu_options:
            return choice
        print("  ⚠️  Invalid option. Please enter 1, 2, or 3.")

def play_continue() -> bool:
    voting = 0
    print(f"\n  🗳️  Game voting start!")
    for player_no in list_player("survived"):
        choice = ""
        while choice not in ["y", "n"]:
            choice = input(f"  Player {player_no}, do you want to continue (Y/N)? ").lower()
            if choice == "y":
                voting += 1
                print(f"  🇴  Player {player_no} want to continue...")
            elif choice == "n":
                print(f"  ❌  Player {player_no} want to stop the game!")
            else:
                print("  ⚠️  Please choose (Y / N).")
    if voting >= len(list_player("survived")) // 2:
        return True
    else: 
        return False

# ─────────────────────────────────────────────
#  Core game flow
# ─────────────────────────────────────────────

def run_game() -> None:
    # ── ROUND 1: Suit Jawa ──
    show_round_transition(1, "Suit Jawa")
    SuitJawa.print_intro()
    for player_no in list_player("registered"):
        player = Player(player_no)
        suit_game = SuitJawa(player.player_no).play()
        player.record("Suit Jawa", suit_game)
        save_player(player.player_no, suit_game)

    if list_player("survived"):
        display_playersboard()
        if play_continue():
            print("\n  ✅  Players Survived advances to Round 2!\n")
        else:
            print("\n  🛑  Players agree to stop the game!  🛑")
            display_summary()
            return
    else:
        print("  💀  No Players Survived...")
        return
    time.sleep(1)
    
    # ── ROUND 2: Bekel Challenge ──
    show_round_transition(2, "Bekel Challenge")
    BekelChallenge.print_intro()
    for player_no in list_player("survived")[:]:
        player = Player(player_no)
        bekel_game = BekelChallenge(player.player_no).play()
        player.record("Bekel Challenge", bekel_game)
        save_player(player.player_no, bekel_game)

    if list_player("survived"):
        display_playersboard()
        if play_continue():
            print("\n  ✅  Players Survived advances to Round 3!\n")
        else:
            print("\n  🛑  Players agree to stop the game!  🛑")
            display_summary()
            return
    else:
        print("  💀  No Players Survived...")
        return
    time.sleep(1)

    # ── ROUND 3: Engklek Survival ──
    show_round_transition(3, "Engklek Survival - FINAL")
    EngklekSurvival.print_intro()
    for player_no in list_player("survived")[:]:
        player = Player(player_no)
        engklek_game  = EngklekSurvival(player.player_no).play()
        player.record("Engklek Survival", engklek_game)
        save_player(player.player_no, engklek_game)

    if list_player("survived"):
        print("\n  🏆  Congratulations for all winners!\n")
        display_summary()
    else:
        print("  💀  No Players Survived...")
    
    time.sleep(1)
    return

# ─────────────────────────────────────────────
#  Entry point
# ─────────────────────────────────────────────

def main() -> None:
    print_banner()

    while True:
        choice = show_menu()

        if choice == "1":
            reset_registry() 
            no_players = int(input("How many players want to play the game? "))
            for _ in range(no_players):
                player_no = assign_player_number()
                print(f"\n  Welcome, Player {player_no}! Prepare yourself...")
                time.sleep(0.5)

            time.sleep(1)
            run_game()

        elif choice == "2":
            display_playersboard()

        elif choice == "3":
            break

    print("\n  👋  Thanks for playing! Sampai jumpa!\n")


if __name__ == "__main__":
    main()

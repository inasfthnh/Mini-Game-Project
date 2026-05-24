import random

REGISTRY_FILE = "player_registry.txt"
MIN_NUMBER    = 1
MAX_NUMBER    = 999
TOTAL_SLOTS   = MAX_NUMBER
players_survived = []
players_eliminated = []
players_registered = []

def load_used_numbers() -> list:
    used_numbers = []
    with open(REGISTRY_FILE, "r") as f:
        for line in f:
            line = line.strip()
            if not line:   # skip blank lines and comments
                continue
            try:
                used_numbers.append(int(line))
            except ValueError:
                continue # skip the text
    return used_numbers

def assign_player_number() -> str:
    used = load_used_numbers()
    available = list(set(range(MIN_NUMBER, MAX_NUMBER + 1)) - set(used))
    if not available:
        raise ValueError("All player numbers (001-999) are taken.")

    chosen = random.choice(available)
    used.append(chosen)
    save_registry(used)
    players_registered.append(f"{chosen:03d}")

    return f"{chosen:03d}"

def save_registry(used: list) -> None:
    with open(REGISTRY_FILE, "w") as f:
        f.write("=== Indonesian Squid Game - Player Registry ===\n")
        for number in sorted(used):
            f.write(f"{number:03d}\n")

def reset_registry() -> None:
    save_registry(list())

def save_player(player: int, win: bool) -> None:
    if win:
        players_survived.append(player)
    else:
        if player in players_survived:
            players_survived.remove(player)
        players_eliminated.append(player)

def list_player(check: str) -> list:
    if check == "survived":
        ls = players_survived
    elif check == "eliminated":
        ls = players_eliminated
    elif check == "registered":
        ls = players_registered
    else:
        return []

    return ls

def display_playersboard() -> None:
    if not players_survived:
        data = players_registered
    else:
        data = players_survived

    print("\n" + "=" * 40)
    print("  👤  PLAYER BOARD - SURVIVORS")
    print("=" * 40)

    if not data:
        print("  No players saved yet. Be the first!")
    else:
        for player in data:
            print(f"  {player}  \n")
        print("=" * 40)
        print("  💰 Money Prize For Each Player : ")
        print("         Rp", (530633520000/len(data)))

    print("=" * 40)

def display_summary() -> None:
    data = players_survived

    print("\n" + "=" * 40)
    print(f"  📋  PLAYERS WON SUMMARY:")
    print("=" * 40)

    if not data:
        print("  No players survived!")
    else:
        for player in data:
                print(f"  {player}  \n")
        print("=" * 45)
        print("  TOTAL MONEY PRIZE FOR EACH PLAYER :")
        print("       Rp", (530633520000/len(data)))
        print("  ", "💸" * 15)
        
    print("=" * 40)
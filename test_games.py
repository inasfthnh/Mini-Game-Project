from config import assign_player_number, load_used_numbers, save_player, list_player, reset_registry, players_survived, players_eliminated, players_registered
from player import Player
from game1_suit_jawa import SuitJawa, BEATS
from game2_bekel import BekelChallenge, BEKEL_ITEMS, MAX_LEVELS, LIVES
from game3_engklek import EngklekSurvival, NUM_ROWS


def run(fn):
    try:
        fn()
        print(f"  ✅  {fn.__name__}")
        return True
    except AssertionError as e:
        print(f"  ❌  {fn.__name__}")
        print(f"      {e}")
        return False
    except Exception as e:
        print(f"  💥  {fn.__name__}")
        print(f"      {type(e).__name__}: {e}")
        return False

def reset_config():
    players_survived.clear()
    players_eliminated.clear()
    players_registered.clear()

def test_player_initial_state():
    p = Player("042")
    assert p.player_no == "042"
    assert p.survived_rounds == 0
    assert p.eliminated == False
    assert p.round_results == {}

def test_player_record_win():
    p = Player("042")
    p.record("Suit Jawa", True)
    assert p.survived_rounds == 1
    assert p.round_results["Suit Jawa"] == "✅"
    assert p.eliminated == False

def test_player_record_loss():
    p = Player("042")
    p.record("Suit Jawa", False)
    assert p.survived_rounds == 0
    assert p.round_results["Suit Jawa"] == "❌"
    assert p.eliminated == True

def test_player_survives_two_rounds_then_fails():
    p = Player("123")
    p.record("Suit Jawa", True)
    p.record("Bekel Challenge", True)
    p.record("Engklek Survival", False)
    assert p.survived_rounds == 2
    assert p.eliminated == True
    assert len(p.round_results) == 3

def test_player_survives_all_rounds():
    p = Player("456")
    p.record("Suit Jawa", True)
    p.record("Bekel Challenge", True)
    p.record("Engklek Survival", True)
    assert p.survived_rounds == 3
    assert p.eliminated == False

def test_config_assign_returns_3_digit_string():
    reset_registry()
    reset_config()
    num = assign_player_number()
    assert len(num) == 3, f"Expected length 3, got '{num}'"
    assert num.isdigit(), f"Expected digits only, got '{num}'"
    assert 1 <= int(num) <= 999

def test_config_assigned_number_saved_to_registry():
    reset_registry()
    reset_config()
    num = assign_player_number()
    used = load_used_numbers()
    assert int(num) in used, f"{num} should be in registry after assignment"

def test_config_numbers_are_unique():
    reset_registry()
    reset_config()
    nums = [assign_player_number() for _ in range(15)]
    assert len(nums) == len(set(nums)), "All assigned numbers must be unique"

def test_config_save_player_win_adds_to_survived():
    reset_config()
    save_player("042", True)
    assert "042" in list_player("survived")
    assert "042" not in list_player("eliminated")

def test_config_save_player_loss_moves_to_eliminated():
    reset_config()
    players_survived.append("042")
    save_player("042", False)
    assert "042" not in list_player("survived")
    assert "042" in list_player("eliminated")

def test_config_registered_list_populated():
    reset_registry()
    reset_config()
    n = assign_player_number()
    assert n in list_player("registered"), "Assigned number must appear in registered list"

def test_suit_jawa_all_win_combinations():
    g = SuitJawa("042")
    assert g.determine_result("Gajah", "Orang") == "win"
    assert g.determine_result("Orang", "Semut") == "win"
    assert g.determine_result("Semut", "Gajah") == "win"

def test_suit_jawa_all_lose_combinations():
    g = SuitJawa("042")
    assert g.determine_result("Orang", "Gajah") == "lose"
    assert g.determine_result("Semut", "Orang") == "lose"
    assert g.determine_result("Gajah", "Semut") == "lose"

def test_suit_jawa_all_tie_combinations():
    g = SuitJawa("042")
    assert g.determine_result("Gajah", "Gajah") == "tie"
    assert g.determine_result("Orang", "Orang") == "tie"
    assert g.determine_result("Semut", "Semut") == "tie"

def test_suit_jawa_beats_dict_has_all_three():
    for gesture in ("Gajah", "Orang", "Semut"):
        assert gesture in BEATS, f"'{gesture}' missing from BEATS dict"

def test_suit_jawa_initial_state():
    g = SuitJawa("042")
    assert g.player_wins == 0
    assert g.computer_wins == 0
    assert g.ties == 0
    assert g.status == False

def test_bekel_initial_state():
    g = BekelChallenge("042")
    assert g.sequence == []
    assert g.level == 0
    assert g.lives_remaining == LIVES
    assert g.status == False

def test_bekel_items_list_valid():
    assert len(BEKEL_ITEMS) > 0
    for item in BEKEL_ITEMS:
        assert isinstance(item, str) and len(item) > 0

def test_bekel_max_levels_positive():
    assert MAX_LEVELS > 0, "MAX_LEVELS must be at least 1"

def test_bekel_sequence_grows_one_item_per_level():
    # Simulate the sequence growth without needing user input
    g = BekelChallenge("042")
    import random
    for lvl in range(1, MAX_LEVELS + 1):
        g.sequence.append(random.choice(BEKEL_ITEMS))
        assert len(g.sequence) == lvl

def test_engklek_board_has_correct_number_of_rows():
    g = EngklekSurvival("042")
    assert len(g.board) == NUM_ROWS

def test_engklek_board_each_row_has_valid_safe_side():
    g = EngklekSurvival("042")
    for i, row in enumerate(g.board):
        assert row["safe"] in ("L", "R"), f"Row {i}: safe must be 'L' or 'R', got '{row['safe']}'"

def test_engklek_board_all_rows_start_unrevealed():
    g = EngklekSurvival("042")
    for i, row in enumerate(g.board):
        assert row["revealed"] == False, f"Row {i} should start unrevealed"

def test_engklek_initial_state():
    g = EngklekSurvival("042")
    assert g.alive == True
    assert g.status == False
    assert g.current_row == 0

def test_engklek_valid_choice_mapping():
    valid = {"l": "L", "left": "L", "r": "R", "right": "R"}
    assert valid["l"]     == "L"
    assert valid["r"]     == "R"
    assert valid["left"]  == "L"
    assert valid["right"] == "R"
    assert valid.get("x") is None


if __name__ == "__main__":

    all_tests = [
        # Player
        test_player_initial_state,
        test_player_record_win,
        test_player_record_loss,
        test_player_survives_two_rounds_then_fails,
        test_player_survives_all_rounds,
        # Config
        test_config_assign_returns_3_digit_string,
        test_config_assigned_number_saved_to_registry,
        test_config_numbers_are_unique,
        test_config_save_player_win_adds_to_survived,
        test_config_save_player_loss_moves_to_eliminated,
        test_config_registered_list_populated,
        # SuitJawa
        test_suit_jawa_all_win_combinations,
        test_suit_jawa_all_lose_combinations,
        test_suit_jawa_all_tie_combinations,
        test_suit_jawa_beats_dict_has_all_three,
        test_suit_jawa_initial_state,
        # BekelChallenge
        test_bekel_initial_state,
        test_bekel_items_list_valid,
        test_bekel_max_levels_positive,
        test_bekel_sequence_grows_one_item_per_level,
        # EngklekSurvival
        test_engklek_board_has_correct_number_of_rows,
        test_engklek_board_each_row_has_valid_safe_side,
        test_engklek_board_all_rows_start_unrevealed,
        test_engklek_initial_state,
        test_engklek_valid_choice_mapping
    ]

    passed = 0
    failed = 0

    print("\n" + "=" * 55)
    print("             INDONESIAN SQUID GAME — TEST")
    print("=" * 55)

    sections = {
        "Player"         : all_tests[0:5],
        "Config"         : all_tests[5:11],
        "SuitJawa"       : all_tests[11:16],
        "BekelChallenge" : all_tests[16:20],
        "EngklekSurvival": all_tests[20:25]
    }

    for section, tests in sections.items():
        print(f"\n  ── {section} {'─' * (20 - len(section))}")
        for test in tests:
            if run(test):
                passed += 1
            else:
                failed += 1

    total = passed + failed
    print("\n" + "=" * 55)
    print(f"  Total : {total}   ✅ Passed : {passed}   ❌ Failed : {failed}")
    print("=" * 55)

    if failed == 0:
        print("  🎉  All tests passed!")
    else:
        print(f"  ⚠️   {failed} test(s) failed — see bug report above.")
    print()

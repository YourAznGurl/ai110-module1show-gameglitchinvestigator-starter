from logic_utils import (
    check_guess,
    get_range_for_difficulty,
    new_game_state,
    update_score,
)


def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    outcome, message = check_guess(50, 50)
    assert outcome == "Win"


def test_guess_too_high():
    # If secret is 50 and guess is 60, outcome should be "Too High"
    outcome, message = check_guess(60, 50)
    assert outcome == "Too High"
    assert "LOWER" in message  # catches the swapped-hint bug


def test_guess_too_low():
    # If secret is 50 and guess is 40, outcome should be "Too Low"
    outcome, message = check_guess(40, 50)
    assert outcome == "Too Low"
    assert "HIGHER" in message  # catches the swapped-hint bug


def test_new_game_resets_state():
    # New Game should reset status, score, history, and respect the difficulty range
    state = new_game_state("Easy")
    assert state["status"] == "playing"
    assert state["score"] == 0
    assert state["attempts"] == 0
    assert state["history"] == []
    low, high = get_range_for_difficulty("Easy")
    assert low <= state["secret"] <= high


def test_win_on_first_guess_scores_100():
    assert update_score(0, "Win", 1) == 100


def test_win_bonus_shrinks_with_each_guess():
    assert update_score(0, "Win", 8) == 30


def test_win_bonus_has_a_minimum_of_10():
    assert update_score(0, "Win", 15) == 10


def test_wrong_guess_costs_5_on_any_attempt():
    # Too High used to give +5 on even attempts
    assert update_score(50, "Too High", 2) == 45
    assert update_score(50, "Too High", 3) == 45
    assert update_score(50, "Too Low", 2) == 45


def test_score_never_goes_below_zero():
    assert update_score(0, "Too Low", 1) == 0
    assert update_score(3, "Too High", 2) == 0
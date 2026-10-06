import random


def get_range_for_difficulty(difficulty: str):
    """Return (low, high) inclusive range for a given difficulty."""
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 100
    if difficulty == "Hard":
        return 1, 50
    return 1, 100


def parse_guess(raw: str):
    """
    Parse user input into an int guess.

    Returns: (ok: bool, guess_int: int | None, error_message: str | None)
    """
    if raw is None:
        return False, None, "Enter a guess."

    if raw == "":
        return False, None, "Enter a guess."

    try:
        if "." in raw:
            value = int(float(raw))
        else:
            value = int(raw)
    except Exception:
        return False, None, "That is not a number."

    return True, value, None


# FIX: Hint messages were swapped and a string-secret fallback broke comparisons.
# Refactored into logic_utils.py with AI assistance; verified with pytest.
def check_guess(guess, secret):
    """
    Compare guess to secret and return (outcome, message).

    outcome examples: "Win", "Too High", "Too Low"
    """
    if guess == secret:
        return "Win", "🎉 Correct!"
    if guess > secret:
        return "Too High", "📉 Go LOWER!"
    return "Too Low", "📈 Go HIGHER!"


# FIX: Scoring was inconsistent (Too High on even attempts gave +5, win bonus used
# attempt_number + 1, and scores could go negative). Rewritten with AI assistance;
# verified with pytest.
def update_score(current_score: int, outcome: str, attempt_number: int):
    """
    Update score based on outcome and attempt number.

    attempt_number is the number of the guess just made (first guess = 1).
    A win earns 100 minus 10 per earlier guess, with a minimum of 10.
    Every wrong guess costs 5 points. The score never drops below 0.
    """
    if outcome == "Win":
        points = 100 - 10 * (attempt_number - 1)
        if points < 10:
            points = 10
        return current_score + points

    if outcome in ("Too High", "Too Low"):
        return max(0, current_score - 5)

    return current_score


# FIX: New Game now builds a full fresh state (status, score, history, secret in range).
def new_game_state(difficulty: str):
    """Return a fresh set of session values for a new game."""
    low, high = get_range_for_difficulty(difficulty)
    return {
        "secret": random.randint(low, high),
        "attempts": 0,
        "score": 0,
        "status": "playing",
        "history": [],
    }
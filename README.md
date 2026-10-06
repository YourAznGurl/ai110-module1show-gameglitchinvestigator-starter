# 🎮 Game Glitch Investigator: The Impossible Guesser

## 🚨 The Situation

You asked an AI to build a simple "Number Guessing Game" using Streamlit.
It wrote the code, ran away, and now the game is unplayable. 

- You can't win.
- The hints lie to you.
- The secret number seems to have commitment issues.

## 🛠️ Setup

1. Install dependencies: `pip install -r requirements.txt` (on macOS: `python3 -m pip install -r requirements.txt`)
2. Run the app: `python -m streamlit run app.py` (on macOS: `python3 -m streamlit run app.py`)
3. Run the tests: `pytest` (or `python3 -m pytest`)

## 🕵️‍♂️ Your Mission

1. **Play the game.** Open the "Developer Debug Info" tab in the app to see the secret number. Try to win.
2. **Find the State Bug.** Why does the secret number change every time you click "Submit"? Ask ChatGPT: *"How do I keep a variable from resetting in Streamlit when I click a button?"*
3. **Fix the Logic.** The hints ("Higher/Lower") are wrong. Fix them.
4. **Refactor & Test.** - Move the logic into `logic_utils.py`.
   - Run `pytest` in your terminal.
   - Keep fixing until all tests pass!

## 📝 Document Your Experience

**Game purpose:** The game is a number-guessing game built with Streamlit. The player picks a difficulty (Easy, Normal, or Hard), which sets the number range and how many attempts they get. The game gives a Higher/Lower hint after each guess and scores the player based on how quickly they find the secret number.

**Bugs I found:**

- The hint messages were swapped: a guess that was too high told me to go higher, and a guess that was too low told me to go lower.
- On every even-numbered attempt, the secret number was converted to a string, so the comparison became a text comparison and gave wrong results (for example, 9 compared against "50").
- The New Game button never reset the game status, score, or history, so after winning or losing I stayed stuck on "Game over." It also ignored the selected difficulty and always picked a number from 1 to 100.
- The scoring was inconsistent: a "Too High" guess on an even attempt added 5 points, the win bonus used `attempt_number + 1`, and a late win could leave the final score negative (I saw a winning score of -10).
- The attempts counter started at 1 instead of 0, so I got one fewer guess than the difficulty allowed (7 instead of 8 on Normal).

**Fixes I applied:**

- Corrected the hint messages in `check_guess` and removed the string-conversion fallback, so the real secret is always compared as a number.
- Refactored `get_range_for_difficulty`, `parse_guess`, `check_guess`, and `update_score` out of `app.py` into `logic_utils.py`, and updated the import in `app.py`.
- Added a `new_game_state()` helper that resets the secret (within the difficulty's range), attempts, score, status, and history. The New Game button now uses it.
- Rewrote `update_score`: a win is worth 100 minus 10 per earlier guess (minimum 10), every wrong guess costs 5, and the score never drops below 0.
- Changed the starting value of `attempts` from 1 to 0 so the player gets the full number of allowed guesses.
- Rewrote the starter tests to unpack the `(outcome, message)` tuple that `check_guess` returns, and added tests for the hint text, New Game, and the scoring rules.

**Bugs I found but did not fix:**

- The "Attempts left" box is drawn before the guess is processed, so it lags one guess behind.
- The info box always says "between 1 and 100," even on Easy and Hard.
- `parse_guess` accepts numbers outside the difficulty range (like 0 or negatives) and silently truncates decimals such as 7.9.
- Hard (1 to 50) has a smaller range than Normal (1 to 100), which seems backwards.

I used Claude as my AI assistant for finding the causes of the bugs, refactoring, and writing tests. I checked every change by running pytest and playing the live game.

## 📸 Demo Walkthrough

Sample game on Normal difficulty (secret number: 58):

1. User enters a guess of 30
2. Game shows "📈 Go HIGHER!" (outcome: Too Low) and the score stays at 0 because it never drops below 0
3. User enters a guess of 80
4. Game shows "📉 Go LOWER!" (outcome: Too High) and the score is still 0
5. User enters a guess of 58
6. Game shows "🎉 Correct!", balloons appear, and the game ends with a final score of 80 (100 minus 10 for each of the two earlier guesses)
7. User clicks New Game: status, score, attempts, and history reset, and a new secret is picked within the difficulty's range

## 🧪 Test Results

```
Paste the real output of `python3 -m pytest` here
```

## 🚀 Stretch Features

No stretch challenges completed.
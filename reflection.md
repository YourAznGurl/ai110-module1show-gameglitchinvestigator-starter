# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

When I first ran the game, it was a Streamlit number-guessing game with a difficulty selector, a guess box, and a debug panel showing the secret number. It looked normal at first, but the hints did not match my guesses. For example, I guessed 0 when the secret was 58 and the game told me to go lower, which is impossible. I also found that New Game did not restart the game after I lost, that the game accepted guesses outside the 1 to 100 range, and that the score and attempt counter behaved strangely.

**Bug Reproduction Log**

| Input | Expected Behavior | Actual Behavior | Console Output / Error |
|-------|-------------------|-----------------|------------------------|
| Guess of 0 (secret was 58, Normal difficulty) | "Too Low" outcome with a hint to go higher | Hint said "Go LOWER!" | none |
| Lose a round, then click New Game | A fresh game starts with reset attempts and score | Still shows "Game over. Start a new game to try again." | none |
| Guess of 0 (valid range is 1 to 100) | Rejected as out of range | Accepted and counted as an attempt, and the score dropped | none |
| Final guess that ends the game | "Attempts left" shows 0 when the game is over | "Attempts left: 1" displayed next to "Out of attempts!" | none |
| Play a full Normal game with all wrong guesses | 8 guesses allowed | Game ended after 7 guesses (final score -35) | none |
| Win on the final allowed attempt | Positive score for winning | Final score of -10 | none |

---

## 2. How did you use AI as a teammate?

I used Claude as my AI assistant throughout this project. It helped me find the causes of the bugs, move the logic into `logic_utils.py`, and write pytest cases. One correct suggestion was to swap the hint messages in `check_guess` and remove the `try/except` that converted the secret to a string on even attempts. I verified it by running pytest, and by guessing 60 when the secret was 100 and seeing "Go HIGHER!" instead of the wrong hint.

One suggestion I questioned was adding a `new_game_state()` helper to fix New Game. A one-line fix (setting `status` back to "playing") would have removed the "Game over" screen, but the helper also reset the score, history, and difficulty range, and it gave me something I could test. The AI's first version of that helper also set `attempts` to 1 to match the buggy starting value, which would have kept the off-by-one bug alive. I changed it to 0 when I fixed the attempts counter, and I verified it with a test that checks `attempts == 0` and by counting that Normal now allows 8 guesses.

---

## 3. Debugging and testing your fixes

I decided a bug was fixed only when pytest and the live game agreed. The starter tests compared the whole return value to a string, but `check_guess` returns an `(outcome, message)` tuple, so I rewrote them to unpack it. I also added assertions on the hint text, because the original bug was in the message and the starter tests never looked at it, so they could not have caught swapped hints. In the end I had 9 passing tests covering the hints, New Game state, and the new scoring rules (first-guess win, minimum bonus, flat -5 penalty, no negative score).

AI helped me notice the tuple mismatch in the starter tests and suggested which cases to test for the scoring rules. I still played the app myself after each change, because pytest only tests the functions and not the button or the screen.

---

## 4. What did you learn about Streamlit and state?

Streamlit reruns the whole script from top to bottom every time you click a button or change a widget. Because of that, normal variables get reset on every rerun, which is why the secret number could seem to "change." `st.session_state` works like a notebook that survives between reruns, so the game uses it to remember the secret, the score, the attempts, and whether the game is still being played.

---

## 5. Looking ahead: your developer habits

One habit I want to reuse is writing a test for each bug right after fixing it, and making the test check the exact thing that was broken (like the hint text). Next time, I would read the AI's suggested code more carefully before accepting it, and ask it to explain why a line is there, instead of testing it afterward and finding problems later. This project made me see AI-generated code as a first draft: it can look reasonable and run without errors while still containing bugs like swapped hints and an off-by-one counter.
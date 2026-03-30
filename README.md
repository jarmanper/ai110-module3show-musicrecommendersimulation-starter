# Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.

## How The System Works

Real-world music recommenders generally fall into two camps. Collaborative filtering learns from the behavior of many users — if people who loved Song A also loved Song B, it recommends Song B to new fans of Song A without ever inspecting the songs themselves. Content-based filtering takes a different approach: it looks directly at song attributes like genre, mood, and energy, then recommends songs whose features match a specific user's preferences. Most production systems (Spotify, YouTube Music) blend both, using collaborative signals to surface surprising picks and content signals to explain or refine them.

**Features used by this system's objects:**

- `Song`: `genre`, `mood`, `energy` (core scoring features); `tempo_bpm`, `valence`, `danceability`, `acousticness` (stored, available for future scoring)
- `UserProfile`: preferred `genre`, preferred `mood`, target `energy` level

### Scoring

| Signal | Points |
|---|---|
| Genre match (song genre == user's preferred genre) | +2.0 |
| Mood match (song mood == user's preferred mood) | +1.0 |
| Energy similarity (`1.0 - abs(song.energy - user.target_energy)`) | +0.0 to +1.0 |

**Potential bias:** Because genre carries the most weight, songs that only match mood or energy will rarely surface ahead of a genre match — even a weak one.

## Sample Output

**High-Energy Pop**

![Terminal output showing recommendations for the High-Energy Pop profile](image%20copy.png)

**Chill Lofi**

![Terminal output showing recommendations for the Chill Lofi profile](image.png)

**Deep Intense Rock**

![Terminal output showing recommendations for the Deep Intense Rock profile](Screenshot%202026-03-29%20220235.png)

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Run the app:

   ```bash
   python -m src.main
   ```

### Running Tests

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this

# Model Card: Music Recommender Simulation

## 1. Model Name

**VibeFinder 1.0**

---

## 2. Intended Use

VibeFinder 1.0 predicts which songs a user will enjoy most by assigning each song a numeric score based on how well it matches the user's preferred genre, mood, and energy level. It is built for classroom exploration and is not intended for real production use. The system assumes every user can fully describe their taste with a single genre, a single mood, and one target energy value — which is a simplification of how real listening preferences work.

---

## 3. How the Model Works

The system looks at three things for each song: its genre, its mood, and its energy level (a number from 0.0 for very calm to 1.0 for very intense).

It then compares each of those to what the user said they want:

- If the song's genre matches the user's preferred genre, it earns **2 points**.
- If the song's mood matches the user's preferred mood, it earns **1 point**.
- The song also earns up to **1 point** for energy closeness. A song that exactly hits the user's target energy earns the full point; a song that is very far off earns close to zero.

All three numbers are added together to get a final score. The songs are then sorted from highest to lowest score, and the top five are returned as recommendations. Every recommendation also comes with a plain-English list of reasons explaining exactly what contributed to its score.

---

## 4. Data

The catalog contains **20 songs** stored in `data/songs.csv`. The original 10 songs were provided as a starter set and covered pop, lofi, rock, ambient, jazz, synthwave, and indie pop. Ten additional songs were added to improve diversity, introducing country, electronic, folk, metal, R&B, classical, funk, latin, and K-pop. Each song stores nine attributes: id, title, artist, genre, mood, energy, tempo, valence, danceability, and acousticness.

The dataset has real limits. Twenty songs is a tiny catalog — a real streaming service has tens of millions. The moods used (happy, chill, intense, relaxed, focused, moody) are hand-labeled and coarse. The catalog skews toward Western genres and English-language artists, which means a user who listens primarily to regional or non-Western music would get poor results. Attributes like valence, danceability, and acousticness are stored but not yet used in scoring.

---

## 5. Strengths

The system works best when the user's preferences align clearly with a specific genre. A "Chill Lofi" user gets both lofi catalog entries ranked at the top, ahead of all other genres, which matches intuition well. The scoring is fully transparent — every recommendation prints exactly why it scored the way it did, making it easy to audit and debug. For simple, single-genre listeners the top result is almost always reasonable.

---

## 6. Limitations and Bias

The biggest limitation is that genre match is worth twice as much as mood match and twice as much as the maximum energy bonus. This means genre dominates every ranking, creating a filter bubble: a user who wants "happy pop" will always see pop songs at the top, even if a jazz or indie song perfectly matches their mood and energy target. A high-energy pop song with mediocre mood alignment will consistently outrank a perfect-energy non-pop song that matches the mood exactly. The system has no concept of listening history, so it treats every session identically and cannot learn or adapt. Songs in underrepresented genres — there is only one rock song and one metal song in the catalog — have almost no chance of surfacing for users whose preferred genre is not in the catalog at all. Finally, the system cannot handle users with mixed or shifting tastes; someone who likes both lofi on weekday mornings and dance music on weekends can only be represented by one profile at a time.

---

## 7. Evaluation

Three distinct user profiles were run through the recommender to check that the scoring logic behaved as expected:

- **High-Energy Pop** (genre: pop, mood: intense, energy: 0.90) — "Gym Hero" ranked first with a score of 3.97, earning both the genre and mood bonus plus a near-perfect energy score. This matched expectations exactly.
- **Chill Lofi** (genre: lofi, mood: chill, energy: 0.38) — Both lofi tracks in the catalog landed in the top two, with the one closest in energy ranking slightly higher. Expected behavior.
- **Deep Intense Rock** (genre: rock, mood: intense, energy: 0.92) — "Storm Runner" scored 3.99 and ranked first, a clear match. However, positions two through five were all non-rock songs that happened to match the mood or energy, which revealed how thin the rock section of the catalog is.

One notable observation: for the Rock profile, the #5 result ("Sunrise City" by Neon Echo, a pop song) made it in purely on energy similarity with no genre or mood bonus. This confirms the genre-dominance bias described above — when the catalog lacks genre matches, the system falls back on weaker signals.

---

## 8. Future Work

1. **Add collaborative filtering signals.** Right now the system only looks at song attributes. Incorporating data about what other users with similar preferences listened to would let it surface unexpected but genuinely good recommendations that pure content matching would miss.
2. **Rebalance the scoring weights and use more features.** Reducing the genre bonus from 2.0 to 1.0 and adding valence and danceability to the score would reduce the filter bubble and make recommendations more sensitive to the full character of a song. This would also make the catalog's unused columns meaningful.

---

## 9. Personal Reflection

Using AI tools to scaffold the boilerplate — the CSV loading, the dataclass definitions, the CLI output loop — cut what would have been an hour of setup down to a few minutes. That said, I still had to read through the scoring function carefully to make sure the energy similarity formula was doing what I intended; the math looked right at first glance but needed a second pass to confirm the sign convention and that the result stays in a sensible range. The most surprising thing was how convincing the output feels despite how simple the algorithm is: three numbers, a sort, and a slice. It genuinely surfaces reasonable songs for each profile, which makes it easy to see why a slightly more sophisticated version of this logic could power a real product. Next time I would add collaborative filtering from the start — content-based filtering alone will always hit a ceiling because it cannot discover that two people with very different stated preferences actually enjoy the same songs.

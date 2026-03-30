# Model Card: Music Recommender Simulation

## 1. Model Name

**VibeFinder 1.0**

## 2. Intended Use

VibeFinder 1.0 predicts which songs a user will enjoy most by scoring each song based on how well it matches their preferred genre, mood, and energy level. It is built for classroom exploration and is not intended for real production use. The system assumes a user can describe their taste with a single genre, a single mood, and one target energy value — which is a simplification of how real listening preferences work.

## 3. How the Model Works

The system evaluates each song against three criteria: its genre, its mood, and its energy level (a number from 0.0 for very calm to 1.0 for very intense).

- If the song's genre matches the user's preferred genre, it earns **2 points**.
- If the song's mood matches the user's preferred mood, it earns **1 point**.
- The song also earns up to **1 point** for energy closeness. A song that exactly hits the user's target energy earns the full point; a song that is far off earns close to zero.

All three numbers are added together to get a final score. The songs are sorted from highest to lowest, and the top five are returned as recommendations. Every result also includes a plain-English breakdown of what drove the score.

## 4. Data

The catalog contains **20 songs** stored in `data/songs.csv`. The original 10 songs were provided as a starter set and covered pop, lofi, rock, ambient, jazz, synthwave, and indie pop. Ten additional songs were added to improve diversity, introducing country, electronic, folk, metal, R&B, classical, funk, latin, and K-pop. Each song stores nine attributes: id, title, artist, genre, mood, energy, tempo, valence, danceability, and acousticness.

The dataset has real limits. Twenty songs is a tiny catalog — a real streaming service has tens of millions. The mood labels (happy, chill, intense, relaxed, focused, moody) are hand-assigned and coarse. The catalog skews toward Western genres and English-language artists, which means a user who listens primarily to regional or non-Western music would get poor results. Attributes like valence, danceability, and acousticness are stored but not yet used in scoring.

## 5. Strengths

The system works best when the user's preferences align clearly with a specific genre in the catalog. A "Chill Lofi" user gets both lofi entries ranked at the top, ahead of everything else, which matches intuition well. The scoring is fully transparent — every recommendation prints exactly why it scored the way it did, making it easy to audit and debug. For a listener with a clear single-genre preference, the top result is almost always reasonable.

## 6. Limitations and Bias

The biggest limitation is that genre match is worth twice as much as mood match and twice as much as the maximum energy bonus, so genre dominates every ranking. This creates a filter bubble: a user who wants "happy pop" will always see pop songs at the top, even if a jazz or indie song perfectly matches their mood and energy. A high-energy pop song with mediocre mood alignment will consistently outrank a non-pop song that nails both mood and energy. The system has no concept of listening history, so it treats every session identically and cannot learn or adapt over time. Songs in underrepresented genres — only one rock song and one metal song appear in the catalog — have almost no chance of surfacing for users whose preferred genre is not well covered. Finally, the system cannot handle mixed or shifting tastes; someone who listens to lofi on weekday mornings and dance music on weekends can only be represented by one static profile.

## 7. Evaluation

Three distinct user profiles were run through the recommender to verify that the scoring logic behaved as expected:

- **High-Energy Pop** (genre: pop, mood: intense, energy: 0.90) — "Gym Hero" ranked first with a score of 3.97, earning both the genre and mood bonus plus a near-perfect energy score. This matched expectations.
- **Chill Lofi** (genre: lofi, mood: chill, energy: 0.38) — Both lofi tracks landed in the top two, with the one closest in energy ranking slightly higher. Expected behavior.
- **Deep Intense Rock** (genre: rock, mood: intense, energy: 0.92) — "Storm Runner" scored 3.99 and ranked first. However, positions two through five were all non-rock songs that happened to match the mood or energy, which revealed how thin the rock section of the catalog is.

One notable observation: for the Rock profile, the fifth result ("Sunrise City" by Neon Echo, a pop song) made it in purely on energy similarity with no genre or mood bonus at all. This confirms the genre-dominance issue — when the catalog lacks genre matches, the system falls back on weaker signals and the results start to feel off.

## 8. Future Work

1. **Add collaborative filtering signals.** Right now the system only looks at song attributes. Incorporating data about what other users with similar preferences listened to would let it surface unexpected but genuinely fitting recommendations that pure content matching would miss.
2. **Rebalance the scoring weights and use more features.** Reducing the genre bonus from 2.0 to 1.0 and incorporating valence and danceability into the score would reduce the filter bubble and make recommendations more sensitive to the full character of a song. This would also put the catalog's unused columns to work.

## 9. Personal Reflection

Using AI tools to scaffold the boilerplate — the CSV loading, the dataclass definitions, the CLI output loop — cut what would have been an hour of setup down to a few minutes. That said, I still had to read through the scoring function carefully to make sure the energy similarity formula was doing what I intended; the math looked right at first glance but needed a second pass to confirm the sign convention and that the result stays in a sensible range. The most surprising thing was how convincing the output feels despite how simple the algorithm is: three numbers, a sort, and a slice. It genuinely surfaces reasonable songs for each profile, which makes it easy to see why a slightly more sophisticated version of this logic could power a real product. Next time I would add collaborative filtering from the start — content-based filtering alone will always hit a ceiling because it cannot discover that two people with very different stated preferences actually enjoy the same songs.

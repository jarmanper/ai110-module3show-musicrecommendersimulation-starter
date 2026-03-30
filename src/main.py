"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

import sys
import os



from recommender import load_songs, recommend_songs

# Resolve data path relative to this file regardless of working directory
_DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "songs.csv")


PROFILES = [
    {
        "name": "High-Energy Pop",
        "prefs": {"genre": "pop", "mood": "intense", "energy": 0.90},
    },
    {
        "name": "Chill Lofi",
        "prefs": {"genre": "lofi", "mood": "chill", "energy": 0.38},
    },
    {
        "name": "Deep Intense Rock",
        "prefs": {"genre": "rock", "mood": "intense", "energy": 0.92},
    },
]


def print_separator(char: str = "-", width: int = 52) -> None:
    """Print a horizontal separator line."""
    print(char * width)


def main() -> None:
    songs = load_songs(_DATA_PATH)

    for profile in PROFILES:
        print()
        print_separator("=")
        print(f"  Listener: {profile['name']}")
        prefs = profile["prefs"]
        print(f"  Genre: {prefs['genre']}  |  Mood: {prefs['mood']}  |  Energy: {prefs['energy']:.2f}")
        print_separator("=")

        recommendations = recommend_songs(prefs, songs, k=5)

        for rank, (song, score, reasons) in enumerate(recommendations, start=1):
            print(f"\n  #{rank}  {song['title']} - {song['artist']}")
            print(f"       Score: {score:.2f}")
            for reason in reasons:
                print(f"         * {reason}")

        print()

    print_separator("-")
    print("  Done.")
    print_separator("-")


if __name__ == "__main__":
    main()

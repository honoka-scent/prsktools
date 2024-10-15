# data_loader.py

import csv


def load_songs_from_csv():
    songs = []
    with open("songs.csv", "r", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            songs.append(row)
    return songs

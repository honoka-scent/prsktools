# manual_input.py

import inquirer
from achievement_manager import update_achievement


def search_words(keyword, word_list):
    return [word for word in word_list if keyword in word]


def manual_input(songs, song_name=None, matched_songs=None):
    song_question = []
    song_names = [song["楽曲名"] for song in songs]
    if matched_songs:
        matched_words = matched_songs

    if song_name is None:
        keyword_question = [
            inquirer.Text("keyword", message="楽曲名を入力してください:"),
        ]
        keyword_answer = inquirer.prompt(keyword_question)
        keyword = keyword_answer["keyword"]

        # キーワードを使って単語リストから検索
        matched_words = search_words(keyword, song_names)

        if not matched_words:
            print("一致する単語が見つかりませんでした。")
            return

        song_question += [
            inquirer.List(
                "name", message="楽曲を選んでください", choices=matched_words
            ),
        ]

    # 見つかった単語を選択させるプロンプト
    song_question += [
        inquirer.List(
            "difficulty",
            message="難易度を選択してください",
            choices=["Expert", "Master", "Append"],
        ),
        inquirer.List(
            "status",
            message="達成度を入力してください",
            choices=["Clear", "FC", "AP"],
        ),
    ]
    song_answer = inquirer.prompt(song_question)

    song_name = song_answer["name"]
    difficulty = song_answer["difficulty"]
    status = song_answer["status"]
    song_count = len(song_names)

    update_achievement(song_name, difficulty, status, song_count, songs)


if __name__ == "__main__":
    from data_loader import load_songs_from_csv

    songs = load_songs_from_csv()
    manual_input(songs=songs)

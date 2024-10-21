import json


def get_diff_dict():
    return {
        "Expert": "X",
        "Master": "M",
        "Append": "A",
    }


def get_song_level(song_name, difficulty, songs):
    song_info = [song for song in songs if song["楽曲名"] == song_name][0]
    lv = song_info[get_diff_dict()[difficulty]]
    return lv


def get_song_count_per_level(songs):
    from collections import defaultdict

    # defaultdictを使用して初期化を簡素化
    song_count_dict = defaultdict(lambda: defaultdict(int))
    diff_dict = get_diff_dict()

    # 各曲のレベルを集計
    for k, diff_column in diff_dict.items():
        for song in songs:
            level = song[diff_column]
            if level == "-":
                continue
            song_count_dict[level][k] += 1

    # レベルを数値順にソート
    sorted_song_count_dict = dict(
        sorted(
            song_count_dict.items(),
            key=lambda x: int(x[0]) if x[0].isdigit() else float("inf"),
        )
    )

    return sorted_song_count_dict


def get_song_count_per_diff(song_info=None):
    if song_info is None:
        song_info = load_song_info()
    diff_count_dict = {
        "Expert": 0,
        "Master": 0,
        "Append": 0,
    }
    for key, value in song_info["song_count"].items():
        for k in diff_count_dict.keys():
            count = value.get(k)
            if count:
                diff_count_dict[k] += count

    return diff_count_dict


def load_song_info():
    name = "song_info.json"
    with open(name, "r") as f:
        song_info = json.load(f)
    return song_info


def save_song_info(songs):
    name = "song_info.json"
    song_info = {}
    song_info["song_count"] = get_song_count_per_level(songs)
    song_info["diff_count"] = get_song_count_per_diff(song_info)

    with open(name, "w") as f:
        json.dump(song_info, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    from data_loader import load_songs_from_csv

    songs = load_songs_from_csv()
    song_count_dict = get_song_count_per_level(songs)
    print(song_count_dict)

    diff_count_dict = get_song_count_per_diff()
    print(diff_count_dict)

    save_song_info(songs)

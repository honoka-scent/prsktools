# achievement_manager.py

import json
import os
from datetime import datetime

ACHIEVEMENTS_JSON = "achievements.json"


def load_achievements():
    if os.path.exists(ACHIEVEMENTS_JSON):
        with open(ACHIEVEMENTS_JSON, "r", encoding="utf-8") as file:
            return json.load(file)
    return {}


def save_achievements(achievements):
    with open(ACHIEVEMENTS_JSON, "w", encoding="utf-8") as file:
        json.dump(achievements, file, ensure_ascii=False, indent=4)


def update_achievement(song_name, difficulty, status, song_count, songs):
    achievements = load_achievements()
    song_info = [song for song in songs if song["楽曲名"] == song_name][0]
    diff_lv_dict = {
        "Expert": "X",
        "Master": "M",
        "Append": "A",
    }
    lv = song_info[diff_lv_dict[difficulty]]

    key = f"{song_name}"

    if "results" not in achievements:
        achievements["results"] = {}

    # 新しいキーの場合、初期値を設定
    if key not in achievements["results"]:
        achieve_dict = {
            "status": None,
            "date": None,
        }
        achievements["results"][key] = {
            "name": song_name,
            "Expert": achieve_dict.copy(),
            "Master": achieve_dict.copy(),
            "Append": achieve_dict.copy(),
            "date": datetime.now().isoformat(),
        }

    # 難易度に応じてステータスを更新
    date_now = datetime.now().isoformat()
    achievements["results"][key][difficulty]["status"] = status
    achievements["results"][key][difficulty]["date"] = date_now
    achievements["results"][key]["date"] = date_now  # 更新日時を変更

    # 集計データの更新
    achievements["total"] = calculate_total_clears(achievements["results"])
    achievements["date"] = date_now

    save_achievements(achievements)
    update_achievement_log(song_name, difficulty, lv, status, song_count)
    print(f"{song_name}（{difficulty}）の達成度を{status}に更新しました。")


def calculate_total_clears(results):
    # 各難易度のクリア数を集計
    t_dict = {"Clear": 0, "FC": 0, "AP": 0}
    total_clears = {
        "Expert": t_dict.copy(),
        "Master": t_dict.copy(),
        "Append": t_dict.copy(),
    }
    keys = ["Expert", "Master", "Append"]

    for key, value in results.items():
        for difficulty in keys:
            diff_dict = value.get(difficulty, None)
            if diff_dict is None:
                continue
            if diff_dict["status"] is not None:  # クリアされている場合のみカウント
                if diff_dict["status"] == "Clear":
                    total_clears[difficulty]["Clear"] += 1
                elif diff_dict["status"] == "FC":
                    total_clears[difficulty]["Clear"] += 1
                    total_clears[difficulty]["FC"] += 1
                elif diff_dict["status"] == "AP":
                    total_clears[difficulty]["Clear"] += 1
                    total_clears[difficulty]["FC"] += 1
                    total_clears[difficulty]["AP"] += 1
    return total_clears


def update_achievement_log(song_name, difficulty, lv, status, song_count):
    # time = datetime.now().strftime("%Y-%m-%d %H:%M")
    time = datetime.now().date().isoformat()
    # log_entry = f"{time}: {status} - {song_name}[{difficulty}]\n"
    log_entry = f"{status} - {song_name}[{difficulty.upper()[:3]}{lv}]\n"

    # 今日の達成をログに追記
    with open("achievement_log.txt", "a", encoding="utf-8") as file:
        file.write(log_entry)

    # 合計達成数を計算して更新
    achievements = load_achievements()
    log_text = ""
    for key, value in achievements["total"].items():
        temp_text = f"[{key[:3].upper()}]"
        for k, v in value.items():
            if k == "Clear":
                continue
            if v == 0:
                continue
            temp_text += "\n"
            temp_text += f"{k}: {v}/{song_count} ({v / song_count:.1%})"
        if temp_text != f"[{key[:3].upper()}]":
            log_text += temp_text + "\n"

    with open("total_achievements.txt", "w", encoding="utf-8") as file:
        file.write(log_text)

    print("ログファイルを更新しました。")

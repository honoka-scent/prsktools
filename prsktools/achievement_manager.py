# achievement_manager.py

import json
import os
from datetime import datetime, timedelta
from wcwidth import wcwidth

from config import (
    load_config,
    is_output_expert,
    is_output_master,
    is_output_append,
    is_output_fc,
    is_output_ap,
)


from song_util import (
    get_diff_dict,
    get_song_level,
    get_song_count_per_level,
    load_song_info,
)


ACHIEVEMENTS_JSON = "achievements.json"


def truncate_string_wcwidth(s, max_width=20):
    current_width = 0
    result = []
    for char in s:
        char_width = wcwidth(char)
        if char_width < 0:
            char_width = 1  # 制御文字などは1幅とみなす
        if current_width + char_width > max_width:
            break
        result.append(char)
        current_width += char_width
    return "".join(result)


def load_achievements():
    if os.path.exists(ACHIEVEMENTS_JSON):
        with open(ACHIEVEMENTS_JSON, "r", encoding="utf-8") as file:
            return json.load(file)
    return {}


def save_achievements(achievements):
    with open(ACHIEVEMENTS_JSON, "w", encoding="utf-8") as file:
        json.dump(achievements, file, ensure_ascii=False, indent=4)


def set_achievement_song_level(songs):
    achievements = load_achievements()
    for key, value in achievements["results"].items():
        for difficulty in ["Expert", "Master", "Append"]:
            lv = get_song_level(value["name"], difficulty, songs)
            achievements["results"][key][difficulty]["level"] = lv
    save_achievements(achievements)
    print("楽曲の難易度を更新しました。")


def set_achievement_level_count(songs):
    achievements = load_achievements()
    song_info = load_song_info()
    achievements["result"]


def get_today_achievements(achievements: dict):
    today = (datetime.now() - timedelta(hours=4)).date().today()
    today_dt = datetime.combine(today, datetime.min.time())
    diff_keys = get_diff_dict().keys()
    histories = {"total": {"FC": 0, "AP": 0}}
    history_dict = {
        "FC": 0,
        "AP": 0,
    }
    for key, value in achievements["results"].items():
        for diff_key in diff_keys:
            date_str = value[diff_key]["date"]
            if date_str is None or date_str == "":
                continue
            if datetime.fromisoformat(date_str) < today_dt:
                continue
            level = value[diff_key]["level"]
            if histories.get(level) is None:
                histories[level] = history_dict.copy()
            if value[diff_key]["status"] == "FC":
                histories[level]["FC"] += 1
                histories["total"]["FC"] += 1
            elif value[diff_key]["status"] == "AP":
                histories[level]["AP"] += 1
                histories["total"]["AP"] += 1

    return histories


def update_achievement(song_name, difficulty, status, song_count, songs):
    achievements = load_achievements()
    lv = get_song_level(song_name, difficulty, songs)

    key = f"{song_name}"

    if "results" not in achievements:
        achievements["results"] = {}

    # 新しいキーの場合、初期値を設定
    if key not in achievements["results"]:
        keys = ["Expert", "Master", "Append"]
        achievements["results"][key] = {
            "name": song_name,
        }
        for d in keys:
            d_l = get_song_level(song_name, d, songs)
            achieve_dict = {
                "status": None,
                "level": d_l,
                "date": None,
            }
            achievements["results"][key][d] = achieve_dict

    # 難易度に応じてステータスを更新
    date_now = datetime.now().isoformat()
    achievements["results"][key][difficulty]["status"] = status
    achievements["results"][key][difficulty]["level"] = lv
    achievements["results"][key][difficulty]["date"] = date_now
    achievements["results"][key]["date"] = date_now  # 更新日時を変更

    # 集計データの更新
    achievements["total"] = calculate_total_clears(achievements["results"], songs)
    achievements["date"] = date_now

    achievements["today"] = get_today_achievements(achievements)

    save_achievements(achievements)
    update_achievement_log(song_name, difficulty, lv, status, song_count)
    print(f"{song_name}（{difficulty}）の達成度を{status}に更新しました。")


def calculate_total_clears(results, songs):
    # 各難易度のクリア数を集計
    t_dict = {"Clear": 0, "FC": 0, "AP": 0}
    total_clears = {
        "Expert": t_dict.copy(),
        "Master": t_dict.copy(),
        "Append": t_dict.copy(),
    }
    # lv_dict =

    keys = ["Expert", "Master", "Append"]

    for key, value in results.items():
        for difficulty in keys:
            lv = get_song_level(value["name"], difficulty, songs)
            # if (lv == "-") or (lv is None):
            #     continue
            diff_dict = value.get(difficulty, None)
            if diff_dict is None:
                continue
            # if lv not in diff_dict:
            if diff_dict["status"] is not None:  # クリアされている場合のみカウント
                if diff_dict["status"] == "Clear":
                    total_clears[difficulty]["Clear"] += 1
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
    log_song_name = truncate_string_wcwidth(song_name, 20)
    # log_entry = f"{time}: {status} - {song_name}[{difficulty}]\n"
    log_entry = f"{status} - {log_song_name}[{difficulty.upper()[:3]}{lv}]\n"

    # 今日の達成をログに追記
    with open("achievement_log.txt", "a", encoding="utf-8") as file:
        file.write(log_entry)

    # 合計達成数を計算して更新
    achievements = load_achievements()
    log_text = ""

    # 今日のリザルトの確認
    log_text += "[Today]\n"
    for key, value in achievements["today"].items():
        if key == "total":
            continue
        lv = key
        log_row = f"Lv.{lv} "
        fc_text = ""
        ap_text = ""
        for k, v in value.items():
            if v == 0:
                continue
            if k == "FC":
                fc_text = f"FC: {v}"
                continue
            if k == "AP":
                ap_text = f"AP: {v}"
                continue
        if fc_text != "":
            log_row += fc_text
        if ap_text != "":
            if fc_text != "":
                log_row += ", "
            log_row += ap_text
        if fc_text != "" or ap_text != "":
            log_text += log_row + "\n"

    log_text += "\n"

    config = load_config()

    # 合計のリザルトの確認
    for key, value in achievements["total"].items():
        if key.upper() == "EXPERT" and not is_output_expert(config):
            print("skipped expert")
            continue
        if key.upper() == "MASTER" and not is_output_master(config):
            print("skipped master")
            continue
        if key.upper() == "APPEND" and not is_output_append(config):
            print("skipped append")
            continue

        temp_text = f"[{key[:3].upper()}]"
        for k, v in value.items():
            if k == "Clear":
                continue
            if k == "FC" and not is_output_fc(config):
                continue
            if k == "AP" and not is_output_ap(config):
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


if __name__ == "__main__":
    from data_loader import load_songs_from_csv

    songs = load_songs_from_csv()
    set_achievement_song_level(songs)

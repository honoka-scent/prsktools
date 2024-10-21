# ocr_input.py

import pytesseract
from PIL import Image
import re
from achievement_manager import update_achievement
from data_loader import load_songs_from_csv
from difflib import SequenceMatcher
from manual_input import manual_input

from screenshot import screenshot_from_window
from file import get_latest_file


def ocr_input_from_window(window_title, crop_box=None, show_image=False):
    screendhot = screenshot_from_window(window_title)
    ocr_input(screendhot, crop_box, show_image)


def ocr_input_from_file(image_path, crop_box=None, show_image=False):
    image = Image.open(image_path)
    ocr_input(image, crop_box=crop_box, show_image=show_image)


# cropbox: (left, upper, right, lower)
def ocr_input(image, crop_box=None, show_image=False):
    # 画像からテキストを抽出
    if crop_box:
        image = image.crop(crop_box)
    if show_image:
        image.show()

    print("テキスト認識中...")
    text = pytesseract.image_to_string(
        image, lang="jpn", config="--psm 7"
    )  # psm 7: Treat the image as a single text line.
    text = re.sub(r"\s+", "", text)
    print("認識されたテキスト:", text)

    # 楽曲データをロードして確認
    songs_list = load_songs_from_csv()

    # 楽曲名の一致率を計算し、一致率が高い順にリスト化
    similarity_threshold = 0.6
    matched_songs = []
    for song in songs_list:
        similarity = SequenceMatcher(None, text, song["楽曲名"]).ratio()
        if similarity >= similarity_threshold:
            matched_songs.append((song, similarity))

    matched_songs.sort(key=lambda x: x[1], reverse=True)

    if not matched_songs:
        print("該当する楽曲が見つかりませんでした。")

    matched_songs_name = [song[0]["楽曲名"] for song in matched_songs]
    print(matched_songs_name)

    if (len(matched_songs_name) == 1) or (len(matched_songs_name) == 0):
        song_name = matched_songs_name[0] if matched_songs_name else None
        manual_input(songs=songs_list, song_name=song_name)
    else:
        manual_input(songs=songs_list, matched_songs=matched_songs_name)


if __name__ == "__main__":
    from prsktools.config import load_config

    config = load_config()
    directory = config["image"]["directory"]
    keyword = config["image"]["keyword"]
    latest_file = get_latest_file(directory, keyword)
    print(f"Latest file: {latest_file}")
    crop_box = config["image"]["crop"]

    image_path = "./image/sample.png"
    ocr_input_from_file(latest_file, crop_box=crop_box, show_image=False)
    # window_name = "ウィンドウプロジェクター（プレビュー）"
    # ocr_input_from_window(window_name, None, True)

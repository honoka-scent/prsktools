# ocr_input.py

import pytesseract
from PIL import Image
import re
from achievement_manager import update_achievement
from data_loader import load_songs_from_csv
from difflib import SequenceMatcher
from manual_input import manual_input

from screenshot import screenshot_from_window


def ocr_input_from_window(window_title, crop_box=None, show_image=False):
    screendhot = screenshot_from_window(window_title)
    ocr_input(screendhot, crop_box, show_image)


def ocr_input_from_file(image_path, crop_box=None, show_image=False):
    image = Image.open(image_path, crop_box, show_image)
    ocr_input(image)


# cropbox: (left, upper, right, lower)
def ocr_input(image, crop_box=None, show_image=False):
    # 画像からテキストを抽出
    if crop_box:
        image = image.crop(crop_box)
    if show_image:
        image.show()

    text = pytesseract.image_to_string(image, lang="日本語")
    print("認識されたテキスト:", text)

    # 楽曲データをロードして確認
    songs_list = load_songs_from_csv()

    # 楽曲名の一致率を計算し、一致率が高い順にリスト化
    similarity_threshold = 0.6
    matched_songs = []
    for song in songs_list:
        similarity = SequenceMatcher(None, text, song["name"]).ratio()
        if similarity >= similarity_threshold:
            matched_songs.append((song, similarity))

    matched_songs.sort(key=lambda x: x[1], reverse=True)

    if not matched_songs:
        print("該当する楽曲が見つかりませんでした。")

    manual_input(
        song_names=[song[0]["name"] for song in matched_songs], songs=songs_list
    )


def main():
    image_path = "./image/sample.png"
    window_name = ""
    ocr_input_from_file(image_path)
    ocr_input_from_window(window_name, (0, 0, 200, 300))

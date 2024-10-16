import pygetwindow as gw
from PIL import ImageGrab
import win32gui


def get_window_screenshot(window_title):
    # ウィンドウを取得
    window = gw.getWindowsWithTitle(window_title)
    if not window:
        print("指定されたウィンドウが見つかりませんでした。")
        return None

    # 最初に見つかったウィンドウを使用
    window = window[0]

    # ウィンドウの位置とサイズを取得
    left, top, right, bottom = window.left, window.top, window.right, window.bottom

    # スクリーンショットを取得
    screenshot = ImageGrab.grab(bbox=(left, top, right, bottom))
    return screenshot


if __name__ == "__main__":
    # 特定のウィンドウ名を指定してスクリーンショットを取得
    window_title = input("ウィンドウを選択してください。Enterキーを押してください。")
    # window_title = "ウィンドウ名をここに入力"
    screenshot = get_window_screenshot(window_title)
    if screenshot:
        screenshot.show()  # 画像を表示
        screenshot.save("window_screenshot.png")  # 画像を保存

import glob
import os


def get_latest_file(directory, keyword):
    # 指定されたディレクトリ内で、特定のキーワードが含まれるファイルを検索
    search_pattern = os.path.join(directory, f"*{keyword}*")
    files = glob.glob(search_pattern)

    if not files:
        return None  # 該当ファイルがない場合

    # ファイルの更新時刻に基づいてソートし、最新のファイルを取得
    latest_file = max(files, key=os.path.getmtime)

    return latest_file


if __name__ == "__main__":
    # ここでメソッドを呼び出します。例えば、get_latest_fileを呼び出す場合:
    directory = "D://My Documents//Video"  # ディレクトリのパスを指定
    keyword = "Screenshot"  # 検索するキーワードを指定
    latest_file = get_latest_file(directory, keyword)
    print(f"Latest file: {latest_file}")

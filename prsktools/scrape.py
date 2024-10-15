import requests
from bs4 import BeautifulSoup
import pandas as pd


def scrape_table_to_csv(url, table_id, output_csv):
    # ウェブページを取得
    response = requests.get(url)
    if response.status_code != 200:
        print(f"ページの取得に失敗しました。ステータスコード: {response.status_code}")
        return
    response.encoding = response.apparent_encoding

    # BeautifulSoupでHTMLを解析
    soup = BeautifulSoup(response.content.decode("utf-8", "ignore"), "html.parser")

    # 指定されたIDのテーブルを探す
    table = soup.find("table", id=table_id)
    if not table:
        print(f"ID '{table_id}' のテーブルが見つかりませんでした。")
        return

    # テーブルヘッダーの取得
    headers = []
    header_row = table.find("thead")
    if header_row:
        for th in header_row.find_all("th"):
            headers.append(th.get_text(strip=True))
    else:
        # theadがない場合、最初のtrからヘッダーを取得
        first_row = table.find("tr")
        if first_row:
            for th in first_row.find_all(["th", "td"]):
                headers.append(th.get_text(strip=True))

    # テーブルの行データの取得
    rows = []
    # tbodyがある場合、tbody内のtrを取得
    tbody = table.find("tbody")
    if tbody:
        tr_elements = tbody.find_all("tr")
    else:
        # tbodyがない場合、全てのtrを取得
        tr_elements = table.find_all("tr")
        # ヘッダー行をスキップ
        if table.find("thead") is None and tr_elements:
            tr_elements = tr_elements[1:]

    for tr in tr_elements:
        cells = tr.find_all(["td", "th"])
        row = [cell.get_text(strip=True) for cell in cells]
        # 行の長さがヘッダーと一致しない場合、調整
        if len(row) != len(headers):
            # 空のセルを追加または不要なセルを削除
            if len(row) < len(headers):
                row += [""] * (len(headers) - len(row))
            else:
                row = row[: len(headers)]
        rows.append(row)

    # pandas DataFrameに変換
    df = pd.DataFrame(rows, columns=headers)

    # CSVファイルに保存
    df.to_csv(output_csv, index=False, encoding="utf-8_sig")
    print(f"テーブルデータが '{output_csv}' に保存されました。")


if __name__ == "__main__":
    # 取得するURL、テーブルID、出力CSVファイル名を指定
    url = "https://pjsekai.com/?aad6ee23b0#table"
    table_id = "sortable_table1"
    output_csv = "songs.csv"

    scrape_table_to_csv(url, table_id, output_csv)

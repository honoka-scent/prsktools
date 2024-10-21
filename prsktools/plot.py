import matplotlib.pyplot as plt
import japanize_matplotlib  # <- これ

import matplotlib.pyplot as plt

# サンプルデータ
labels = ["カテゴリA", "カテゴリB", "カテゴリC", "カテゴリD"]
sizes = [40, 30, 20, 10]  # 各カテゴリの数値
colors = ["#ff9999", "#66b3ff", "#99ff99", "#ffcc99"]  # セクションの色


# パーセンテージと実際の数値を表示する関数
def autopct_format(pct, allvals):
    absolute = int(round(pct / 100.0 * sum(allvals)))
    return f"{pct:.1f}%\n({absolute})"


# グラフの作成
fig, ax = plt.subplots(figsize=(8, 8))  # 図のサイズを指定

# 円グラフの描画
wedges, texts, autotexts = ax.pie(
    sizes,
    labels=labels,  # カテゴリ名をラベルとして使用
    autopct=lambda pct: autopct_format(pct, sizes),  # パーセンテージと数値を表示
    startangle=90,  # グラフの開始角度
    colors=colors,  # セクションの色
    textprops=dict(color="white", fontsize=12),  # パーセンテージ表示の文字色とサイズ
    # wedgeprops=dict(width=0.5, edgecolor="w"),  # セクションの幅とエッジ色
)

# グラフの等しい比率を保持して円を描画
ax.axis("equal")

# 凡例の追加
plt.legend(
    wedges,
    labels,
    title="カテゴリ",
    loc="center left",
    bbox_to_anchor=(1, 0, 0.5, 1),
    fontsize=12,
)

# タイトルの追加
plt.title("カテゴリ別の割合と数値", fontsize=16)

# 画像として保存
plt.savefig("pie_chart_with_categories.png", dpi=300, bbox_inches="tight")

# グラフを表示
plt.show()

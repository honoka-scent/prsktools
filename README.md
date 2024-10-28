# ビターチョコレート

甘い

## motivate

プロセカの音ゲー部分のモチベ維持のため。それと手の休憩

## for me

・あくまで手の休憩のついでに作るだけなので1つの機能は小さく作る

・フロントはnext.jsとMUIで他はpython

・達成状況はachievements.jsonに保存。DBはgithubで履歴が見れないので却下。CSVでも良かったかも

・曲が追加されたらscrape.pyで更新する

・manual_input.pyで曲名を入力して更新

・ocr_input.pyで指定したディレクトリにあるリザルト画像から文字を読み取って更新する

・ocrで楽曲情報を取得する場合はtesseractを入れた後に日本語の学習データを入れる

・Clear/FC/APの3種のステータスがあるけどClearは基本使わない

・曲の難易度が追加されたらscrape.pyでレベルを取得してachievement_manager.pyでachievements.jsonのレベルを更新する

・OBS表示用はtotal_achievements.txtとachievement_log.txtの2つ。後者はチャットモードで使う

・inquirerはipynb上で動かない

・achievements.jsonはwebページに反映させるときは親ディレクトリからpublicに上書きコピーする

・gh-pagesのブランチがGithub Pagesになる

・github Pagesを使いたい場合はリポジトリを公開にする必要がある。恥ずかしい

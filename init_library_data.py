"""
蔵書関連テーブル(zosho, name, author, publisher, textsource)の
作成 + テストデータ投入を行う、初回セットアップ用スクリプト。

アプリ起動時(login画面表示時など)には絶対に呼ばないこと。
セットアップ時、またはテストデータを最初からやり直したい時に
手動で1回だけ実行する。

使い方:
    python init_library_data.py
"""
import main
import tsuika

print("テーブルを作成します（既存データは削除されます）...")
main.maketable()
print("テーブルを作成しました。")

print("テストデータを投入します...")
tsuika.pre_tsuika()
print("テストデータを投入しました。")

"""
DB初期化用スクリプト。
アプリ起動時(gunicornのワーカー起動時など)には絶対に実行しないこと。
セットアップ時、またはDBをリセットしたい時に手動で1回だけ実行する。

使い方:
    python init_db.py          # 既存のadminがいなければ作成(安全)
    python init_db.py --reset  # 全テーブルを削除して作り直す(データ全消去、要注意)
"""
import sys
from werkzeug.security import generate_password_hash

# flaskmain.py 側で定義している app, db, User をインポートする
# (flaskmain.py 側は import 時に db.drop_all() 等が動かないよう、
#  上記の with app.app_context(): ブロックを削除済みであること)
from flaskmain import app, db, User

RESET = "--reset" in sys.argv

with app.app_context():
    if RESET:
        confirm = input("本当に全テーブルを削除して作り直しますか？既存データは全て消えます。[y/N]: ")
        if confirm.lower() != "y":
            print("中止しました。")
            sys.exit(0)
        db.drop_all()
        db.create_all()
        print("テーブルを削除・再作成しました。")
    else:
        db.create_all()  # 無ければ作成、あれば何もしない

    existing = User.query.filter_by(username="admin").first()
    if existing:
        print("adminユーザーは既に存在します。スキップしました。")
    else:
        admin = User(
            username="admin",
            password_hash=generate_password_hash("adminpass"),
            role="admin",
        )
        db.session.add(admin)
        db.session.commit()
        print("adminユーザーを作成しました。")

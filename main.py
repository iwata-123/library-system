"""
開発者モード
    貸出する本の追加
    貸出する本の削除
    禁書への登録
    本の情報の更新
貸出
    その本のステータスを貸出状態にする
返却
    その本のステータスを返却状態にする
予約
    その本が返却されたら通知する
検索
    その本の情報が見れる

テーブルは？どう設計する？
タイトル,著者名,isbn,出版社,貸し出しステータス,禁書ステータス,id
"""
import sqlite3
import numpy as np





# -------------------------------------------------
# メソッド名：maketable
# 引数　：なし
# 返却値：なし
# 処理の説明
# zosho,name,author,publisher,textsourceテーブルを作る処理
# -------------------------------------------------
def maketable():
    with sqlite3.connect('lib_sys.db') as conn:
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute('''
                    DROP TABLE IF EXISTS zosho
                    ''')
        conn.commit()

        cur.execute('''
                    DROP TABLE IF EXISTS name
                    ''')
        conn.commit()
        cur.execute('''
                    DROP TABLE IF EXISTS author
                    ''')
        conn.commit()
        cur.execute('''
                    DROP TABLE IF EXISTS publisher
                    ''')
        conn.commit()
        cur.execute('''
                    DROP TABLE IF EXISTS textsource
                    ''')
        conn.commit()
        conn.execute("PRAGMA foreign_keys = ON")
        conn.commit()
        cur.execute("""
                    CREATE TABLE IF NOT EXISTS zosho (
                    id INTEGER,
                    name_id INTEGER,
                    author_id INTEGER,
                    publisher_id INTEGER,
                    textsource_id INTEGER,
                    isbn TEXT NOT NULL,
                    kashidashi INTEGER,
                    kinsho INTEGER,
                    yoyaku INTEGER,
                    PRIMARY KEY (id,isbn),
                    FOREIGN KEY (author_id) REFERENCES author(id),
                    FOREIGN KEY (name_id) REFERENCES name(id),
                    FOREIGN KEY (publisher_id) REFERENCES publisher(id)
                    FOREIGN KEY (textsource_id) REFERENCES publisher(id)
                    )
                    """)
        conn.commit()
        cur.execute("""
                    CREATE TABLE IF NOT EXISTS name (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL)
                    """)
        conn.commit()
        cur.execute("""
                    CREATE TABLE IF NOT EXISTS author (
                    id INTEGER PRIMARY KEY,
                    author TEXT NOT NULL)
                    """)
        conn.commit()
        cur.execute("""
                    CREATE TABLE IF NOT EXISTS publisher (
                    id INTEGER PRIMARY KEY,
                    publisher TEXT NOT NULL)
                    """)
        cur.execute("""
                    CREATE TABLE IF NOT EXISTS textsource (
                    id INTEGER PRIMARY KEY,
                    textsource TEXT NOT NULL)
                    """)
        conn.commit()


# -------------------------------------------------
# メソッド名：d_koushin
# 引数　：id,name,author,publisher,isbn,kashidashi,kinsho,yoyak
# 返却値：なし
# 処理の説明
# zoshoテーブルでid（主キーのid）,name_id（nameテーブルとリレーションが貼ってある）,
# author_id（authorテーブルとリレーションが貼ってある）,
# publisher_id（publisherテーブルとリレーションが貼ってある）,
# isbn（書籍に割り振られた国際規格の番号）,kashidashi（貸し出しているかのフラグ）,
# kinsho（禁書登録になってるかのフラグ）,yoyaku（予約済みかのフラグ）
# nameテーブル、id（zoshoテーブルとリレーションが貼ってある）,name（本の名前）
# authorテーブル、id（zoshoテーブルとリレーションが貼ってある）,author（著者名）
# publisherテーブルからid（zoshoテーブルとリレーションが貼ってある）,publisher（出版社名）
# を更新
# -------------------------------------------------
def d_koushin(id,name,author,publisher,isbn,kashidashi,kinsho,yoyaku,textsource):
    with sqlite3.connect('lib_sys.db') as conn:
        cur = conn.cursor()
        cur.execute(
                    """
                    UPDATE zosho SET id = ?,name_id = ?,author_id = ?,publisher_id = ?,isbn = ?,kashidashi = ?,kinsho = ?,yoyaku = ? WHERE id = ?
                    """,
                    (f"{id}",f"{id}",f"{id}",f"{id}",f"{isbn}",f"{kashidashi}",f"{kinsho}",f"{yoyaku}",f"{id}")
                    )
        conn.commit()
        cur.execute(
                    """
                    UPDATE name SET id = ?,name = ? WHERE id = ?
                    """,
                    (f"{id}",f"{name}",f"{id}")
                    )
        conn.commit()
        cur.execute(
                    """
                    UPDATE author SET id = ?,author = ? WHERE id = ?
                    """,
                    (f"{id}",f"{author}",f"{id}")
                    )
        conn.commit()
        cur.execute(
                    """
                    UPDATE publisher SET id = ?,publisher = ? WHERE id = ?
                    """,
                    (f"{id}",f"{publisher}",f"{id}")
                    )
        conn.commit()
        cur.execute(
                    """
                    UPDATE textsource SET id = ?,textsource = ? WHERE id = ?
                    """,
                    (f"{id}",f"{textsource}",f"{id}")
                    )
        conn.commit()


#書籍の追加用
def d_tsuika(name,author,publisher,isbn,textsource):
    with sqlite3.connect('lib_sys.db') as conn:
        cur = conn.cursor()
        #同じ本がないかチェック
        flg = 0
        cur.execute(
                    """
                    SELECT isbn 
                    FROM zosho
                    WHERE isbn = ? 
                    """,
                    (f"{isbn}",)
                    )
        conn.commit()
        rows = cur.fetchall()
        if rows:
            # データがあったらflgは1
            flg = 1
            return flg
        #データを挿入
        cur.execute(
                    """INSERT INTO zosho 
                    (isbn,kashidashi,kinsho,yoyaku) 
                    VALUES (?,?,?,?)
                    """,
                    (f"{isbn}",0,0,0)
                    )
        conn.commit()
        #idを取得
        rowid = cur.lastrowid
        cur.execute(
                    """
                    UPDATE zosho 
                    SET id = ?,name_id = ?,author_id = ?,publisher_id = ?
                    WHERE isbn = ?
                    """,
                    (f"{rowid}",f"{rowid}",f"{rowid}",f"{rowid}",f"{isbn}",)
                    )
        conn.commit()

        cur.execute(
                        """INSERT INTO name 
                        (name) 
                        VALUES (?)
                        """,
                        (f"{name}",)
                        )
        conn.commit()
        cur.execute(
                        """INSERT INTO author
                        (author) 
                        VALUES (?)
                        """,
                        (f"{author}",)
                        )
        conn.commit()
        cur.execute(
                        """INSERT INTO publisher
                        (publisher) 
                        VALUES (?)
                        """,
                        (f"{publisher}",)
                        )

        conn.commit()
        cur.execute(
                        """INSERT INTO textsource
                        (textsource) 
                        VALUES (?)
                        """,
                        (f"{textsource}",)
                        )

        conn.commit()
        flg = 0
        return flg 
    

# -------------------------------------------------
# メソッド名：d_sakuzyo
# 引数　：isbn　（書籍に割り振られた国際規格の番号）
# 返却値：  1 （蔵書にあるかないかのフラグ、呼び出し先でflg==0を上書きする）
# 処理の説明
# zoshoテーブル , nameテーブル , authorテーブル , publisherテーブルから
# 対象の書籍データの削除処理を行う。
# -------------------------------------------------
def d_sakuzyo(isbn):
    with sqlite3.connect('lib_sys.db') as conn:
        cur = conn.cursor()

        cur.execute(
                        """
                        SELECT id
                        FROM zosho
                        WHERE isbn = ?
                        """,
                        (f"{isbn}",)
                        )
        conn.commit()
        rows = cur.fetchall()
        if rows != []:
            id = rows[0]
            id = id[0]
        else:
            return 0
        cur.execute(
                        """
                        DELETE FROM zosho WHERE id = ?
                        """,
                        (f"{id}",)
                        )
        conn.commit()
        cur.execute(
                        """
                        DELETE FROM name WHERE id = ?
                        """,
                        (f"{id}",)
                        )
        conn.commit()
        cur.execute(
                        """
                        DELETE FROM author WHERE id = ?
                        """,
                        (f"{id}",)
                        )
        conn.commit()
        cur.execute(
                        """
                        DELETE FROM publisher WHERE id = ?
                        """,
                        (f"{id}",)
                        )
        conn.commit()
        cur.execute(
                        """
                        DELETE FROM textsource WHERE id = ?
                        """,
                        (f"{id}",)
                        )
        conn.commit()
        return 1

# -------------------------------------------------
# メソッド名：d_kinsho
# 引数　：isbn（書籍に割り振られた国際規格の番号）
# 返却値：なし
# 処理の説明
# isbnで蔵書検索をかけて検索をかけた書籍に対して禁書登録をする
# -------------------------------------------------
def d_kinsho(isbn):
    with sqlite3.connect('lib_sys.db') as conn:
        cur = conn.cursor()
        cur.execute(
                        """
                        UPDATE zosho SET kinsho = 1 WHERE isbn = ?
                        """,
                        (f"{isbn}",)
                        )
        conn.commit()

# -------------------------------------------------
# メソッド名：d_kinsho_kaizyo
# 引数　：isbn（書籍に割り振られた国際規格の番号）
# 返却値：なし
# 処理の説明
# isbnで蔵書検索をかけて検索をかけた書籍に対して禁書登録解除をする
# -------------------------------------------------
def d_kinsho_kaizyo(isbn):
    with sqlite3.connect('lib_sys.db') as conn:
        cur = conn.cursor()
        cur.execute(
                        """
                        UPDATE zosho SET kinsho = 0 WHERE isbn = ?
                        """,
                        (f"{isbn}",)
                        )
        conn.commit()



# テスト用　テーブルの中身をコンソールに表示する用だったもの
def hyozi():
    with sqlite3.connect('lib_sys.db') as conn:
        cur = conn.cursor()
        cur.execute(
                        """
                        SELECT *
                        FROM zosho
                        """
                        )
        conn.commit()
        rows1 = cur.fetchall()

        cur.execute(
                        """
                        SELECT *
                        FROM name
                        """
                        )
        conn.commit()
        rows2 = cur.fetchall()
        cur.execute(
                        """
                        SELECT *
                        FROM author
                        """
                        )
        conn.commit()
        rows3 = cur.fetchall()
        cur.execute(
                        """
                        SELECT *
                        FROM publisher
                        """
                        )
        conn.commit()
        rows4 = cur.fetchall()

    return rows1,rows2,rows3,rows4

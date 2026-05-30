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
        conn.execute("PRAGMA foreign_keys = ON")
        conn.commit()
        cur.execute("""
                    CREATE TABLE IF NOT EXISTS zosho (
                    id INTEGER,
                    name_id INTEGER,
                    author_id INTEGER,
                    publisher_id INTEGER,  
                    isbn TEXT NOT NULL,
                    kashidashi INTEGER,
                    kinsho INTEGER,
                    yoyaku INTEGER,
                    PRIMARY KEY (id,isbn),
                    FOREIGN KEY (author_id) REFERENCES author(id),
                    FOREIGN KEY (name_id) REFERENCES name(id),
                    FOREIGN KEY (publisher_id) REFERENCES publisher(id)
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
        conn.commit()


#ai使用
def search_5(id=None, name=None, author=None, publisher=None, isbn=None):
    s_id = None
    s_isbn = None
    s_kashidashi = None
    s_yoyaku = None
    s_name = None
    s_author = None
    s_publisher = None

    conditions1 = []
    conditions2 = []
    conditions3 = []
    conditions4 = []

    values1 = []
    values2 = []
    values3 = []
    values4 = []

    with sqlite3.connect('lib_sys.db') as conn:
        cur = conn.cursor()
        
        if id:
            conditions1.append("id = ?")
            conditions2.append("id = ?")
            conditions3.append("id = ?")
            conditions4.append("id = ?")
            values1.append(id)
            values2.append(id)
            values3.append(id)
            values4.append(id)

        if name:
            conditions2.append("name = ?")
            values2.append(name)

        if author:
            conditions3.append("author = ?")
            values3.append(author)

        if isbn:
            conditions1.append("isbn = ?")
            values1.append(isbn)

        if publisher:
            conditions4.append("publisher = ?")
            values4.append(publisher)


        query1 = "SELECT * FROM zosho"
        query2 = "SELECT * FROM name"
        query3 = "SELECT * FROM author"
        query4 = "SELECT * FROM publisher"


#機能する？
        if conditions1 != []:
            # 
            query1 += " WHERE " + " AND ".join(conditions1)
        

        if conditions2 != []:
            #
            query2 += " WHERE " + " AND ".join(conditions2)

        if conditions3 != []:
            #
            query3 += " WHERE " + " AND".join(conditions3)


        if conditions4 != []:
            #
            query4 += " WHERE " + " AND".join(conditions4)

#機能する？id=?があるから絶対true
        if len(query1) > 19:
            print("実行1")
            cur.execute(query1, values1)
            conn.commit()
            rows = cur.fetchall()
            #unsupported operand type(s) for %: 'builtin_function_or_method' and 'int'
            # タプル (tuple) に対して % 演算子を使おうとしたときに出ます。
            s_id = [row[0] for row in rows]
            print(s_id)
            # s_isbn = [row[1] for row in rows]
            # s_kashidashi = [row[2] for row in rows]
            # s_yoyaku = [row[4] for row in rows]
            for row_id in s_id:
                cur.execute("""
                            SELECT name.name,author.author,publisher.publisher,zosho.isbn,zosho.kashidashi,zosho.yoyaku
                            FROM zosho
                            JOIN name 
                            ON zosho.name_id = name.id
                            JOIN author
                            ON zosho.author_id = author.id
                            JOIN publisher
                            ON zosho.publisher_id = publisher.id
                            WHERE zosho.id = ? AND kinsho != 1
                            """,(f"{row_id}",)
                            )
                conn.commit()
                rows = cur.fetchall()
                if rows != []:
                    return rows


        if len(query2) > 18:
            cur.execute(query2, values2)
            conn.commit()
            rows= cur.fetchall()
            s_id = [row[0] for row in rows]
            # s_name = [row[1] for row in rows]
            for row_id in s_id:
                cur.execute("""
                            SELECT name.name,author.author,publisher.publisher,zosho.isbn,zosho.kashidashi,zosho.yoyaku
                            FROM zosho
                            JOIN name 
                            ON zosho.name_id = name.id
                            JOIN author
                            ON zosho.author_id = author.id
                            JOIN publisher
                            ON zosho.publisher_id = publisher.id
                            WHERE name.id = ? AND kinsho != 1
                            """,(f"{row_id}")
                            )
                conn.commit()
                rows = cur.fetchall()
                print(rows)
                if rows != []:
                    return rows
                print(rows)


        if len(query3) > 20:
            cur.execute(query3, values3)
            conn.commit()
            rows= cur.fetchall()
            s_id = [row[0] for row in rows]
            # s_author = [row[1] for row in rows]
            for row_id in s_id:
                cur.execute("""
                            SELECT name.name,author.author,publisher.publisher,zosho.isbn,zosho.kashidashi,zosho.yoyaku
                            FROM zosho
                            JOIN name 
                            ON zosho.name_id = name.id
                            JOIN author
                            ON zosho.author_id = author.id
                            JOIN publisher
                            ON zosho.publisher_id = publisher.id
                            WHERE author.id = ? AND kinsho != 1
                            """,(f"{row_id}")
                            )
                conn.commit()
                rows = cur.fetchall()
                print(rows)
                if rows != []:
                    return rows
                print(rows)


        if len(query4) > 23:
            cur.execute(query4, values4)
            conn.commit()
            rows= cur.fetchall()
            s_id = [row[0] for row in rows]
            for row_id in s_id:
                cur.execute("""
                            SELECT name.name,author.author,publisher.publisher,zosho.isbn,zosho.kashidashi,zosho.yoyaku
                            FROM zosho
                            JOIN name 
                            ON zosho.name_id = name.id
                            JOIN author
                            ON zosho.author_id = author.id
                            JOIN publisher
                            ON zosho.publisher_id = publisher.id
                            WHERE publisher.id = ? AND kinsho != 1
                            """,(f"{row_id}")
                            )
                conn.commit()
                rows = cur.fetchall()
                print(rows)
                if rows != []:
                    return rows
                print(rows)





#ai使用
def search_8(id=None,name=None,author=None,publisher=None,isbn=None,kashidashi=None,kinsho=None,yoyaku=None):
    s_id = None

    conditions1 = []
    conditions2 = []
    conditions3 = []
    conditions4 = []

    values1 = []
    values2 = []
    values3 = []
    values4 = []
    with sqlite3.connect('lib_sys.db') as conn:
        cur = conn.cursor()

        if id:
            conditions1.append("id = ?")
            conditions2.append("id = ?")
            conditions3.append("id = ?")
            conditions4.append("id = ?")
            values1.append(id)
            values2.append(id)
            values3.append(id)
            values4.append(id)

        if name:
            conditions2.append("name = ?")
            values2.append(name)

        if author:
            conditions3.append("author = ?")
            values3.append(author)

        if publisher:
            conditions4.append("publisher = ?")
            values4.append(publisher)

        if isbn:
            conditions1.append("isbn = ?")
            values1.append(isbn)

        if kashidashi:
            conditions1.append("kashidashi = ?")
            values1.append(kashidashi)

        if kinsho:
            conditions1.append("kinsho = ?")
            values1.append(kinsho)

        if yoyaku:
            conditions1.append("yoyaku = ?")
            values1.append(yoyaku)

        query1 = "SELECT * FROM zosho"
        query2 = "SELECT * FROM name"
        query3 = "SELECT * FROM author"
        query4 = "SELECT * FROM publisher"

        if conditions1 != []:
            # 
            query1 += " WHERE " + " AND ".join(conditions1)
            print("今は" + query1)
        

        if conditions2 != []:
            #
            query2 += " WHERE " + " AND ".join(conditions2)
            print("今は" + query2)

        if conditions3 != []:
            #
            print(conditions3)
            query3 += " WHERE " + " AND".join(conditions3)
            print("今は" + query3)


        if conditions4 != []:
            #
            query4 += " WHERE " + " AND".join(conditions4)
            print("今は" + query4)

        if len(query1) > 19:
            print("今実行１")
            cur.execute(query1, values1)
            conn.commit()
            rows = cur.fetchall()
            #unsupported operand type(s) for %: 'builtin_function_or_method' and 'int'
            # タプル (tuple) に対して % 演算子を使おうとしたときに出ます。
            s_id = [row[0] for row in rows]
            print(s_id)
            for row_id in s_id:
                cur.execute("""
                            PRAGMA table_info(zosho)
                            """
                            )
                conn.commit()
                rows = cur.fetchall()
                for row in rows:
                    print(row)
                cur.execute("""
                            SELECT name.name,author.author,publisher.publisher,zosho.isbn,zosho.kashidashi,zosho.kinsho,zosho.yoyaku
                            FROM zosho
                            JOIN name 
                            ON zosho.name_id = name.id
                            JOIN author
                            ON zosho.author_id = author.id
                            JOIN publisher
                            ON zosho.publisher_id = publisher.id
                            WHERE zosho.id = ? AND kinsho != 1
                            """,(f"{row_id}",)
                            )
                conn.commit()
                rows = cur.fetchall()
                print(rows)
                if rows != []:
                    return rows
                print(rows)

        if len(query2) > 18:
            print("今実行２")
            cur.execute(query2, values2)
            conn.commit()
            rows= cur.fetchall()
            s_id = [row[0] for row in rows] 
            for row_id in s_id:
                cur.execute("""
                            PRAGMA table_info(name)
                            """
                            )
                conn.commit()
                rows = cur.fetchall()
                for row in rows:
                    print(row)
                cur.execute("""
                            SELECT name.name,author.author,publisher.publisher,zosho.isbn,zosho.kashidashi,zosho.kinsho,zosho.yoyaku
                            FROM zosho
                            JOIN name 
                            ON zosho.name_id = name.id
                            JOIN author
                            ON zosho.author_id = author.id
                            JOIN publisher
                            ON zosho.publisher_id = publisher.id
                            WHERE name.id = ? AND kinsho != 1
                            """,(f"{row_id}")
                            )
                conn.commit()
                rows = cur.fetchall()
                print(rows)
                if rows != []:
                    return rows
                print(rows)


        if len(query3) > 20:
            print("今実行３")
            cur.execute(query3, values3)
            conn.commit()
            rows= cur.fetchall()
            s_id = [row[0] for row in rows]
            for row_id in s_id:
                cur.execute("""
                            PRAGMA table_info(author)
                            """
                            )
                conn.commit()
                rows = cur.fetchall()
                for row in rows:
                    print(row)
                cur.execute("""
                            SELECT name.name,author.author,publisher.publisher,zosho.isbn,zosho.kashidashi,zosho.kinsho,zosho.yoyaku
                            FROM zosho
                            JOIN name 
                            ON zosho.name_id = name.id
                            JOIN author
                            ON zosho.author_id = author.id
                            JOIN publisher
                            ON zosho.publisher_id = publisher.id
                            WHERE author.id = ? AND kinsho != 1
                            """,(f"{row_id}")
                            )
                conn.commit()
                rows = cur.fetchall()
                print(rows)
                if rows != []:
                    return rows
                print(rows)


        if len(query4) > 23:
            print("今実行４")
            cur.execute(query4, values4)
            conn.commit()
            rows= cur.fetchall()
            s_id = [row[0] for row in rows]
            for row_id in s_id:
                cur.execute("""
                            PRAGMA table_info(publisher)
                            """
                            )
                conn.commit()
                rows = cur.fetchall()
                for row in rows:
                    print(row)
                cur.execute("""
                            SELECT name.name,author.author,publisher.publisher,zosho.isbn,zosho.kashidashi,zosho.kinsho,zosho.yoyaku
                            FROM zosho
                            JOIN name 
                            ON zosho.name_id = name.id
                            JOIN author
                            ON zosho.author_id = author.id
                            JOIN publisher
                            ON zosho.publisher_id = publisher.id
                            WHERE publisher.id = ? AND kinsho != 1
                            """,(f"{row_id}")
                            )
                conn.commit()
                rows = cur.fetchall()
                print(rows)
                if rows != []:
                    return rows
                print(rows)

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
        print(rows1)

        cur.execute(
                        """
                        SELECT *
                        FROM name
                        """
                        )
        conn.commit()
        rows2 = cur.fetchall()
        print(rows2)
        cur.execute(
                        """
                        SELECT *
                        FROM author
                        """
                        )
        conn.commit()
        rows3 = cur.fetchall()
        print(rows3)

        cur.execute(
                        """
                        SELECT *
                        FROM publisher
                        """
                        )
        conn.commit()
        rows4 = cur.fetchall()
        print(rows4)

    return rows1,rows2,rows3,rows4


def pre_tsuika():
    tuika_list_zosho = [
                        (1,1,1,1,"978-9-87-654321-0",0,0,0),
                        (2,2,2,2,"979-8-12-908374-5",0,0,0),
                        (3,3,3,3,"978-1-99-443210-7",0,0,0),
                        (4,4,4,4,"979-0-44-771982-3",0,0,0),
                        (5,5,5,5,"978-3-61-559004-9",0,0,0),
                        (6,6,6,6,"979-5-73-280156-2",0,0,0),
                        (7,7,7,7,"978-8-02-199873-4",0,0,0),
                        (8,8,8,8,"979-2-66-401990-6",0,0,0),
                        (9,9,9,9,"978-6-14-770045-1",0,0,0),
                        (10,10,10,10,"979-4-88-932611-8",0,0,0)
                        ]

    tuika_list_name = [(1,"霧の街と七つの歯車"),
                       (2,"量子砂漠の歩き方"),
                       (3,"月面郵便局勤務日誌"),
                       (4,"思考する機械と沈黙する人間"),
                       (5,"雨音保存協会"),
                       (6,"非連続な午後"),
                       (7,"海底都市アグラファ"),
                       (8,"コンパイラは夢を見ない"),
                       (9,"忘却回路設計論"),
                       (10,"風向きが反転する丘")
                       ]
    
    tuika_list_author = [(1,"朝凪 恒一"),
                         (2,"日影 ミナト"),
                         (3,"白峰 アオ"),
                         (4,"早川 リク"),
                         (5,"小鳥遊 セツ"),
                         (6,"神崎 トオル"),
                         (7,"深海 ソウ"),
                         (8,"井波 ケイ"),
                         (9,"真白 ユウ"),
                         (10,"霧島 ナナ")]
    
    tuika_list_publisher = [(1,"星環書房"),
                            (2,"未来層出版"),
                            (3,"ルナ・プレス"),
                            (4,"構造舎"),
                            (5,"水脈文庫"),
                            (6,"パララックス出版"),
                            (7,"ネレイド社"),
                            (8,"ビット樹林社"),
                            (9,"ノードブックス"),
                            (10,"境界線出版")
                            ]

    with sqlite3.connect('lib_sys.db') as conn:
        cur = conn.cursor()
        cur.executemany(
                    """INSERT INTO zosho
                    (id,name_id,author_id,publisher_id,isbn,kashidashi,kinsho,yoyaku) 
                    VALUES (?,?,?,?,?,?,?,?)
                    """,
                    tuika_list_zosho
                    )
        cur.executemany(
                    """INSERT INTO name
                    (id,name) 
                    VALUES (?,?)
                    """,
                    tuika_list_name
                    )

        cur.executemany(
                    """INSERT INTO author
                    (id,author) 
                    VALUES (?,?)
                    """,
                    tuika_list_author
                    )
        cur.executemany(
                    """INSERT INTO publisher
                    (id,publisher) 
                    VALUES (?,?)
                    """,
                    tuika_list_publisher
                    )

        conn.commit()

def d_koushin(id,name,author,publisher,isbn,kashidashi,kinsho,yoyaku):
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


def d_tsuika(name,author,publisher,isbn):
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
        print(rowid)
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
        flg = 0
        return flg 


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
        print(rows)
        if rows != []:
            id = rows[0]
            id = id[0]
            print("\n")
            print(id)
            print("\n")
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
        return 1


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



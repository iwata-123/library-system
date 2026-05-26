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
from sudachipy import tokenizer
from sudachipy import dictionary


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

def huwatto(content=None):

    tokenizer_obj = dictionary.Dictionary().create()
    # 複数粒度分割
    mode = tokenizer.Tokenizer.SplitMode.A
    [m.surface() for m in tokenizer_obj.tokenize(content, mode)]
    return 



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

#まだ
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

#○
def pre_tsuika():
    books = [
        (1, 1, 1, 1, 1, "9784000000001", 0, 0, 0),
        (2, 2, 2, 2, 2, "9784000000002", 0, 0, 0),
        (3, 3, 3, 3, 3, "9784000000003", 0, 0, 0),
        (4, 4, 4, 4, 4, "9784000000004", 0, 0, 0),
        (5, 5, 5, 5, 5, "9784000000005", 0, 0, 0),
        (6, 6, 6, 6, 6, "9784000000006", 0, 0, 0),
        (7, 7, 7, 7, 7, "9784000000007", 0, 0, 0),
        (8, 8, 8, 8, 8, "9784000000008", 0, 0, 0),
        (9, 9, 9, 9, 9, "9784000000009", 0, 0, 0),
        (10, 10, 10, 10, 10, "9784000000010", 0, 0, 0),
        (11, 11, 11, 11, 11, "9784000000011", 0, 0, 0),
        (12, 12, 12, 12, 12, "9784000000012", 0, 0, 0),
        (13, 13, 13, 13, 13, "9784000000013", 0, 0, 0),
        (14, 14, 14, 14, 14, "9784000000014", 0, 0, 0),
        (15, 15, 15, 15, 15, "9784000000015", 0, 0, 0),
        (16, 16, 16, 16, 16, "9784000000016", 0, 0, 0),
        (17, 17, 17, 17, 17, "9784000000017", 0, 0, 0),
        (18, 18, 18, 18, 18, "9784000000018", 0, 0, 0),
        (19, 19, 19, 19, 19, "9784000000019", 0, 0, 0),
        (20, 20, 20, 20, 20, "9784000000020", 0, 0, 0),
        (21, 21, 21, 21, 21, "9784000000021", 0, 0, 0),
        (22, 22, 22, 22, 22, "9784000000022", 0, 0, 0),
        (23, 23, 23, 23, 23, "9784000000023", 0, 0, 0),
        (24, 24, 24, 24, 24, "9784000000024", 0, 0, 0),
        (25, 25, 25, 25, 25, "9784000000025", 0, 0, 0),
        (26, 26, 26, 26, 26, "9784000000026", 0, 0, 0),
        (27, 27, 27, 27, 27, "9784000000027", 0, 0, 0),
        (28, 28, 28, 28, 28, "9784000000028", 0, 0, 0),
        (29, 29, 29, 29, 29, "9784000000029", 0, 0, 0),
        (30, 30, 30, 30, 30, "9784000000030", 0, 0, 0),
        (31, 31, 31, 31, 31, "9784000000031", 0, 0, 0),
        (32, 32, 32, 32, 32, "9784000000032", 0, 0, 0),
        (33, 33, 33, 33, 33, "9784000000033", 0, 0, 0),
        (34, 34, 34, 34, 34, "9784000000034", 0, 0, 0),
        (35, 35, 35, 35, 35, "9784000000035", 0, 0, 0),
        (36, 36, 36, 36, 36, "9784000000036", 0, 0, 0),
        (37, 37, 37, 37, 37, "9784000000037", 0, 0, 0),
        (38, 38, 38, 38, 38, "9784000000038", 0, 0, 0),
        (39, 39, 39, 39, 39, "9784000000039", 0, 0, 0),
        (40, 40, 40, 40, 40, "9784000000040", 0, 0, 0),
        (41, 41, 41, 41, 41, "9784000000041", 0, 0, 0),
        (42, 42, 42, 42, 42, "9784000000042", 0, 0, 0),
        (43, 43, 43, 43, 43, "9784000000043", 0, 0, 0),
        (44, 44, 44, 44, 44, "9784000000044", 0, 0, 0),
        (45, 45, 45, 45, 45, "9784000000045", 0, 0, 0),
        (46, 46, 46, 46, 46, "9784000000046", 0, 0, 0),
        (47, 47, 47, 47, 47, "9784000000047", 0, 0, 0),
        (48, 48, 48, 48, 48, "9784000000048", 0, 0, 0),
        (49, 49, 49, 49, 49, "9784000000049", 0, 0, 0),
        (50, 50, 50, 50, 50, "9784000000050", 0, 0, 0)
    ]

    names = [
        (1, "量子世界への扉"),
        (2, "Python実践入門"),
        (3, "静かな森の記録"),
        (4, "未来都市アルカ"),
        (5, "数式と星空"),
        (6, "深海研究日誌"),
        (7, "人工知能概論"),
        (8, "電脳迷宮"),
        (9, "風と図書館"),
        (10, "銀河鉄道の夢"),
        (11, "宇宙船ノア"),
        (12, "夏色ノート"),
        (13, "微分積分の旅"),
        (14, "暗号の秘密"),
        (15, "夜明けのロボット"),
        (16, "仮想世界探訪"),
        (17, "光の街"),
        (18, "量子回路設計"),
        (19, "月面都市計画"),
        (20, "時間旅行者"),
        (21, "古代文明の謎"),
        (22, "雪原の足跡"),
        (23, "音楽理論基礎"),
        (24, "プログラマの思考"),
        (25, "雲海の城"),
        (26, "電子工作入門"),
        (27, "秋風エッセイ"),
        (28, "銀色の海"),
        (29, "数理モデル入門"),
        (30, "星降るキャンパス"),
        (31, "データ分析大全"),
        (32, "生命科学の扉"),
        (33, "機械学習実験室"),
        (34, "旅する哲学"),
        (35, "空想科学読本"),
        (36, "深夜特急2050"),
        (37, "ニューラルネットの世界"),
        (38, "記憶のアーカイブ"),
        (39, "ゼロから学ぶLinux"),
        (40, "量子通信最前線"),
        (41, "桜舞う丘"),
        (42, "統計学ストーリー"),
        (43, "天体観測ガイド"),
        (44, "ロボット工学演習"),
        (45, "未来予測論"),
        (46, "サイバー都市"),
        (47, "物理法則の探求"),
        (48, "AI時代の社会"),
        (49, "深宇宙探索記"),
        (50, "知識の迷路")
    ]    
    authors = [
        (1, "山田太郎"),
        (2, "佐藤花子"),
        (3, "高橋健"),
        (4, "伊藤美咲"),
        (5, "中村誠"),
        (6, "渡辺光"),
        (7, "小林直樹"),
        (8, "加藤玲奈"),
        (9, "吉田悠人"),
        (10, "松本遥"),
        (11, "井上修司"),
        (12, "木村彩"),
        (13, "林健太"),
        (14, "清水真由"),
        (15, "山口達也"),
        (16, "森田葵"),
        (17, "阿部誠司"),
        (18, "石川由衣"),
        (19, "前田航"),
        (20, "藤井涼"),
        (21, "岡田奈々"),
        (22, "橋本蓮"),
        (23, "斎藤優"),
        (24, "池田未来"),
        (25, "原田悠"),
        (26, "福田陸"),
        (27, "西村葵"),
        (28, "長谷川誠"),
        (29, "村上真"),
        (30, "青木凛"),
        (31, "三浦直人"),
        (32, "近藤美月"),
        (33, "遠藤光"),
        (34, "坂本未来"),
        (35, "土屋蒼"),
        (36, "大野翼"),
        (37, "平野楓"),
        (38, "菅原遥"),
        (39, "安藤誠"),
        (40, "上田直樹"),
        (41, "野口彩"),
        (42, "谷口優"),
        (43, "島田涼"),
        (44, "宮本葵"),
        (45, "河野誠"),
        (46, "柴田未来"),
        (47, "久保悠斗"),
        (48, "工藤凛"),
        (49, "中川翼"),
        (50, "金子遥")
    ]

    publishers = [
        (1, "青空出版"),
        (2, "未来書房"),
        (3, "知識社"),
        (4, "銀河出版"),
        (5, "創造社"),
        (6, "北斗ブックス"),
        (7, "テクノ社"),
        (8, "風見書店"),
        (9, "学術堂"),
        (10, "星雲社"),
        (11, "白夜出版"),
        (12, "光彩堂"),
        (13, "未来堂"),
        (14, "翠文社"),
        (15, "知能出版"),
        (16, "創星社"),
        (17, "青葉書房"),
        (18, "暁出版"),
        (19, "文理社"),
        (20, "銀嶺堂"),
        (21, "新世紀ブックス"),
        (22, "東雲出版"),
        (23, "天文社"),
        (24, "風花堂"),
        (25, "アルゴ出版"),
        (26, "知恵の森"),
        (27, "蒼空社"),
        (28, "海鳴社"),
        (29, "先端出版"),
        (30, "黎明書房"),
        (31, "未来技研"),
        (32, "夢幻社"),
        (33, "探究舎"),
        (34, "無限堂"),
        (35, "虹彩堂"),
        (36, "サイエンス社"),
        (37, "テラ出版"),
        (38, "電脳書院"),
        (39, "銀翼社"),
        (40, "知新堂"),
        (41, "創研出版"),
        (42, "青嵐社"),
        (43, "未来文化社"),
        (44, "宙出版"),
        (45, "星海書房"),
        (46, "技術評論社"),
        (47, "天空社"),
        (48, "理工出版"),
        (49, "潮流社"),
        (50, "ナレッジブック")
    ]

    texts = [
        (1, "量子力学の基本概念から最新研究までをやさしく解説する入門書。観測問題や量子もつれなど不思議な現象について具体例を交えながら説明し、初学者でも読み進めやすい構成となっている。"),
        (2, "Pythonを使ったプログラミングの基礎から応用までを体系的に学べる一冊。Web開発やデータ分析、GUI制作など実践的な内容を含み、サンプルコードも豊富に掲載されている。"),
        (3, "山奥の静かな村を舞台に、人々の日常と自然との関わりを丁寧に描いた物語。季節の移り変わりと共に登場人物の心情が変化していく様子が美しく表現されている。"),
        (4, "高度に発展した未来都市で発生した事件を追うSF小説。人工知能と人類の関係、監視社会の問題など現代的なテーマを含みながらスリリングな展開が続く。"),
        (5, "数学と天文学の歴史をたどりながら、人類がどのように宇宙を理解してきたのかを紹介する科学読み物。数式の背景にある物語にも焦点を当てている。"),
        (6, "深海探査チームの活動記録をまとめたノンフィクション作品。未知の生物や海底資源についての研究成果を豊富なエピソードと共に紹介している。"),
        (7, "人工知能技術の基礎理論から応用事例までを解説する専門書。ニューラルネットワークや機械学習について図を交えて説明している。"),
        (8, "仮想空間に閉じ込められた主人公たちが謎を解きながら脱出を目指すSFアドベンチャー。ゲームと現実の境界が揺らぐ展開が特徴。"),
        (9, "古びた図書館を舞台に、本を通じて人々が交流していく心温まる物語。読書の魅力と知識の継承について描かれている。"),
        (10, "銀河を走る列車に乗り込んだ少年の冒険を描く幻想小説。旅の途中で出会う人々との交流を通じて成長していく姿が描かれる。"),
        (11, "地球を離れた宇宙船で生活する人々の日常を描いたSF作品。閉鎖空間での人間関係や未来技術について深く掘り下げている。"),
        (12, "高校生たちのひと夏の思い出を描いた青春小説。友情や進路への悩みを爽やかな文章で表現している。"),
        (13, "微分積分学の基礎から応用までを丁寧に解説した参考書。例題と演習問題が豊富で独学にも適している。"),
        (14, "古代から現代までの暗号技術の歴史を紹介しながら、情報セキュリティの重要性について解説している。"),
        (15, "感情を持つロボットが人間社会で生活する未来を描いた物語。倫理や共存について考えさせられる内容となっている。"),
        (16, "仮想現実技術を活用した新しい世界を探検するガイドブック。最新デバイスや応用例についても紹介している。"),
        (17, "光に包まれた未来都市で暮らす人々の群像劇。テクノロジーと芸術が融合した社会の姿を描いている。"),
        (18, "量子コンピュータの回路設計について基礎から学べる技術書。量子ビットやゲート操作を具体例で説明している。"),
        (19, "月面都市建設計画をテーマにした科学読み物。宇宙開発技術やエネルギー問題について詳しく解説している。"),
        (20, "偶然タイムマシンを発見した青年が歴史を巡る冒険小説。過去改変による影響を描くスリリングな展開が魅力。")
    ]

    texts += [
        (21, "古代遺跡の発掘調査を通して失われた文明の秘密に迫る歴史ミステリー。考古学の知識と冒険要素を組み合わせた読み応えのある作品。"),
        (22, "雪に覆われた大地を旅する探検隊の記録。極寒環境での生活や自然との戦いをリアルに描き出している。"),
        (23, "音楽理論の基礎を初心者向けに解説した入門書。和音やリズム、作曲の考え方について具体例を交えて説明している。"),
        (24, "優れたプログラマがどのように問題を考え解決しているのかを紹介する技術エッセイ。実践的な思考法が学べる内容。"),
        (25, "空に浮かぶ城を舞台にしたファンタジー小説。主人公たちが秘宝を巡って旅を続ける壮大な物語となっている。"),
        (26, "電子工作の基本からマイコン制御までを解説した実践書。初心者でも回路制作を楽しめるよう丁寧に構成されている。"),
        (27, "秋の景色や日常の出来事を繊細な文章で描いたエッセイ集。季節の移ろいと人々の感情が静かに綴られている。"),
        (28, "銀色に輝く海辺の町を舞台にした恋愛小説。再会した幼なじみとの交流を中心に物語が展開していく。"),
        (29, "数理モデルを用いて社会現象や自然現象を分析する方法を解説した専門書。実例を交えながら数学的考え方を紹介している。"),
        (30, "大学の天文サークルに所属する学生たちの青春を描いた物語。星空観測を通じて友情と夢を育んでいく。"),
        (31, "データ分析の基礎から機械学習まで幅広く扱う解説書。統計処理や可視化技術についても詳しく説明している。"),
        (32, "生命科学の発展と最新研究についてわかりやすく紹介する科学書。遺伝子編集や再生医療にも触れている。"),
        (33, "機械学習モデルを実際に構築しながら学べる実践的な技術書。Pythonによるコード例が多数掲載されている。"),
        (34, "旅先で出会う人々との会話を通じて哲学的テーマを考察する紀行エッセイ。人生観について深く考えさせられる。"),
        (35, "一見空想に思える科学技術について現実的な視点から検証するユニークな科学読み物。身近な例も多く親しみやすい。"),
        (36, "2050年の未来社会を舞台にしたロードムービー風SF小説。超高速交通網で各地を巡る主人公の旅を描いている。"),
        (37, "ニューラルネットワークの理論と実装方法について詳しく解説した専門書。深層学習の基礎を学ぶことができる。"),
        (38, "人々の記憶を保存できる技術が普及した世界を描く近未来小説。記憶と人格の関係について問いかけている。"),
        (39, "Linuxの基本操作からシステム管理までを初心者向けに説明した入門書。コマンド例が豊富に掲載されている。"),
        (40, "量子通信技術の原理と将来性について解説する技術書。量子暗号や次世代ネットワークへの応用を紹介している。"),
        (41, "桜が舞う丘の上で再会した旧友たちの交流を描いた感動小説。時間の流れと友情の大切さがテーマとなっている。"),
        (42, "統計学の基本概念をストーリー形式で学べる教育書。データの見方や分析方法を直感的に理解できる構成。"),
        (43, "初心者向けの天体観測ガイド。星座の探し方や望遠鏡の使い方について写真付きで丁寧に説明している。"),
        (44, "ロボット工学の基礎理論から制御技術までを学べる教科書。センサーやモーター制御についても解説している。"),
        (45, "未来社会を予測するための技術動向や経済変化について分析した評論集。AIやエネルギー問題にも触れている。"),
        (46, "巨大ネットワークで管理された近未来都市を舞台にしたサイバーパンク小説。自由と監視の対立を描いている。"),
        (47, "古典力学から量子力学まで物理法則の成り立ちを紹介する科学書。実験例や歴史的背景も豊富に取り上げている。"),
        (48, "AI技術が普及した社会で人々の働き方や価値観がどう変化するのかを考察する社会学的読み物。"),
        (49, "深宇宙探査船に乗り込んだ研究者たちの冒険を描くSF作品。未知の惑星や異星文明との遭遇が大きな見どころ。"),
        (50, "広大な図書館世界を巡りながら知識の意味を探していく幻想文学作品。本と記憶をテーマにした物語となっている。")
    ]

    # テスト用データ追加

    books += [
        (51, 51, 51, 51, 51, "9784000000051", 1, 0, 0),
        (52, 52, 52, 52, 52, "9784000000052", 0, 1, 0),
        (53, 53, 53, 53, 53, "9784000000053", 0, 0, 1),
        (54, 54, 54, 54, 54, "9784000000054", 1, 1, 0),
        (55, 55, 55, 55, 55, "9784000000055", 0, 1, 1),
        (56, 56, 56, 56, 56, "9784000000056", 1, 0, 1),
        (57, 57, 57, 57, 57, "9784000000057", 1, 1, 1),
        (58, 58, 58, 58, 58, "9784000000058", 0, 0, 0),
        (59, 59, 59, 59, 59, "9784000000059", 1, 0, 0),
        (60, 60, 60, 60, 60, "9784000000060", 0, 1, 0)
    ]

    names += [
        (51, "重複ISBNテスト"),
        (52, "貸出中テスト"),
        (53, "予約済みテスト"),
        (54, "禁書フラグ確認"),
        (55, "特殊文字テスト☆"),
        (56, "超長タイトルの確認用データベース設計入門完全版"),
        (57, "空白 テスト"),
        (58, "NULL確認用"),
        (59, "検索動作確認"),
        (60, "最終テストデータ")
    ]

    authors += [
        (51, "Test Author"),
        (52, "Admin User"),
        (53, "System Writer"),
        (54, "Debug Tester"),
        (55, "Sample Name"),
        (56, "Long Name Author Example"),
        (57, "Space User"),
        (58, "Null Checker"),
        (59, "Search Engine"),
        (60, "Final Writer")
    ]

    publishers += [
        (51, "Test出版"),
        (52, "Debug社"),
        (53, "System Books"),
        (54, "Checker出版"),
        (55, "Sample社"),
        (56, "Long Publisher Name Books"),
        (57, "Space出版"),
        (58, "Null出版"),
        (59, "Search社"),
        (60, "Final出版")
    ]

    texts += [
        (51, "ISBNやIDの扱いを確認するためのテストデータ。データベースで重複処理や検索動作を確認する用途を想定している。"),
        (52, "貸出中フラグが有効になっている状態を確認するためのデータ。貸出画面や返却処理の動作テストに利用できる。"),
        (53, "予約済み状態を確認するためのテストデータ。ユーザー予約機能や一覧表示の確認に使用する。"),
        (54, "禁書フラグが立った場合に一覧や検索結果でどのように表示されるかを確認するためのデータ。"),
        (55, "特殊文字や記号を含むタイトルや出版社名の表示確認を目的としたテスト用データ。文字化け確認にも利用可能。"),
        (56, "非常に長いタイトルや著者名を扱った場合にレイアウト崩れやデータ切り捨てが起こらないか確認するためのデータ。"),
        (57, "空白を含むデータの検索や表示を確認するためのテストデータ。部分一致検索などにも利用できる。"),
        (58, "NULL値や空データを扱う処理を確認するために利用するサンプルデータ。例外処理の確認にも役立つ。"),
        (59, "検索機能の動作確認を行うためのテストデータ。タイトル検索や著者検索など複数条件を試す用途に向いている。"),
        (60, "最終的な総合テスト用データ。登録、検索、貸出、予約など一連の機能確認に使用することを想定している。")
    ]
    with sqlite3.connect('lib_sys.db') as conn:
        cur = conn.cursor()
        cur.executemany(
                    """INSERT INTO zosho
                    (id,name_id,author_id,publisher_id,textsource_id,isbn,kashidashi,kinsho,yoyaku) 
                    VALUES (?,?,?,?,?,?,?,?,?)
                    """,
                    books
                    )
        cur.executemany(
                    """INSERT INTO name
                    (id,name) 
                    VALUES (?,?)
                    """,
                    names
                    )

        cur.executemany(
                    """INSERT INTO author
                    (id,author) 
                    VALUES (?,?)
                    """,
                    authors
                    )
        cur.executemany(
                    """INSERT INTO publisher
                    (id,publisher) 
                    VALUES (?,?)
                    """,
                    publishers
                    )

        cur.executemany(
                    """INSERT INTO textsource
                    (id,textsource) 
                    VALUES (?,?)
                    """,
                    texts
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


#まだ
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
#まだ
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

#まだ
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



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
from collections import Counter
import math
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from ja_stopword_filter import JaStopwordFilter
import numpy as np
import pandas as pd

# 自力で一から実装中
#=====================================================================================================
#文章を入力して検索ができるモード
def huwatto(content,conleng):
        #sudachi.pyから始めている
        # tokenizer_obj = dictionary.Dictionary().create()
        # # 複数粒度分割
        # mode = tokenizer.Tokenizer.SplitMode.A
        # print ([m.surface() for m in tokenizer_obj.tokenize(content, mode)])
        #contentをそのまま持ってきている.
        #なのでスペースの空いた単語の列がそのまま来ている
        #単語に分けれた
        #conは分けたデータ
    #文章を単語に分けている（計算　機　科学）
    con = word_bunri(content)
    #文章の中で単語が出てくる頻度
    tf = tf_calc(con)
    #文章の中でどれだけその単語が出てこないか
    idf = idf_calc(con)
    #idfとtfをかけた値
    tf_idf = tf_idf_calc(idf,tf,conleng)
    # テスト用
    # mkmatrix(con,conleng,tf,idf,tf_idf)
        #文書ごとの総tf_idf値を計算
        #tf-idfをconの長さ分繰り返して計算
    return tf_idf

#文書の数
def count_word_all(con):
    with sqlite3.connect('lib_sys.db') as conn:
        cur = conn.cursor()
        result = []
        for c in con:
            cnt = 0
            i = 1
            while i <= count_book():
                #一件ずつテキストをとってくる
                cur.execute(
                            """
                            SELECT
                                textsource
                            FROM
                                textsource
                            WHERE 
                                id = ?
                            """,(i,)
                            )
                conn.commit()
                rows = cur.fetchone()
                row = rows[0]
                #カウントアップ
                if c in row:
                    cnt += 1
                i += 1
            result.append(cnt)
        #何を返したらいい？

    return result

#ある単語がすべての文書からあった総数
def count_word_from_one(con):
    with sqlite3.connect('lib_sys.db') as conn:
        cur = conn.cursor()
        result = []
        for c in con:
            cnt = 0
            i = 1
            while i <= count_book():
                #一件ずつテキストをとってくる
                cur.execute(
                            """
                            SELECT
                                textsource
                            FROM
                                textsource
                            WHERE 
                                id = ?
                            """,(i,)
                            )
                conn.commit()
                rows = cur.fetchone()
                row = rows[0]
                #カウントアップ
                cnt += row.count(f"{c}")
                i += 1
            result.append(cnt)

    return result

# n/ntを計算　nは全文書数 ntはその単語を含む文書数
def idf_calc(con):
    n = count_book()
    nt = count_word_all(con)
    result = []
    for val in nt:
        if val != 0:
            idf = math.log(n/nt)
            result.append(idf)
        else:
            idf = "error"
            result.append(idf)
    return result


def tf_calc(content):
    # 単語の出現回数をカウント
    result = []
    tf = count_word_from_one(content)
    for val in tf:
        result.append(math.log(val+1))
    
    return result

def word_bunri(content):
    tokenizer_obj = dictionary.Dictionary().create()
    mode = tokenizer.Tokenizer.SplitMode.A
    result = [m.surface() for m in tokenizer_obj.tokenize(content, mode)]
    return result 

def tf_idf_calc(idf,tf,conleng):
    i = 0
    val = []
    while i < conleng:
        tf[i] * idf[i]
        i += 1
        val.append()
    return val

#ここで値も入れてしまいたい
def mkmatrix(con,conleng,tf,idf,tf_idf):
    rows, cols = conleng,4 
    matrix = [[0 for _ in range(cols)] for _ in range(rows)]
    i = 0
    while i < conleng:
        matrix[i][1] = con[i]
        matrix[i][2] = tf[i]
        matrix[i][3] = idf[i]
        matrix[i][4] = tf_idf[i]
        i += 1

#どれだけ蔵書があるかカウント
def count_book():
    with sqlite3.connect('lib_sys.db') as conn:
        cur = conn.cursor()
        cur.execute(
                    """
                    SELECT id
                    FROM zosho
                    ORDER BY id DESC
                    LIMIT 1
                    """
                    )
        conn.commit()
        rows = cur.fetchall()
        rows = rows[0]
        row = rows[0] 
    return row

#=========================================================================

# tf-idfの準備
def pre_insed_tf_tdf():
    content = []
    with sqlite3.connect('lib_sys.db') as conn:
        cur = conn.cursor()
        # 全書籍のtextsource（あらすじみたいなもの）を持ってくる
        for d in range(count_book()):
            cur.execute(
                    """
                    SELECT
                        textsource
                    FROM
                        textsource
                    WHERE 
                        id = ?
                    """,(d+1,)
                    )
            conn.commit()
            rows = cur.fetchall()
            rows = rows[0]
            rows = rows[0]
            content.append(rows)

    # 単語を分ける
    content = [" ".join(word_bunri(text))for text in content]
        # 分かち書き済み
    # 出現回数を調べる
    count_vect = CountVectorizer()
    # 単語の出現回数をベクトルにしている
    X_counts = count_vect.fit_transform(content)
    # tf-idfを計算、正規化
    tfidf_transformer = TfidfTransformer()
    X_tfidf = tfidf_transformer.fit_transform(X_counts)
        # テスト用
    # 見出し語の取得
    feature_names = count_vect.get_feature_names_out()
    # 表示
    df = pd.DataFrame(X_tfidf.toarray(), columns=feature_names)

    return X_tfidf,content

def insed_tf_tdf(word,X_tfidf,con):
    #検索語の分かち書き
    content = word_bunri(word)
    content = rm_stopword(content)

    #総文書数を表示
    rows = count_book()
    tmp = 0.0
    val = []
    #文書の中から一つ選択（繰り返す）
    for j in range(rows):
        tmp = 0.0
        #検索語の中から一つ選択（繰り返す）
        for s in content:
            #文書の中の分かち書きした単語を一つ選択して一致するか総当たりで見る
            mask = np.array([s in doc for doc in con])
            #1の要素の位置を返す（1の場所だけになる）
            #タプルが返るため[0]
            matched_indices = np.where(mask)[0]
            for idx in matched_indices:
                if X_tfidf[j,idx] == 0.0:
                    tmp += 0
                else:
                    tmp += X_tfidf[j,idx]
                    #桁数2で切り捨てたい
                    tmp = math.floor(tmp * 10**2) / (10**2)
        val.append(tmp)
    scores = list(enumerate(val))
    scores.sort(key=lambda x: x[1], reverse=True)
    scores = [(i, float(score)) for i, score in scores]
    return scores

# tf-idf検索
def huwatto(scores):

    tmp = []

    for score in scores:
        tmp.append(score[0])


    with sqlite3.connect('lib_sys.db') as conn:
        cur = conn.cursor()

        placeholders = ",".join(["?"] * len(tmp))
        cur.execute(
                    f"""
                    SELECT name.name,author.author,publisher.publisher,zosho.isbn,zosho.kashidashi,zosho.yoyaku
                    FROM zosho
                    JOIN name 
                    ON zosho.name_id = name.id
                    JOIN author
                    ON zosho.author_id = author.id
                    JOIN publisher
                    ON zosho.publisher_id = publisher.id
                    WHERE zosho.id IN ({placeholders})
                    """,(tmp)
                    )
        rows = cur.fetchall()
        return rows

# 文章を単語に
def word_bunri(content):
    tokenizer_obj = dictionary.Dictionary().create()
    mode = tokenizer.Tokenizer.SplitMode.A
    result = [m.surface() for m in tokenizer_obj.tokenize(content, mode)]
    return result 

# ストップワード（は、とか、を、とか検索語彙としてひっかかってほしくないワード）
def rm_stopword(tokens):
    # フィルタの初期化
    custom_wordlist = []
    filter = JaStopwordFilter(
        convert_full_to_half=True,  # 全角文字を半角文字に変換
        use_slothlib=True,         # SlothLibのストップワードを使用
        filter_length=1,           # 文字数が1以下のトークンを削除
        use_date=True,             # 日付形式のトークンを削除
        use_numbers=True,          # 数字のトークンを削除
        use_symbols=True,          # 記号を削除
        use_spaces=True,           # 空白トークンを削除
        use_emojis=True,           # 絵文字を削除
        custom_wordlist=custom_wordlist  # ユーザー定義ストップワードを追加
    )

    # トークンをフィルタリング
    filtered_tokens = filter.remove(tokens)
    return filtered_tokens

# 特定の値以下のデータを削除
def ashikiri(scores):
    scores = [score for score in scores if score[1] > 1.0]    
    return scores

# テーブルを作る
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


#5つの項目で検索をかける
def search_5(id=None, name=None, author=None, publisher=None, isbn=None):
    s_id = None
    # where句に書く条件をためておくためのリスト
    conditions1 = []
    conditions2 = []
    conditions3 = []
    conditions4 = []
    # プレースホルダーに代入するためのリスト
    values1 = []
    values2 = []
    values3 = []
    values4 = []

    with sqlite3.connect('lib_sys.db') as conn:
        cur = conn.cursor()
        # idの条件の追加
        if id:
            conditions1.append("id = ?")
            conditions2.append("id = ?")
            conditions3.append("id = ?")
            conditions4.append("id = ?")
            values1.append(id)
            values2.append(id)
            values3.append(id)
            values4.append(id)
        # 書名の条件の追加
        if name:
            conditions2.append("name = ?")
            values2.append(name)
        # 著者名の条件の追加
        if author:
            conditions3.append("author = ?")
            values3.append(author)
        # isbnの条件の追加
        if isbn:
            conditions1.append("isbn = ?")
            values1.append(isbn)
        # 出版社の条件の追加
        if publisher:
            conditions4.append("publisher = ?")
            values4.append(publisher)

        # クエリの組立
        query1 = "SELECT * FROM zosho"
        query2 = "SELECT * FROM name"
        query3 = "SELECT * FROM author"
        query4 = "SELECT * FROM publisher"

        if conditions1 != []:
            # クエリに条件を付与
            query1 += " WHERE " + " AND ".join(conditions1)
        

        if conditions2 != []:
            # クエリに条件を付与
            query2 += " WHERE " + " AND ".join(conditions2)

        if conditions3 != []:
            # クエリに条件を付与
            query3 += " WHERE " + " AND".join(conditions3)


        if conditions4 != []:
            # クエリに条件を付与
            query4 += " WHERE " + " AND".join(conditions4)

        # 条件が加わっていればクエリ実行
        if len(query1) > 19:
            cur.execute(query1, values1)
            conn.commit()
            rows = cur.fetchall()
            s_id = [row[0] for row in rows]
            # 表を組み立て
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

        # 条件が加わっていればクエリ実行
        if len(query2) > 18:
            cur.execute(query2, values2)
            conn.commit()
            rows= cur.fetchall()
            s_id = [row[0] for row in rows]
            # 表を組み立て
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
                if rows != []:
                    return rows

        # 条件が加わっていればクエリ実行
        if len(query3) > 20:
            cur.execute(query3, values3)
            conn.commit()
            rows= cur.fetchall()
            s_id = [row[0] for row in rows]
            # 表を組み立て
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
                if rows != []:
                    return rows

        # 条件が加わっていればクエリ実行
        if len(query4) > 23:
            cur.execute(query4, values4)
            conn.commit()
            rows= cur.fetchall()
            s_id = [row[0] for row in rows]
            # 表を組み立て
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
                if rows != []:
                    return rows




#8つの項目で検索をかける
def search_8(id=None,name=None,author=None,publisher=None,isbn=None,kashidashi=None,kinsho=None,yoyaku=None):
    s_id = None
    # where句に書く条件をためておくためのリスト
    conditions1 = []
    conditions2 = []
    conditions3 = []
    conditions4 = []
    # プレースホルダーに代入するためのリスト
    values1 = []
    values2 = []
    values3 = []
    values4 = []
    with sqlite3.connect('lib_sys.db') as conn:
        cur = conn.cursor()
        # idの条件の追加
        if id:
            conditions1.append("id = ?")
            conditions2.append("id = ?")
            conditions3.append("id = ?")
            conditions4.append("id = ?")
            values1.append(id)
            values2.append(id)
            values3.append(id)
            values4.append(id)
        # 書名の条件の追加
        if name:
            conditions2.append("name = ?")
            values2.append(name)
        # 著者名の条件の追加
        if author:
            conditions3.append("author = ?")
            values3.append(author)
        # 出版社の条件の追加
        if publisher:
            conditions4.append("publisher = ?")
            values4.append(publisher)
        # isbnの条件の追加
        if isbn:
            conditions1.append("isbn = ?")
            values1.append(isbn)
        # 貸出済みかの条件の追加
        if kashidashi:
            conditions1.append("kashidashi = ?")
            values1.append(kashidashi)
        # 禁書になってるかの条件の追加
        if kinsho:
            conditions1.append("kinsho = ?")
            values1.append(kinsho)
        # 予約済みかの条件の追加
        if yoyaku:
            conditions1.append("yoyaku = ?")
            values1.append(yoyaku)
        # クエリの組立
        query1 = "SELECT * FROM zosho"
        query2 = "SELECT * FROM name"
        query3 = "SELECT * FROM author"
        query4 = "SELECT * FROM publisher"

        # クエリに条件を付与
        if conditions1 != []:
            query1 += " WHERE " + " AND ".join(conditions1)
        
        # クエリに条件を付与
        if conditions2 != []:
            query2 += " WHERE " + " AND ".join(conditions2)
        # クエリに条件を付与
        if conditions3 != []:
            query3 += " WHERE " + " AND".join(conditions3)

        # クエリに条件を付与
        if conditions4 != []:
            query4 += " WHERE " + " AND".join(conditions4)
        # 条件が加わっていればクエリ実行
        if len(query1) > 19:
            cur.execute(query1, values1)
            conn.commit()
            rows = cur.fetchall()
            s_id = [row[0] for row in rows]
            for row_id in s_id:
                # 表を組み立て
                cur.execute("""
                            PRAGMA table_info(zosho)
                            """
                            )
                conn.commit()
                rows = cur.fetchall()
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
                if rows != []:
                    return rows
        # 条件が加わっていればクエリ実行
        if len(query2) > 18:
            cur.execute(query2, values2)
            conn.commit()
            rows= cur.fetchall()
            s_id = [row[0] for row in rows] 
            for row_id in s_id:
                # 表を組み立て
                cur.execute("""
                            PRAGMA table_info(name)
                            """
                            )
                conn.commit()
                rows = cur.fetchall()
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
                if rows != []:
                    return rows

        # 条件が加わっていればクエリ実行
        if len(query3) > 20:
            cur.execute(query3, values3)
            conn.commit()
            rows= cur.fetchall()
            s_id = [row[0] for row in rows]
            for row_id in s_id:
                # 表を組み立て
                cur.execute("""
                            PRAGMA table_info(author)
                            """
                            )
                conn.commit()
                rows = cur.fetchall()
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
                if rows != []:
                    return rows

        # 条件が加わっていればクエリ実行
        if len(query4) > 23:
            cur.execute(query4, values4)
            conn.commit()
            rows= cur.fetchall()
            s_id = [row[0] for row in rows]
            # 表を組み立て
            for row_id in s_id:
                cur.execute("""
                            PRAGMA table_info(publisher)
                            """
                            )
                conn.commit()
                rows = cur.fetchall()
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
                if rows != []:
                    return rows

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

#データベースの内容の更新
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


#書籍の追加用
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
        flg = 0
        return flg 
#書籍データの削除用
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
        return 1

#禁書登録用
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

# 禁書登録の解除用
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


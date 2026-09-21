
import sqlite3


# -------------------------------------------------
# メソッド名：search_5
# 引数　：id （書籍ごとに振ってあるid）
#        name（書籍の名前）
#        author（著者の名前）
#        publisher（出版社の名前）
#        isbn（書籍に割り振られた国際規格の番号）
# 返却値：rows（検索クエリの結果）
# 処理の説明
# idでの検索条件、nameでの検索条件、authorでの検索条件、publisherでの検索条件、isbnでの検索条件、
# をそれぞれconditionsとvaluesに追加していき、conditionsが空でなかったらqueryにWHERE句を付与。
# 条件が加わっていれば、検索クエリ実行
# -------------------------------------------------
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
                # rowsが空じゃなければ値を返す
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
                # rowsが空じゃなければ値を返す
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
                # rowsが空じゃなければ値を返す
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
                # rowsが空じゃなければ値を返す
                if rows != []:
                    return rows




# -------------------------------------------------
# メソッド名：search_8
# 引数　：id（書籍ごとのに振ってあるid）
#        name（書籍の名前）
#        author（著者の名前）
#        publisher（出版社の名前）
#        isbn（書籍に割り振られた国際規格の番号）
#        kashidashi（貸し出しているか判別するフラグ）
#        kinsho（禁書になってるか判断するフラグ）
#        yoyaku（予約されているか判断するフラグ）
# 返却値：rows（検索クエリの実行結果）
# 処理の説明
# idでの検索条件、nameでの検索条件、authorでの検索条件、publisherでの検索条件、isbnでの検索条件、kashidashiでの検索条件、
# kinshoでの検索条件、yoyakuでの検索条件、
# をそれぞれconditionsとvaluesに追加していき、conditionsが空でなかったらqueryにWHERE句を付与。
# 条件が加わっていれば、検索クエリ実行
# -------------------------------------------------
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



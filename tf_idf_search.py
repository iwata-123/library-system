import sqlite3
import math
from sudachipy import tokenizer
from sudachipy import dictionary
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from ja_stopword_filter import JaStopwordFilter
import pandas as pd

# tf-idf検索を自力で一から実装中（ 28行目から187行目まで）
# 既存機能があるが勉強のため自分で一から実装している
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



# -------------------------------------------------
# メソッド名：pre_insed_tf_tdf
# 引数　：なし
# 返却値：X_tfidf (tf-idfを計算、正規化後のデータ),
#        content（検索ワードからスペースを除去してリストにしたもの） 
#
# 処理の説明
# ライブラリになっているtf-idfの前処理
#       単語を語の区切りで分けて
#       出現回数を調べ
#       ベクトルにして
#       tf-idfを計算、正規化
#       見出し語の取得
# をしています
# 全書籍にすることでどんな単語がどれくらい入っているか
# ベクトルの形式で保存しておいています
# -------------------------------------------------
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
    count_vect = CountVectorizer(min_df=0.1,max_df=25)
    # 単語の出現回数をベクトルにしている
    X_counts = count_vect.fit_transform(content)
    # tf-idfを計算、正規化
    tfidf_transformer = TfidfTransformer()
    X_tfidf = tfidf_transformer.fit_transform(X_counts)
        # テスト用
    # 見出し語の取得
    feature_names = count_vect.get_feature_names_out()
    # 表示
    # 開発用
    df = pd.DataFrame(X_tfidf.toarray(), columns=feature_names)

    return X_tfidf,feature_names



# -------------------------------------------------
# メソッド名：insed_tf_tdf
# 引数　：word（検索語）
#        X_tfidf（tf-idfを計算、正規化後のデータ）
#        con（全文書を前処理してベクトル化したもの）
# 返却値：scores（tf-idf計算結果）
# 処理の説明：
# 検索した単語に対して語の区切りで分けて
# 総文書数を計算して
# 文書ごとに検索語を一つずつあるか検索をかける
# -------------------------------------------------

def insed_tf_tdf(word, X_tfidf, feature_names):
    # 検索語の分かち書き
    content = word_bunri(word)
    content = rm_stopword(content)

    # 総文書数
    rows = X_tfidf.shape[0]
    # 語彙一覧をリスト化
    feature_list = feature_names.tolist()

    val = []
    for j in range(rows):
        tmp = 0.0
        for s in content:
            if s in feature_list:
                idx = feature_list.index(s)
                score = X_tfidf[j, idx]
                if score != 0.0:
                    tmp += score
                    tmp = math.floor(tmp * 10**2) / (10**1)
        val.append(tmp)

    scores = list(enumerate(val))
    scores.sort(key=lambda x: x[1], reverse=True)
    scores = [(i, float(score)) for i, score in scores]
    return scores
# -------------------------------------------------
# メソッド名：huwatto
# 引数　：scores（文書ごとのtf-idfの結果）
# 返却値：rows（検索クエリの結果）
# 処理の説明
# tf-idfの結果がリストなのでほしい情報を一つのリストにする
# そのリスト検索クエリを実行
# -------------------------------------------------
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



# -------------------------------------------------
# メソッド名：word_bunri
# 引数　：content（検索ワードや文書の内容（textsource））
# 返却値：result （文章を語の区切りで分けた結果）
# 処理の説明
# sudachi.pyというライブラリを用いて文章を分ける
# -------------------------------------------------
def word_bunri(content):
    tokenizer_obj = dictionary.Dictionary().create()
    mode = tokenizer.Tokenizer.SplitMode.A
    result = [m.surface() for m in tokenizer_obj.tokenize(content, mode)]
    return result 



# -------------------------------------------------
# メソッド名：rm_stopword
# 引数　：tokens（）
# 返却値：filtered_tokens（）
# 処理の説明
# 文章を語の区切りで分けたものからストップワード（は、とか、を、とか
# 検索語彙としてひっかかってほしくないワード）
# を除去
# -------------------------------------------------
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

# -------------------------------------------------
# メソッド名：ashikiri
# 引数　：scores（tf-idfをした後の結果）
# 返却値：scores（足切を設けた後の結果）
# 処理の説明
# 0.8未満のtf-idfの結果を削除
# 
# -------------------------------------------------
def ashikiri(scores):
    scores = [score for score in scores if score[1] > 0.8]    
    return scores

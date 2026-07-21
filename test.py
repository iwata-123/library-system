# import sqlite3
# from flask import Flask,render_template,request,jsonify
# import json
# import main
# import math
# import tsuika
# import pandas as pd
# import numpy as np

# from ja_stopword_filter import JaStopwordFilter
# from sudachipy import tokenizer
# from sudachipy import dictionary

# from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer

# main.maketable()
# tsuika.pre_tsuika()

# #tf,idf,tf-idfについてどの文書ごとに計算しているか全部なのか一部なのか


# def huwatto(word):
#     #sudachi.pyから始めている
#     # tokenizer_obj = dictionary.Dictionary().create()
#     # # 複数粒度分割
#     # mode = tokenizer.Tokenizer.SplitMode.A
#     # print ([m.surface() for m in tokenizer_obj.tokenize(content, mode)])
#     #contentをそのまま持ってきている.
#     #なのでスペースの空いた単語の列がそのまま来ている
#     #単語に分けれた
#     #conは分けたデータ
#     #
#     content = []
#     with sqlite3.connect('lib_sys.db') as conn:
#         cur = conn.cursor()
#         for d in range(count_book()):
#         # for d in range():
#             cur.execute(
#                     """
#                     SELECT
#                         textsource
#                     FROM
#                         textsource
#                     WHERE 
#                         id = ?
#                     """,(d+1,)
#                     )
#             conn.commit()
#             rows = cur.fetchall()
#             rows = rows[0]
#             rows = rows[0]
#             content.append(rows)
#     con = word_bunri(content)
#     print(con)
#     filtered_tokens = rm_stopword(con)
#     idf = idf_calc(filtered_tokens)
#     tf = tf_calc(filtered_tokens)
#     conleng = len(idf)
#     tf_idf = tf_idf_calc(idf,tf)
#     # mkmatrix(filtered_tokens,conleng,tf_idf)
#     #文書ごとの総tf_idf値を計算
#     #tf-idfをconの長さ分繰り返して計算
#     filtered_word = rm_stopword(word)
#     s_idf = idf_calc(filtered_word)
#     s_tf = tf_calc(filtered_word)
#     conleng = len(s_idf)
#     tf_idf = tf_idf_calc(s_idf,s_tf)

#     result = sum(tf_idf,conleng)
#     print(len(result))
#     print(len(filtered_tokens))
#     result.sort()
#     print(result[0:10])
#     print(result[11:20])
#     print(result[21:30])
#     print(result[31:40])
#     print(result[41:50])
#     print(result[51:60])
#     print(result[61:70])
#     print(result[71:80])
#     print(result[81:90])


# def sum(tf_idf,conleng):
#     c = 0
#     result = []
#     while c < count_book():
#         val = 0
#         i = 0
#         while i < conleng:
#             val += tf_idf[i][c]
#             i += 1
#         result.append(val)
#         c += 1
#     return result


# def rm_stopword(tokens):
#     # フィルタの初期化
#     custom_wordlist = []
#     filter = JaStopwordFilter(
#         convert_full_to_half=True,  # 全角文字を半角文字に変換
#         use_slothlib=True,         # SlothLibのストップワードを使用
#         filter_length=1,           # 文字数が1以下のトークンを削除
#         use_date=True,             # 日付形式のトークンを削除
#         use_numbers=True,          # 数字のトークンを削除
#         use_symbols=True,          # 記号を削除
#         use_spaces=True,           # 空白トークンを削除
#         use_emojis=True,           # 絵文字を削除
#         custom_wordlist=custom_wordlist  # ユーザー定義ストップワードを追加
#     )

#     # トークンをフィルタリング
#     filtered_tokens = filter.remove(tokens)
#     print("#################")
#     print(filtered_tokens) 
#     return filtered_tokens

# #どれだけ蔵書があるかカウント
# #蔵書数を持ってくる
# def count_book():
#     with sqlite3.connect('lib_sys.db') as conn:
#         cur = conn.cursor()
#         cur.execute(
#                     """
#                     SELECT id
#                     FROM zosho
#                     ORDER BY id DESC
#                     LIMIT 1
#                     """
#                     )
#         conn.commit()
#         rows = cur.fetchall()
#         rows = rows[0]
#         row = rows[0]
#     return row

# #文書全体に関して検索
# #文書の数
# def count_word_all(con):
#     with sqlite3.connect('lib_sys.db') as conn:
#         cur = conn.cursor()
#         result = []
#         for c in con:
#             cnt = 0
#             i = 1
#             #蔵書数まで繰り返し
#             while i <= count_book():
#                 #一件ずつテキストをとってくる
#                 cur.execute(
#                             """
#                             SELECT
#                                 textsource
#                             FROM
#                                 textsource
#                             WHERE 
#                                 id = ?
#                             ORDER BY id DESC
#                             """,(i,)
#                             )
#                 conn.commit()
#                 rows = cur.fetchone()
#                 row = rows[0]
#                 #カウントアップ
#                 if c in row:
#                     cnt += 1
#                 i += 1
#             result.append(cnt)

#     return result

# #文書全体に関して検索
# #ある単語がすべての文書の中に対して何個あったか
# def count_word_from_one(con,conleng):
#     with sqlite3.connect('lib_sys.db') as conn:
#         cur = conn.cursor()
#         #rowsが索引語数colsが文書数
#         matrix = [[0 for _ in range(count_book())] for _ in range(conleng)]
#         #蔵書数まで繰り返し
#         #二次元のデータを返してみる
#         #処理済みの検索された文字を一つずつ取り出す
#         for c in con:
#             tmp = []
#             cnt = 0
#             #一件ずつテキストをとってくる
#             i = 1
#             while i <= count_book():
#                 cur.execute(
#                             """
#                             SELECT
#                                 textsource
#                             FROM
#                                 textsource
#                             WHERE 
#                                 id = ?
#                             ORDER BY id DESC
#                             """,(i,)
#                             )
#                 conn.commit()
#                 rows = cur.fetchone()
#                 row = rows[0]
#                 #カウント
#                 #個数を小数にして小数第二位にする
#                 cnt = round(float(row.count(f"{c}")),2) 
#                 i += 1
#                 tmp.append(cnt)
#             matrix.append(tmp)

#     return matrix

# #
# def idf_calc(con):
#     n = count_book()
#     nt = count_word_all(con)
#     result = []
#     for val in nt:
#         if val != 0:
#             idf = math.log((n + 1) / (val + 1)) + 1
#             # idf = math.log(n/val) + 0.25
#             idf = round(idf, 2)
#             result.append(idf)
#         else:
#             idf = 0
#             result.append(idf)
#     return result

# def tf_calc(content):
#     # 単語の出現回数をカウント
#     matrix = []
#     conleng = len(content)
#     tf = count_word_from_one(content,conleng)
#     #行を取り出す
#     for val in tf:
#         tmp = []
#         #rowsが索引語数colsが文書数
#         #要素を取得
#         for v in val:
#         #二次元のネストにする
#             tmp.append(math.log10(v+2))
#         matrix.append(tmp)
#     return matrix

# def word_bunri(content):
#     tokenizer_obj = dictionary.Dictionary().create()
#     mode = tokenizer.Tokenizer.SplitMode.A
#     result = [m.surface() for m in tokenizer_obj.tokenize(content, mode)]
#     return result 

# def tf_idf_calc(idf,tf):
#     matrix = []
#     #idfリストからひとつずつ取り出す
#     for i in idf:
#         tmp = []
#         #tf:   rowsが索引語数colsが文書数
#         #tfリストから行をひとつずつ取り出す
#         for t in tf:
#             #行から要素をひとつずつ取り出す
#             for x in t:
#                 x = float(x)
#                 tf_idf = x * i
#                 tmp.append(tf_idf)
#         matrix.append(tmp)
#     return matrix

# #ここで値も入れてしまいたい
# def mkmatrix(con,conleng,tf_idf):
#     #rowsが索引語colsが文書
#     """
#         t1 t2 t3 t4
#     w1
#     w2
#     w3
#     w4
#     """
#     # rows, cols = conleng,count_book()
#     # matrix = [[0 for _ in range(cols)] for _ in range(rows)]
#     # i = 0
#     # while i < conleng:
#     #     for val in tf_idf:
#     #         matrix[i][3] = val[i][]
#     #     i += 1
#     # for row in matrix:
#     #     print(row)
#     print("\t")
#     for val in range(count_book()):
#         print("################################")
#         print("\t\t" + "t" + str(val))
#     for c in con:
#         print(c,end="\t")
#         for matrix in tf_idf:
#             for m in matrix:
#                 print(m,end="\t")
#     print("\n")



print(0.0 <= 1)
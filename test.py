# import sqlite3
# from flask import Flask,render_template,request,jsonify
# import json
# import main

# main.maketable()
# main.pre_tsuika()

# d = {}
# index = 0
# keys = []
# values = []
# isbn = ""
# # isbndata = request.get_json()
# # isbn = isbndata.get("isbn")
# # isbn = isbn["isbn"]
# isbn += '978%'
# with sqlite3.connect('lib_sys.db') as conn:
#     cur = conn.cursor()
#     cur.execute("""
#                 SELECT name_id
#                 FROM zosho
#                 WHERE isbn 
#                 LIKE ?
#                 """,(f"{isbn}",)
#                 )
#     conn.commit()
#     name_id = cur.fetchall()
#     # name_id = name_id[0]
#     # name_id = name_id[0]
#     print(name_id)
#     for namae in name_id:
#         namae = namae[0]
#         cur.execute("""
#                     SELECT name
#                     FROM name
#                     WHERE id = ?
#                     """,(f"{namae}",)
#                     )
#         conn.commit()
#         kouho = cur.fetchall()
#         for k in kouho:
#             #zipを使う、[]に追加していく
#             keys.append(index)
#             index+=1
#             values.append(k)
        
#         di = dict(zip(keys,values))
#         print(di)      

import re

one = "1234567891011"
two = "1234-567891011"
three = "12345-678-91011"
four = "12345-678-910-11"
five = "123-45-678-910-11"
six = "1234-------------"
seven = "9780306406158"
eight = "978048665088"
nine = "97801311036270"
ten = "9780X86650883"
eleven = "0000000000000"
"""
ダメだったやつ
0000000000000
97801311036270
9780306406158
"""

# pattern1 = r"[\d-]{13,17}"
pattern1 = r"978[\d-]{10,14}"
pattern2 = r"[-]{5,}"

i = 0
len_7 = len(seven)
while i <= len_7:
    "keta" + f"{i}" = 
    i += 1

print(f"{pattern1}")
print(f"{one}")
print(re.fullmatch(pattern1,one))
print(f"{two}")
print(re.fullmatch(pattern1,two))
print(f"{three}")
print(re.fullmatch(pattern1,three))
print(f"{four}")
print(re.fullmatch(pattern1,four))
print(f"{five}")
print(re.fullmatch(pattern1,five))
print(f"{six}")
print(re.fullmatch(pattern1,six))
print(f"{seven}")
print(re.fullmatch(pattern1,seven))
print(f"{eight}")
print(re.fullmatch(pattern1,eight))
print(f"{nine}")
print(re.fullmatch(pattern1,nine))
print(f"{ten}")
print(re.fullmatch(pattern1,ten))
print(f"{eleven}")
print(re.fullmatch(pattern1,eleven))

# print(f"{pattern2}")
# print(f"{one}")
# print(re.fullmatch(pattern2,one))
# print(f"{two}")
# print(re.fullmatch(pattern2,two))
# print(f"{three}")
# print(re.fullmatch(pattern2,three))
# print(f"{four}")
# print(re.fullmatch(pattern2,four))
# print(f"{five}")
# print(re.fullmatch(pattern2,five))
# print(f"{six}")
# print(re.fullmatch(pattern2,six))

count1 = one.count('-')
count2 = two.count('-')
count3 = three.count('-')
count4 = four.count('-')
count5 = five.count('-')
count6 = six.count('-')
count7 = seven.count('-')
count8 = eight.count('-')
count9 = nine.count('-')
count10 = ten.count('-')
count11 = eleven.count('-')



print(f"{one}")
if count1 >= 5:
    print("-が多い")
print(f"{two}")
if count2 >= 5:
    print("-が多い")
print(f"{three}")
if count3 >= 5:
    print("-が多い")
print(f"{four}")
if count4 >= 5:
    print("-が多い")
print(f"{five}")
if count5 >= 5:
    print("-が多い")
print(f"{six}")
if count6 >= 5:
    print("-が多い")
print(f"{seven}")
if count7 >= 5:
    print("-が多い")
print(f"{eight}")
if count8 >= 5:
    print("-が多い")
print(f"{nine}")
if count9 >= 5:
    print("-が多い")
print(f"{ten}")
if count10 >= 5:
    print("-が多い")
print(f"{eleven}")
if count11 >= 5:
    print("-が多い")

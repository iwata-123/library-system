from flask import Flask,render_template,request,jsonify
import main
import json
import sqlite3
import re
import json
import requests

def datapost():
    if request.method == 'POST':
        id = request.form["id"]
        name = request.form["name"]
        author = request.form["author"]
        publisher = request.form["publisher"]
        isbn = request.form["isbn"]

    return id,name,author,publisher,isbn

def staff_datapost():
    if request.method == 'POST':
        id = request.form["id"]
        name = request.form["name"]
        author = request.form["author"]
        publisher = request.form["publisher"]
        isbn = request.form["isbn"]
        kashidashi = request.form.get("kashidashi")
        if kashidashi:
            kashidashi = int(kashidashi)
        kinsho = request.form.get("kinsho")
        if kinsho:
            kinsho = int(kinsho)
        yoyaku = request.form.get("yoyaku")
        if yoyaku:
            yoyaku = int(yoyaku)
            

    return id,name,author,publisher,isbn,kashidashi,kinsho,yoyaku


app = Flask(__name__)

#index.html
@app.route("/")
def index():
    main.maketable()
    main.pre_tsuika()
    return render_template("index.html")

#user.html
@app.route("/user")
def user():
    return render_template("user/user.html")

#staff.html
@app.route("/staff")
def staff():
    return render_template("staff/staff.html")



@app.route("/yoyaku/<btitle>", methods=["GET", "POST"])
def yoyaku(btitle):
    cnt = 1
    #タイトルをもとにyoyakuを取得
    with sqlite3.connect('lib_sys.db') as conn:
        cur = conn.cursor()
        cur.execute(
                        """
                        SELECT id FROM name WHERE name = ?
                        """,(f"{btitle}",)
                        )
        conn.commit()
        s_id = cur.fetchone()
        s_id = s_id[0]

        cur.execute(
                        """
                        SELECT yoyaku FROM zosho WHERE id = ?
                        """,(f"{s_id}",)
                        )
        conn.commit()
        yoyaku = cur.fetchone()
        yoyaku = yoyaku[0]
    #予約件数の更新
        cur.execute(
                        """
                        UPDATE zosho SET yoyaku = ? WHERE id = ?
                        """,(cnt + yoyaku,f"{s_id}")
                        )
        conn.commit()

    return render_template("user/yoyaku.html",cnt = cnt)

#staff.html
@app.route("/base/<btitle>")
def base(btitle):
    #初期化
    s_id = ""
    s_name = ""
    s_author = ""
    s_publisher = ""
    s_isbn = ""
    s_kashikari = ""
    s_yoyaku = ""

    with sqlite3.connect('lib_sys.db') as conn:
        print("今")
        print(btitle)
        #クリックした本のタイトルを取得
        cur = conn.cursor()
        cur.execute(
                        """
                        SELECT
                            *  
                        FROM
                            name
                        WHERE
                            name = ?  
                        """,(f"{btitle}",)
                        )
                        
        conn.commit()
        rows = cur.fetchall()
        print("今")
        print(rows)
        #authorの取得
        for row in rows:
            s_id = row[0]
            s_name = row[1]

        cur.execute(
                        """
                        SELECT
                            *  
                        FROM
                            author
                        WHERE
                            id = ?  
                        """,(f"{s_id}",)
                        )
                        
        conn.commit()
        rows = cur.fetchall()
        #publisherの取得
        for row in rows:
            s_author = row[1]
        cur.execute(
                        """
                        SELECT
                            *  
                        FROM
                            publisher
                        WHERE
                            id = ?  
                        """,(f"{s_id}",)
                        )      
        conn.commit()
        rows = cur.fetchall()
        for row in rows:
            s_publisher = row[1]

        #idの取得
        cur.execute(
                        """
                        SELECT
                            *  
                        FROM
                            zosho
                        WHERE
                            id = ?  
                        """,(f"{s_id}",)
                        )
        conn.commit()
        rows = cur.fetchall()
        
        for row in rows:
            print(row)
            s_isbn = row[4]
            s_kashikari = row[5]
            s_yoyaku = row[7]

    return render_template("user/base.html",base_title = s_name,title = s_name,author = s_author,publisher = s_publisher,isbn = s_isbn,kashikari = s_kashikari,yoyaku = s_yoyaku)

#search.html
@app.route("/base_staff_search/<btitle>")
def base_staff_search(btitle):
    s_name = ""
    s_author = ""
    s_publisher = ""
    s_isbn = ""
    s_kashikari = ""
    s_yoyaku = ""

    with sqlite3.connect('lib_sys.db') as conn:
        cur = conn.cursor()
        cur.execute(
                        """
                        SELECT
                            * 
                        FROM
                            zosho
                        WHERE
                            name = ?  
                        """,(f"{btitle}",)
                        )
        conn.commit()
        rows = cur.fetchall()

        for row in rows:
            s_name = row[1]
            s_author = row[2]
            s_publisher = row[3]
            s_isbn = row[4]
            s_kashikari = row[5]
            s_yoyaku = row[6]

    return render_template("staff/base_staff_search.html",base_title = s_name,title = s_name,author = s_author,publisher = s_publisher,isbn = s_isbn,kashikari = s_kashikari,yoyaku = s_yoyaku)

#staff_search_result.html
@app.route("/staff_search_result", methods=["GET", "POST"])
def staff_search_result():
    id,name,author,publisher,isbn,kashidashi,kinsho,yoyaku = staff_datapost()
    rows = main.search_8(id,name,author,publisher,isbn,kashidashi,kinsho,yoyaku)
    return render_template("staff/staff_search_result.html",rows = rows)

@app.route("/search_result", methods=["GET", "POST"])
def search_result():
    id,name,author,publisher,isbn = datapost()
#??????????????????????????????????????????????????????????????????????
    pattern = r"\d{3}+-[0-9\-]{9}+-\d{1}"
    re.search(pattern,isbn)
    rows = main.search_5(id,name,author,publisher,isbn)
    return render_template("user/search_result.html",rows=rows)

#staff_search.html
@app.route("/staff_search")
def staff_search():
    return render_template("staff/staff_search.html")

#search.html
@app.route("/search")
def search():
    return render_template("user/search.html")

#####################################################################################

#######################################################################################

#staff.html
@app.route("/kashi",methods=["GET", "POST"])
def kashi():
    return render_template("staff/kashikari/kashi.html")

@app.route('/api/data',methods=["GET", "POST"])
def get_data():
    # ここにPythonの処理を書く
    d = {}
    name_data = []
    isbn_data = []
    index = 0
    keys = []
    values = []
    isbn = ""
    try:
        isbndata = request.get_json()
        print("＃")
        print(isbndata)
        isbn = isbndata.get("number")
        print("＃")
        print(type(isbn))
        print("＃")
        print(isbn)
        isbn += '%'
        with sqlite3.connect('lib_sys.db') as conn:
            cur = conn.cursor()
            cur.execute("""
                        SELECT name_id,isbn
                        FROM zosho
                        WHERE isbn 
                        LIKE ?;
                        """,(f"{isbn}",)
                        )
            conn.commit()
            data = cur.fetchall()
            print(data)
            # [(1, '978-9-87-654321-0'), (3, '978-1-99-443210-7'), (5, '978-3-61-559004-9'), (7, '978-8-02-199873-4'), (9, '978-6-14-770045-1')]
            for name_id in data:
                print(name_id)
                _ = name_id[:1]
                print(_)
                name_data.append(_)
                print(name_data)
            print(name_data)            
            for d_isbn in data:
                x = d_isbn[1:2]
                x = x[0]
                isbn_data.append(x)
                print(isbn_data)
            print(isbn_data)
            print(name_data)
            for namae in name_data:
                print(namae)
                namae = namae[0]
                cur.execute("""
                            SELECT name
                            FROM name
                            WHERE id = ?
                            """,(f"{namae}",)
                            )
                conn.commit()
                kouho = cur.fetchall()
                print(kouho)
                # kouho = kouho[0]
                # kouho = kouho[0]
                print("今２")
                print(kouho)
                values.append(kouho)
            print(values)
            # v_len = len(values)
            # print("今")
            # print(v_len)
            # str_list = range(v_len)
            # print(str_list)
            # keys = list(map(str,str_list))
            # print(keys)
            di = dict(zip(isbn_data,values))
            print(di)
            print("今")
            print(jsonify(di))
            return jsonify(di)
    except Exception as e:
        d = str(e)
        print(f"例外クラス: {e.__class__.__name__}")
        print(f"エラーメッセージ: {e}")
        print("!2")
        return jsonify(d)

@app.route("/kashi_kakunin",methods=["GET", "POST"])
def kashi_kakunin():
    isbn = request.form["isbn"]
    with sqlite3.connect('lib_sys.db') as conn:
        cur = conn.cursor()
        cur.execute(
                    """
                    SELECT kashidashi
                    FROM zosho
                    WHERE isbn = ?
                    """,(f"{isbn}",)
                    )
        conn.commit()
        flg = cur.fetchall()
        cur.execute(
                    """
                    SELECT kinsho
                    FROM zosho
                    WHERE isbn = ?
                    """,(f"{isbn}",)
                    )
        conn.commit()
        k_flg = cur.fetchall()
        print("今")
        print(k_flg)
        if k_flg == [(1,)]:
            return render_template("staff/kashikari/kashi.html",k_check = "禁書です",erflg = 2)
        if flg == []:
            return render_template("staff/kashikari/kashi.html",check = "蔵書にありません",erflg = 0)
        if flg == [(1,)]:
            return render_template("staff/kashikari/kashi.html",check = "貸出済みです",erflg = 1)
        if flg != []:
            cur.execute(
                        """
                        UPDATE zosho SET kashidashi = ? WHERE isbn = ?
                        """,(1,f"{isbn}")
                        )
            conn.commit()
            return render_template("staff/kashikari/kashi_kakunin.html")


@app.route("/henkyaku_kakunin",methods=["GET", "POST"])
def henkyaku_kakunin():
    isbn = request.form["isbn"]
    with sqlite3.connect('lib_sys.db') as conn:
        cur = conn.cursor()
        cur.execute(
                    """
                    SELECT kashidashi
                    FROM zosho
                    WHERE isbn = ?
                    """,(f"{isbn}",)
                    )
        conn.commit()
        flg = cur.fetchall()
        if flg == [(0,)]:
            return render_template("staff/kashikari/henkyaku.html",check = "返却済みです",erflg = 1)
        if flg == []:
            return render_template("staff/kashikari/henkyaku.html",check = "蔵書にありません",erflg = 0)
        if flg != []:
            cur.execute(
                        """
                        UPDATE zosho SET kashidashi = ? WHERE isbn = ?
                        """,(0,f"{isbn}")
                        )
            conn.commit()
            return render_template("staff/kashikari/henkyaku_kakunin.html")


@app.route("/henkyaku")
def henkyaku():
    return render_template("staff/kashikari/henkyaku.html")






#staff.html
@app.route("/kaihatsu")
def kaihatsu():
    return render_template("staff/kaihatsu/kaihatsu.html")




#全部入力しないと動かないようにする
@app.route("/kaihatsu_tsuika")
def kaihatsu_tsuika():
    return render_template("staff/kaihatsu/kaihatsu_tsuika.html")


@app.route("/tsuika_kakunin", methods=["GET", "POST"])
def tsuika_kakunin():
    if request.method == 'POST':
        name = request.form["name"]
        author = request.form["author"]
        publisher = request.form["publisher"]
        isbn = request.form["isbn"]
        flg = main.d_tsuika(name,author,publisher,isbn)
        if flg == 1:
            return render_template("staff/kaihatsu/kaihatsu_tsuika.html",flg = flg)
    main.hyozi()

    return render_template("staff/kaihatsu/tsuika_kakunin.html")

@app.route("/kaihatsu_sakuzyo")
def kaihatsu_sakuzyo():
    return render_template("staff/kaihatsu/kaihatsu_sakuzyo.html")

@app.route("/sakuzyo_kakunin", methods=["GET", "POST"])
def sakuzyo_kakunin():
    if request.method == 'POST':
        isbn = request.form["isbn"]
    rtn = main.d_sakuzyo(isbn)
    if rtn == 0:
        return render_template("staff/kaihatsu/kaihatsu_sakuzyo.html",msg="蔵書にありません",erflg=0)
    main.hyozi()

    return render_template("staff/kaihatsu/sakuzyo_kakunin.html")


@app.route("/kaihatsu_koushin")
def kaihatsu_koushin():
    
    return render_template("staff/kaihatsu/kaihatsu_koushin.html")

@app.route("/koushin_kakunin", methods=["GET", "POST"])
def koushin_kakunin():
    if request.method == 'POST':
        id = request.form["id"]
        name = request.form["name"]
        author = request.form["author"]
        publisher = request.form["publisher"]
        isbn = request.form["isbn"]
        kashidashi = request.form["kashidashi"]
        kinsho = request.form["kinsho"]
        yoyaku =request.form["yoyaku"]
        main.d_koushin(id,name,author,publisher,isbn,kashidashi,kinsho,yoyaku)
    main.hyozi()
    return render_template("staff/kaihatsu/koushin_kakunin.html")


@app.route("/kaihatsu_kinsho")
def kaihatsu_kinsho():
    return render_template("staff/kaihatsu/kaihatsu_kinsho.html")

@app.route("/kinsho_kakunin", methods=["GET", "POST"])
def kinsho_kakunin():
    isbn = request.form["isbn"]
    with sqlite3.connect('lib_sys.db') as conn:
        cur = conn.cursor()
        cur.execute(
                    """
                    SELECT kinsho
                    FROM zosho
                    WHERE isbn = ?
                    """,(f"{isbn}",)
                    )
        conn.commit()
        rows = cur.fetchall()
        print(rows)
        #必要な成分だけ取り出す
        if rows == []:
            return render_template("staff/kaihatsu/kaihatsu_kinsho.html",rows=rows,z_check="蔵書にありません")
        rows = rows[0]
        rows = rows[0]
        print(rows)
        if rows == 1:
            return render_template("staff/kaihatsu/kaihatsu_kinsho.html",rows=rows,check="禁書登録されてます")

    main.d_kinsho(isbn)
    main.hyozi()
    
    return render_template("staff/kaihatsu/kinsho_kakunin.html")

@app.route("/kaihatsu_kinsho_kaizyo", methods=["GET", "POST"])
def kaihatsu_kinsho_kaizyo():

    return render_template("staff/kaihatsu/kaihatsu_kinsho_kaizyo.html")

@app.route("/kaizyo_kakunin", methods=["GET", "POST"])
def kaizyo_kakunin():
    isbn = request.form["isbn"]
    with sqlite3.connect('lib_sys.db') as conn:
        cur = conn.cursor()
        cur.execute(
                    """
                    SELECT kinsho
                    FROM zosho
                    WHERE isbn = ?
                    """,(f"{isbn}",)
                    )
        conn.commit()
        rows = cur.fetchall()
        print("今")
        print(rows)
        #必要な成分だけ取り出す
        if rows == []:
            return render_template("staff/kaihatsu/kaizyo_kakunin.html",rows=rows,z_check="蔵書にありません")
        rows = rows[0]
        rows = rows[0]
        print(rows)
        if rows == 0:
            return render_template("staff/kaihatsu/kaizyo_kakunin.html",rows=rows,check="禁書解除されてます")

    main.d_kinsho_kaizyo(isbn)
    main.hyozi()
    

    return render_template("staff/kaihatsu/kaizyo_kakunin.html")


if __name__ == "__main__":
    app.run(debug=True)
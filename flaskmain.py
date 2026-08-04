from flask import Flask,render_template,request,jsonify,session,redirect, url_for
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
import main
import sqlite3
import re
import json
import requests
import tsuika
from dotenv import load_dotenv
import os
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash

db = SQLAlchemy()

app = Flask(__name__)

load_dotenv()
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


# ユーザークラスを作成します（IDだけ使うシンプルな例）
class User(db.Model, UserMixin):
    id = db.Column(
        db.Integer,
        primary_key=True
    )

    username = db.Column(
        db.String(50),
        unique=True,
        nullable=False
    )

    password_hash = db.Column(
        db.String(200),
        nullable=False
    )

    role = db.Column(
        db.String(20),
        default="user"
    )

    # Flask-LoginがセッションIDとして使用するため、必ず文字列で返す
    def get_id(self):
        return str(self.id)
# ユーザー情報をIDから取得する関数（今はシンプルに戻すだけ）

with app.app_context():
    db.drop_all()
    db.create_all()
    admin = User(
        username="admin",
        password_hash=generate_password_hash("adminpass"),
        role="admin"
    )

    db.session.add(admin)
    db.session.commit()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

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

def huwatto_post():
    if request.method == 'POST':
        content = request.form["content"]
    return content


@app.route("/")
def login():
    main.maketable()
    tsuika.pre_tsuika()

    return render_template("user/login.html")

@app.route("/login", methods=["POST"])
def login_post():

    username = request.form["username"]
    password = request.form["password"]

    user = User.query.filter_by(
        username=username
    ).first()

    if user and check_password_hash(
        user.password_hash,
        password
    ):
        login_user(user)

        if user.role == "admin":
            return render_template("staff/staff.html")

        else:
            return render_template("user/user.html")

@app.route("/user/signup", methods=["GET", "POST"])
def register():

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        password_hash = generate_password_hash(password)

        user = User(
            username=username,
            password_hash=password_hash,
            role="user"
        )

        db.session.add(user)
        db.session.commit()

        return render_template("user/user.html")

    return render_template("user/signup.html")

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return render_template('user/logout.html')


@app.route("/index", methods=["GET", "POST"])
def index():
    return render_template("index.html")

#user.html
@app.route("/user", methods=["GET", "POST"])
def user():
    username = request.form["username"]
    password = request.form["password"]
    if username == "admin" and password == "adminpass":
        return render_template("staff/staff.html")
    return render_template("user/user.html")

#staff.html
@app.route("/staff", methods=["GET", "POST"])
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
            s_isbn = row[4]
            s_kashikari = row[5]
            s_yoyaku = row[7]

        cur.execute(
            """
            SELECT
                textsource
            FROM
                textsource
            WHERE
                id = ?
            """,(f"{s_id}",)
        )
        rows = cur.fetchall()

        rows = rows[0]
        row = rows[0]

        s_naiyou = row

    return render_template("user/base.html",base_title = s_name,title = s_name,author = s_author,publisher = s_publisher,isbn = s_isbn,kashikari = s_kashikari,yoyaku = s_yoyaku,naiyou = s_naiyou)

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
        isbn = isbndata.get("number")
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
            # [(1, '978-9-87-654321-0'), (3, '978-1-99-443210-7'), (5, '978-3-61-559004-9'), (7, '978-8-02-199873-4'), (9, '978-6-14-770045-1')]
            for name_id in data:
                _ = name_id[:1]
                name_data.append(_)
            for d_isbn in data:
                x = d_isbn[1:2]
                x = x[0]
                isbn_data.append(x)
            for namae in name_data:
                namae = namae[0]
                cur.execute("""
                            SELECT name
                            FROM name
                            WHERE id = ?
                            """,(f"{namae}",)
                            )
                conn.commit()
                kouho = cur.fetchall()
                values.append(kouho)
            di = dict(zip(isbn_data,values))
            return jsonify(di)
    except Exception as e:
        d = str(e)
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
        #必要な成分だけ取り出す
        if rows == []:
            return render_template("staff/kaihatsu/kaihatsu_kinsho.html",rows=rows,z_check="蔵書にありません")
        rows = rows[0]
        rows = rows[0]
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
        #必要な成分だけ取り出す
        if rows == []:
            return render_template("staff/kaihatsu/kaizyo_kakunin.html",rows=rows,z_check="蔵書にありません")
        rows = rows[0]
        rows = rows[0]
        if rows == 0:
            return render_template("staff/kaihatsu/kaizyo_kakunin.html",rows=rows,check="禁書解除されてます")

    main.d_kinsho_kaizyo(isbn)
    main.hyozi()
    

    return render_template("staff/kaihatsu/kaizyo_kakunin.html")

@app.route("/huwatto")
def huwatto():
    return render_template("user/huwatto.html")

@app.route("/huwatto_search_result", methods=["GET", "POST"])
def huwatto_search_result():
    text = huwatto_post()
    X_tfidf,content = main.pre_insed_tf_tdf()
    scores = main.insed_tf_tdf(text,X_tfidf,content)
    scores = main.ashikiri(scores)
    rows = main.huwatto(scores)
    return render_template("user/huwatto_search_result.html",rows = rows)


if __name__ == "__main__":
    app.run(debug=True)
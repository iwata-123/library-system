from flask import Flask,render_template,request,jsonify,session,redirect, url_for,abort
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
import main
import sqlite3
import re
import tsuika
from dotenv import load_dotenv
import os
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash,check_password_hash
from functools import wraps

db = SQLAlchemy()

app = Flask(__name__)

# .envをロード
load_dotenv()
# キーの設定
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
# データベースのパスの設定
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
# SQLAlchemy用
db.init_app(app)
# flask_login用
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'



# -------------------------------------------------
# クラス名：User
# 引数　：db.Model（flask_loginを使うために必要）
#        UserMixin（flask_loginを使うために必要）
# 処理の説明
# ユーザーを作るクラス
# -------------------------------------------------
# ユーザークラスの作成
class User(db.Model, UserMixin):
    # idカラムの作成
    id = db.Column(
        db.Integer,
        primary_key=True
    )
    # usernameカラムの作成
    username = db.Column(
        db.String(50),
        unique=True,
        nullable=False
    )
    # password用
    password_hash = db.Column(
        db.String(200),
        nullable=False
    )
    # 権限設定
    role = db.Column(
        db.String(20),
        default="user"
    )

    # Flask-LoginがセッションIDとして使用するため、必ず文字列で返す
    def get_id(self):
        return str(self.id)
# ユーザー情報をIDから取得する関数（今はシンプルに戻すだけ）



#-----------------------------------------------------------------------------
#管理者アカウントの作成
#-----------------------------------------------------------------------------
with app.app_context():
    # 起動時テーブルを削除（開発用）
    db.drop_all()
    # テーブルの作成
    db.create_all()
    # 管理者用モデル
    admin = User(
        username="admin",
        password_hash=generate_password_hash("adminpass"),
        role="admin"
    )
    # 管理者ユーザー保存
    db.session.add(admin)
    db.session.commit()



# -------------------------------------------------
# メソッド名：admin_required
# 引数　：f（受け取る関数）
# 返却値：decorated_function（処理後の関数）
# 処理の説明
# アカウントが管理者でなかったらアクセス禁止にする
# 管理者だったらそのままアクセスを許可する
# -------------------------------------------------
def admin_required(f):
    # 元の関数の名前や説明などの情報を保持
    @wraps(f)
    def decorated_function(*args, **kwargs):

        if current_user.role != "admin":
            # アクセス禁止にする
            abort(403)

        return f(*args, **kwargs)

    return decorated_function



# -------------------------------------------------
# メソッド名：load_user
# 引数　：user_id（検索をかけたいuser_id）
# 返却値：User.query.get(int(user_id))　　　（user_idで検索をかけた結果得られたユーザーアカウント）
# 処理の説明
# ユーザーをロード
# ------------------------------------------------- 
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



# -------------------------------------------------
# メソッド名：datapost
# 引数　：なし
# 返却値：id （書籍ごとに振ってあるid）
#        name（書籍の名前）
#        author（著者の名前）
#        publisher（出版社の名前）
#        isbn（書籍に割り振られた国際規格の番号）
# 処理の説明
# id,name,author,publisher,isbnをhtmlから受け取る
# -------------------------------------------------
def datapost():
    if request.method == 'POST':
        id = request.form["id"]
        name = request.form["name"]
        author = request.form["author"]
        publisher = request.form["publisher"]
        isbn = request.form["isbn"]

    return id,name,author,publisher,isbn



# -------------------------------------------------
# メソッド名：staff_datapost
# 引数　：なし
# 返却値：id（書籍ごとのに振ってあるid）
#        name（書籍の名前）
#        author（著者の名前）
#        publisher（出版社の名前）
#        isbn（書籍に割り振られた国際規格の番号）
#        kashidashi（貸し出しているか判別するフラグ）
#        kinsho（禁書になってるか判断するフラグ）
#        yoyaku（予約されているか判断するフラグ）
# 処理の説明
# id,name,author,publisher,isbn,kashidashi,kinsho,yoyakuをhtmlから受け取る
# -------------------------------------------------
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



# -------------------------------------------------
# メソッド名：huwatto_post
# 引数　：なし
# 返却値：content（検索ワード）
# 処理の説明
# contentをhtmlから受け取る
# -------------------------------------------------
def huwatto_post():
    if request.method == 'POST':
        content = request.form["content"]
    return content



# -------------------------------------------------
# メソッド名：login
# 引数　：なし
# 返却値：render_template("user/login.html")　　　（ログインページの描画）
# 処理の説明
# テーブル追加用
# -------------------------------------------------
@app.route("/")
def login():
    main.maketable()
    tsuika.pre_tsuika()

    return render_template("user/login.html")



# -------------------------------------------------
# メソッド名：login_post
# 引数　：なし
# 返却値：render_template("/user/login.html")　　（ログイン画面へ）
# redirect(url_for("staff"))　　（管理者ホーム画面へ）
# redirect(url_for("user"))　　　（利用者ホーム画面へ）
# render_template("user/login.html",flg=flg)　（ログイン失敗時ログイン画面へ）
# 処理の説明
# 
# -------------------------------------------------
@app.route("/login", methods=["GET", "POST"])
def login_post():
    if request.method == "GET":
        return render_template("/user/login.html")
    flg = 0 
    username = request.form["username"]
    password = request.form["password"]
    # ユーザーネームで検索をかける
    user = User.query.filter_by(
        username=username
    ).first()
    # パスワードとユーザーをチェック
    if user and check_password_hash(
        user.password_hash,
        password
    ):
        login_user(user)
    # 管理者ユーザーだったらこっち
        if user.role == "admin":
            return redirect(url_for("staff"))
    # 利用者ユーザーだったらこっち
        else:
            return redirect(url_for("user"))
    # ログイン失敗なら、ログインページに戻す
    else:
        flg = 1    
    return render_template("user/login.html",flg=flg)



# -------------------------------------------------
# メソッド名：register
# 引数　：なし
# 返却値：render_template("user/login.html")　　　（ログインページを描画）
#       render_template("user/signup.html")　　　（サインアップに失敗したときリダイレクト）
# 処理の説明
# リクエストがポストなら、リクエストを受け取り、ユーザーのアカウントを生成、保存
# -------------------------------------------------
@app.route("/user/signup", methods=["GET", "POST"])
def register():

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        # パスワードの生成
        password_hash = generate_password_hash(password)
        # ユーザーのアカウントを生成
        user = User(
            username=username,
            password_hash=password_hash,
            role="user"
        )
        # 保存
        db.session.add(user)
        db.session.commit()

        return render_template("user/login.html")

    return render_template("user/signup.html")



# -------------------------------------------------
# メソッド名：logout
# 引数　：なし
# 返却値：render_template('user/logout.html')　　　（ログアウトしたときのログアウトと書かれているページを描画）
# 処理の説明
# ログアウト画面を描画
# -------------------------------------------------
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return render_template('user/logout.html')



# -------------------------------------------------
# メソッド名：user
# 引数　：なし
# 返却値：render_template("user/user.html")     （利用者ユーザーのホーム画面を描画）
# 処理の説明
# 利用者ユーザーのホーム画面を描画
# -------------------------------------------------
@app.route("/user")
@login_required
def user():
    return render_template("user/user.html")


# -------------------------------------------------
# メソッド名：staff
# 引数　：なし
# 返却値：render_template("staff/staff.html")　　　（管理者ユーザーのホーム画面を描画）
# 処理の説明
# 利用者ユーザーのホーム画面を描画
# -------------------------------------------------
#管理者ユーザーのホーム画面
@app.route("/staff")
@login_required
@admin_required
def staff():
    return render_template("staff/staff.html")


# -------------------------------------------------
# メソッド名：yoyaku
# 引数　：btitle（予約しようとしている本の名前）
# 返却値：render_template("user/yoyaku.html",cnt = cnt)　　　　（予約確認画面を描画）
# 処理の説明
# タイトルをもとに予約されているか調べ、予約されていなかったら予約フラグを立てる
# -------------------------------------------------
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



# -------------------------------------------------
# メソッド名：base
# 引数　：btitle　　（詳細の見たい本の名前）
# 返却値：render_template("user/base.html",base_title = s_name,
# title = s_name,author = s_author,publisher = s_publisher,
# isbn = s_isbn,kashikari = s_kashikari,yoyaku = s_yoyaku,
# naiyou = s_naiyou)　　　　　　　　　　（利用者用本の詳細ページを描画）
# 処理の説明
# 利用者用本の詳細ページを描画
# -------------------------------------------------
#書籍の詳細ページ
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



# -------------------------------------------------
# メソッド名：base_staff_search
# 引数　：btitle
# 返却値：render_template("staff/base_staff_search.html",
# base_title = s_name,title = s_name,
# author = s_author,publisher = s_publisher,
# isbn = s_isbn,kashikari = s_kashikari,yoyaku = s_yoyaku)　　　　（管理者用本の詳細ページを描画）
# 処理の説明
# 管理者用本の詳細ページを描画
# -------------------------------------------------
@app.route("/base_staff_search/<btitle>")
@login_required
@admin_required
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



# -------------------------------------------------
# メソッド名：staff_search_result
# 引数　：なし
# 返却値：render_template("staff/staff_search_result.html",rows = rows)　　　（管理者用の検索結果ページを生成）
# 処理の説明 
# データを受け取り、検索クエリを実行する
# -------------------------------------------------
@app.route("/staff_search_result", methods=["GET", "POST"])
@login_required
@admin_required
def staff_search_result():
    id,name,author,publisher,isbn,kashidashi,kinsho,yoyaku = staff_datapost()
    rows = main.search_8(id,name,author,publisher,isbn,kashidashi,kinsho,yoyaku)
    return render_template("staff/staff_search_result.html",rows = rows)



# -------------------------------------------------
# メソッド名：search_result
# 引数　：なし
# 返却値：render_template("user/search_result.html",rows=rows)　　　　（利用者側の検索結果ページを描画）
# 処理の説明
# データを受け取り、検索クエリを実行する
# -------------------------------------------------
@app.route("/search_result", methods=["GET", "POST"])
def search_result():
    id,name,author,publisher,isbn = datapost()
    rows = main.search_5(id,name,author,publisher,isbn)
    return render_template("user/search_result.html",rows=rows)



# -------------------------------------------------
# メソッド名：staff_search
# 引数　：なし
# 返却値：render_template("staff/staff_search.html")　　　（管理者側の検索フォームを描画）
# 処理の説明
# 管理者側の検索フォームを描画
# -------------------------------------------------
@app.route("/staff_search")
@login_required
@admin_required
def staff_search():
    return render_template("staff/staff_search.html")



# -------------------------------------------------
# メソッド名：search
# 引数　：なし
# 返却値：render_template("user/search.html")　　　　（利用者側の検索フォームを描画）
# 処理の説明
# 利用者側の検索フォームを描画
# -------------------------------------------------
@app.route("/search")
def search():
    return render_template("user/search.html")



# -------------------------------------------------
# メソッド名：kashi
# 引数　：なし
# 返却値：render_template("staff/kashikari/kashi.html")　　　（貸出画面の描画）
# 処理の説明
# 貸出画面の描画
# -------------------------------------------------
# 本来バーコードで入力すべきですがないので検索して貸出しています
@app.route("/kashi",methods=["GET", "POST"])
def kashi():
    return render_template("staff/kashikari/kashi.html")



# -------------------------------------------------
# メソッド名：get_data
# 引数　：なし
# 返却値：jsonify(di)   （成功時辞書形式を返却）
#         jsonify(d)　　（失敗時エラーを返す）
# 処理の説明
# isbnをjsonで受けとり、部分一致で検索本の名前で検索し直し
# -------------------------------------------------
# 検索候補用api
# isbnで検索
@app.route('/api/data',methods=["GET", "POST"])
def get_data():
    d = {}
    name_data = []
    isbn_data = []
    values = []
    isbn = ""
    try:
        # isbnを受け取る
        isbndata = request.get_json()
        isbn = isbndata.get("number")
        # 検索予測のため部分一致
        isbn += '%'
        # isbnで検索
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
            # 複数検索結果が返ってくる
            # 一件の要素ごとに最初の要素（id）を取り出す
            for name_id in data:
                _ = name_id[:1]
                name_data.append(_)
            # 一件の要素ごとに２番目の要素（isbn）を取り出す
            for d_isbn in data:
                x = d_isbn[1:2]
                x = x[0]
                isbn_data.append(x)
            #idを書名に変換
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
            # 辞書形式にする
            di = dict(zip(isbn_data,values))
            return jsonify(di)
        # エラーが出たらエラーを返す
    except Exception as e:
        d = str(e)
        return jsonify(d)

# -------------------------------------------------
# メソッド名：kashi_kakunin
# 引数　：なし
# 返却値：render_template("staff/kashikari/kashi.html",k_check = "禁書です",erflg = 2)　　　
#        （禁書だったらはじく）
#        render_template("staff/kashikari/kashi.html",check = "蔵書にありません",erflg = 0)
# 　　　　（蔵書だったらはじく）
#         render_template("staff/kashikari/kashi.html",check = "貸出済みです",erflg = 1)
# 　　　　（貸出済みだったらはじく）
#          render_template("staff/kashikari/kashi_kakunin.html")
# 　　　　（成功時確認画面へ）
# 処理の説明
# 貸し出してるか禁書かをチェックしokだったら貸出済みに更新
# -------------------------------------------------
@app.route("/kashi_kakunin",methods=["GET", "POST"])
@login_required
@admin_required
def kashi_kakunin():
    isbn = request.form["isbn"]
    with sqlite3.connect('lib_sys.db') as conn:
        cur = conn.cursor()
        # 貸し出しているかチェック
        cur.execute(
                    """
                    SELECT kashidashi
                    FROM zosho
                    WHERE isbn = ?
                    """,(f"{isbn}",)
                    )
        conn.commit()
        flg = cur.fetchall()
        # 禁書になってるかチェック
        cur.execute(
                    """
                    SELECT kinsho
                    FROM zosho
                    WHERE isbn = ?
                    """,(f"{isbn}",)
                    )
        conn.commit()
        k_flg = cur.fetchall()
        # 禁書だったら表示
        if k_flg == [(1,)]:
            return render_template("staff/kashikari/kashi.html",k_check = "禁書です",erflg = 2)
        # 蔵書になかったら表示
        if flg == []:
            return render_template("staff/kashikari/kashi.html",check = "蔵書にありません",erflg = 0)
        # 貸出済みなら表示
        if flg == [(1,)]:
            return render_template("staff/kashikari/kashi.html",check = "貸出済みです",erflg = 1)
        # 貸出済みに更新
        if flg != []:
            cur.execute(
                        """
                        UPDATE zosho SET kashidashi = ? WHERE isbn = ?
                        """,(1,f"{isbn}")
                        )
            conn.commit()
            return render_template("staff/kashikari/kashi_kakunin.html")




# -------------------------------------------------
# メソッド名：henkyaku_kakunin
# 引数　：なし
# 返却値：render_template("staff/kashikari/henkyaku.html",check = "返却済みです",erflg = 1)　　　
#        （返却済みだったらはじく）
#        render_template("staff/kashikari/henkyaku.html",check = "蔵書にありません",erflg = 0)
# 　　　　（蔵書だったらはじく）
#         render_template("staff/kashikari/henkyaku_kakunin.html")
# 　　　　（成功時確認画面へ）
# 処理の説明
# 返却済みか禁書かをチェックしokだったら返却済みに更新
# -------------------------------------------------
# 返却確認用ページ
@app.route("/henkyaku_kakunin",methods=["GET", "POST"])
@login_required
@admin_required
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
            # 返却済みだったら表示
            return render_template("staff/kashikari/henkyaku.html",check = "返却済みです",erflg = 1)
        if flg == []:
            # 蔵書になかったら表示
            return render_template("staff/kashikari/henkyaku.html",check = "蔵書にありません",erflg = 0)
        if flg != []:
            cur.execute(
                        """
                        UPDATE zosho SET kashidashi = ? WHERE isbn = ?
                        """,(0,f"{isbn}")
                        )
            conn.commit()
            return render_template("staff/kashikari/henkyaku_kakunin.html")



# -------------------------------------------------
# メソッド名：henkyaku
# 引数　：なし
# 返却値：render_template("staff/kashikari/henkyaku.html")　　　（返却画面の描画）
# 処理の説明
# 返却画面の描画
# -------------------------------------------------
# 本来バーコードで入力すべきですがないので検索して返却しています
@app.route("/henkyaku")
@login_required
@admin_required
def henkyaku():
    return render_template("staff/kashikari/henkyaku.html")



# -------------------------------------------------
# メソッド名：kaihatsu
# 引数　：なし
# 返却値：render_template("staff/kaihatsu/kaihatsu.html")　　　（管理者モードのホームを描画）
# 処理の説明
# 管理者モードのホームを描画
# -------------------------------------------------
@app.route("/kaihatsu")
@login_required
@admin_required
def kaihatsu():
    return render_template("staff/kaihatsu/kaihatsu.html")



# -------------------------------------------------
# メソッド名：kaihatsu_tsuika
# 引数　：なし
# 返却値：render_template("staff/kaihatsu/kaihatsu_tsuika.html")　　　（書籍の追加ページを描画）
# 処理の説明
# 書籍の追加ページを描画
# -------------------------------------------------
@app.route("/kaihatsu_tsuika")
@login_required
@admin_required
def kaihatsu_tsuika():
    return render_template("staff/kaihatsu/kaihatsu_tsuika.html")



# -------------------------------------------------
# メソッド名：tsuika_kakunin
# 引数　：なし
# 返却値：render_template("staff/kaihatsu/kaihatsu_tsuika.html",flg = flg)　　　（すでにある本だったらはじく）
#        render_template("staff/kaihatsu/tsuika_kakunin.html")　　　　　　（成功時確認画面へ）
# 処理の説明
# データを受けとり、データがあったらはじく、そうでなかったら追加
# -------------------------------------------------
@app.route("/tsuika_kakunin", methods=["GET", "POST"])
@login_required
@admin_required
def tsuika_kakunin():
    if request.method == 'POST':
        name = request.form["name"]
        author = request.form["author"]
        publisher = request.form["publisher"]
        isbn = request.form["isbn"]
        textsource = request.form["textsource"]
        flg = main.d_tsuika(name,author,publisher,isbn,textsource)
        # データがあったらflgは1
        # すでにある本だったらはじく
        if flg == 1:
            return render_template("staff/kaihatsu/kaihatsu_tsuika.html",flg = flg)

    return render_template("staff/kaihatsu/tsuika_kakunin.html")



# -------------------------------------------------
# メソッド名：kaihatsu_sakuzyo
# 引数　：なし
# 返却値：render_template("staff/kaihatsu/kaihatsu_sakuzyo.html")　　（蔵書の削除ページを描画）
# 処理の説明
# 蔵書の削除ページを描画
# -------------------------------------------------
@app.route("/kaihatsu_sakuzyo")
@login_required
@admin_required
def kaihatsu_sakuzyo():
    return render_template("staff/kaihatsu/kaihatsu_sakuzyo.html")



# -------------------------------------------------
# メソッド名：sakuzyo_kakunin
# 引数　：なし
# 返却値：render_template("staff/kaihatsu/kaihatsu_sakuzyo.html",msg="蔵書にありません",erflg=0)  
#        （蔵書になかったらはじく）  
#        render_template("staff/kaihatsu/sakuzyo_kakunin.html")
#　　　　　（成功時確認画面へ）
# 処理の説明
# isbnを受け取り蔵書になかったらはじくあったら確認画面へ
# -------------------------------------------------
@app.route("/sakuzyo_kakunin", methods=["GET", "POST"])
@login_required
@admin_required
def sakuzyo_kakunin():
    if request.method == 'POST':
        isbn = request.form["isbn"]
    rtn = main.d_sakuzyo(isbn)
    if rtn == 0:
        return render_template("staff/kaihatsu/kaihatsu_sakuzyo.html",msg="蔵書にありません",erflg=0)

    return render_template("staff/kaihatsu/sakuzyo_kakunin.html")



# -------------------------------------------------
# メソッド名：kaihatsu_koushin
# 引数　：なし
# 返却値：render_template("staff/kaihatsu/kaihatsu_koushin.html")　　　（蔵書データの更新を描画）
# 処理の説明
# 蔵書データの更新を描画
# -------------------------------------------------
@app.route("/kaihatsu_koushin")
@login_required
@admin_required
def kaihatsu_koushin():
    
    return render_template("staff/kaihatsu/kaihatsu_koushin.html")



# -------------------------------------------------
# メソッド名：koushin_kakunin
# 引数　：なし
# 返却値：render_template("staff/kaihatsu/koushin_kakunin.html")　　（更新確認画面を描画）
# 処理の説明
# データを受け取り更新をかける 
# -------------------------------------------------
@app.route("/koushin_kakunin", methods=["GET", "POST"])
@login_required
@admin_required
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
        textsource = request.form["textsource"]
        main.d_koushin(id,name,author,publisher,isbn,kashidashi,kinsho,yoyaku,textsource)
    return render_template("staff/kaihatsu/koushin_kakunin.html")



# -------------------------------------------------
# メソッド名：kaihatsu_kinsho
# 引数　：なし
# 返却値：render_template("staff/kaihatsu/kaihatsu_kinsho.html")　　（蔵書の禁書指定ページを描画）
# 処理の説明
# 蔵書の禁書指定ページを描画
# -------------------------------------------------
@app.route("/kaihatsu_kinsho")
@login_required
@admin_required
def kaihatsu_kinsho():
    return render_template("staff/kaihatsu/kaihatsu_kinsho.html")



# -------------------------------------------------
# メソッド名：
# 引数　：なし
# 返却値：render_template("staff/kaihatsu/kaihatsu_kinsho.html",rows=rows,z_check="蔵書にありません")
#　　　　（蔵書にないときはじく）
# render_template("staff/kaihatsu/kaihatsu_kinsho.html",rows=rows,check="禁書登録されてます")
#      （禁書に登録されているときはじく）
# render_template("staff/kaihatsu/kinsho_kakunin.html")
#       （成功時確認画面へ）
# 処理の説明
# 蔵書にないとき、禁書登録がされているとき以外は確認画面へ
# -------------------------------------------------
@app.route("/kinsho_kakunin", methods=["GET", "POST"])
@login_required
@admin_required
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
        #蔵書にないときは表示
        if rows == []:
            return render_template("staff/kaihatsu/kaihatsu_kinsho.html",rows=rows,z_check="蔵書にありません")
        rows = rows[0]
        rows = rows[0]
        # 禁書登録が既にされていたら表示
        if rows == 1:
            return render_template("staff/kaihatsu/kaihatsu_kinsho.html",rows=rows,check="禁書登録されてます")

    main.d_kinsho(isbn)
    
    return render_template("staff/kaihatsu/kinsho_kakunin.html")



# -------------------------------------------------
# メソッド名：kaihatsu_kinsho_kaizyo
# 引数　：なし
# 返却値：render_template("staff/kaihatsu/kaihatsu_kinsho_kaizyo.html")
# 　　　　（禁書登録を外すページを生成）
# 処理の説明
# 禁書登録を外すページを生成
# -------------------------------------------------
@app.route("/kaihatsu_kinsho_kaizyo", methods=["GET", "POST"])
@login_required
@admin_required
def kaihatsu_kinsho_kaizyo():

    return render_template("staff/kaihatsu/kaihatsu_kinsho_kaizyo.html")



# -------------------------------------------------
# メソッド名：kaizyo_kakunin
# 引数　：なし
# 返却値：render_template("staff/kaihatsu/kaizyo_kakunin.html",rows=rows,z_check="蔵書にありません")
# 　　　　（蔵書になかったらはじく）
#     render_template("staff/kaihatsu/kaizyo_kakunin.html",rows=rows,check="禁書解除されてます")
# 　　（禁書指定されていたらはじく）
#     render_template("staff/kaihatsu/kaizyo_kakunin.html")
# 　　（もとの画面へ）
# 処理の説明
# 蔵書にないとき、禁書登録がされているとき以外は確認画面へ
# -------------------------------------------------
@app.route("/kaizyo_kakunin", methods=["GET", "POST"])
@login_required
@admin_required
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
        #蔵書になかったら表示
        if rows == []:
            return render_template("staff/kaihatsu/kaizyo_kakunin.html",rows=rows,z_check="蔵書にありません")
        rows = rows[0]
        rows = rows[0]
        # 禁書登録解除されてたら表示
        if rows == 0:
            return render_template("staff/kaihatsu/kaizyo_kakunin.html",rows=rows,check="禁書解除されてます")

    main.d_kinsho_kaizyo(isbn)
    

    return render_template("staff/kaihatsu/kaizyo_kakunin.html")



# -------------------------------------------------
# メソッド名：huwatto
# 引数　：なし
# 返却値：render_template("user/huwatto.html")　　（tf-idfを使った検索フォームを描画）
# 処理の説明
# tf-idfを使った検索フォームを描画
# -------------------------------------------------
@app.route("/huwatto")
def huwatto():
    return render_template("user/huwatto.html")



# -------------------------------------------------
# メソッド名：huwatto_search_result
# 引数　：なし
# 返却値：render_template("user/huwatto_search_result.html",rows = rows)　（tf-idfを使った検索結果を描画）
# 処理の説明
# tf-idfを使った検索結果を描画
# -------------------------------------------------
@app.route("/huwatto_search_result", methods=["GET", "POST"])
def huwatto_search_result():
    # データ受け取り
    text = huwatto_post()
    # tf-idf検索
    X_tfidf,content = main.pre_insed_tf_tdf()
    scores = main.insed_tf_tdf(text,X_tfidf,content)
    # 規定以下の値は削除
    scores = main.ashikiri(scores)
    # 検索をかける
    rows = main.huwatto(scores)
    return render_template("user/huwatto_search_result.html",rows = rows)



# -------------------------------------------------
# メソッド名：account_info
# 引数　：なし
# 返却値：render_template("user/account_info.html",username=username)　　　（アカウントページを描画）
# 処理の説明
# アカウントページを描画
# # -------------------------------------------------
@app.route("/account_info", methods=["GET", "POST"])
@login_required
def account_info():
    username = current_user.username

    return render_template("user/account_info.html",username=username)


if __name__ == "__main__":
    app.run(debug=True)
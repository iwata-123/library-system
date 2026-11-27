import random
import sqlite3
import sys

random.seed(42)
N = 2000  # 生成する蔵書数

# ===== 設定(実際の環境に合わせて変更) =====
DB_PATH = (
    sys.argv[1] if len(sys.argv) > 1 else "lib_sys.db"
)  # SQLiteのDBパス(引数でも指定可)


# テーブル名(実際の名前に合わせて変更してください)
TABLES = {
    "books": "zosho",
    "name": "name",
    "author": "author",
    "publisher": "publisher",
    "textsource": "textsource",
}

GENRES = {
    "技術": {
        "topics": [
            "Python",
            "Java",
            "SQL",
            "Flask",
            "Linux",
            "AWS",
            "機械学習",
            "Webアプリ",
            "アルゴリズム",
            "データ構造",
            "ネットワーク",
            "セキュリティ",
            "Docker",
            "Git",
            "設計",
        ],
        "patterns": [
            "{t}入門",
            "{t}実践ガイド",
            "わかる{t}",
            "{t}の教科書",
            "{t}設計パターン",
            "やさしい{t}",
            "{t}完全マスター",
            "{t}ハンドブック",
        ],
        "words": [
            "コード",
            "実装",
            "開発",
            "サーバー",
            "データベース",
            "テスト",
            "運用",
            "バグ",
            "フレームワーク",
            "API",
            "設計",
            "効率化",
        ],
    },
    "ミステリ": {
        "topics": [
            "密室",
            "殺人",
            "探偵",
            "古い洋館",
            "消えた遺書",
            "雪山の山荘",
            "港町",
            "図書館",
            "双子",
            "暗号",
            "最後の晩餐",
            "時計塔",
        ],
        "patterns": [
            "{t}の謎",
            "{t}事件",
            "{t}殺人事件",
            "{t}の真相",
            "名探偵と{t}",
            "{t}の追憶",
        ],
        "words": [
            "事件",
            "犯人",
            "トリック",
            "証言",
            "アリバイ",
            "推理",
            "刑事",
            "動機",
            "真相",
            "伏線",
        ],
    },
    "SF": {
        "topics": [
            "火星",
            "宇宙船",
            "人工知能",
            "タイムトラベル",
            "未来都市",
            "ロボット",
            "星間戦争",
            "量子",
            "地球最後の日",
            "仮想世界",
            "月面基地",
        ],
        "patterns": [
            "{t}の彼方",
            "{t}年代記",
            "{t}クロニクル",
            "さよなら{t}",
            "{t}の記憶",
            "{t}戦記",
        ],
        "words": [
            "未来",
            "宇宙",
            "技術",
            "文明",
            "人類",
            "実験",
            "異星",
            "時間",
            "世界",
            "記憶",
        ],
    },
    "歴史": {
        "topics": [
            "戦国",
            "江戸",
            "明治維新",
            "平安",
            "鎌倉",
            "古代ローマ",
            "大航海時代",
            "幕末",
            "シルクロード",
            "縄文",
            "室町",
            "第二次世界大戦",
        ],
        "patterns": [
            "{t}の歴史",
            "{t}の人々",
            "図説{t}",
            "{t}を読み解く",
            "{t}の真実",
            "{t}史入門",
        ],
        "words": [
            "歴史",
            "文化",
            "戦い",
            "政治",
            "時代",
            "人物",
            "社会",
            "資料",
            "世界",
            "日本",
            "設計",
        ],
    },
    "料理": {
        "topics": [
            "和食",
            "パスタ",
            "カレー",
            "パン",
            "スイーツ",
            "発酵食品",
            "お弁当",
            "中華",
            "野菜",
            "魚料理",
            "スープ",
            "家庭料理",
        ],
        "patterns": [
            "{t}レシピ",
            "毎日の{t}",
            "{t}のきほん",
            "プロが教える{t}",
            "{t}100選",
            "かんたん{t}",
        ],
        "words": [
            "レシピ",
            "調味料",
            "食材",
            "時短",
            "下ごしらえ",
            "味付け",
            "旬",
            "健康",
            "家庭",
            "献立",
        ],
    },
    "科学": {
        "topics": [
            "物理学",
            "宇宙",
            "生物",
            "化学",
            "数学",
            "脳",
            "遺伝子",
            "地球",
            "量子力学",
            "進化",
            "素粒子",
            "気象",
        ],
        "patterns": [
            "{t}の世界",
            "{t}はなぜ面白いのか",
            "{t}入門",
            "ゼロからわかる{t}",
            "{t}の謎",
            "{t}図鑑",
        ],
        "words": [
            "理論",
            "実験",
            "法則",
            "発見",
            "宇宙",
            "研究",
            "世界",
            "仕組み",
            "数式",
            "観測",
            "設計",
        ],
    },
    "ビジネス": {
        "topics": [
            "マーケティング",
            "リーダーシップ",
            "営業",
            "起業",
            "マネジメント",
            "交渉術",
            "時間管理",
            "プレゼン",
            "チームづくり",
            "経営戦略",
            "働き方",
        ],
        "patterns": [
            "{t}の教科書",
            "{t}の技術",
            "{t}大全",
            "成功する{t}",
            "{t}の習慣",
            "{t}入門",
        ],
        "words": [
            "仕事",
            "成果",
            "戦略",
            "組織",
            "顧客",
            "習慣",
            "効率化",
            "目標",
            "会社",
            "設計",
            "人生",
        ],
    },
    "健康": {
        "topics": [
            "睡眠",
            "ストレッチ",
            "栄養",
            "ランニング",
            "メンタル",
            "ダイエット",
            "腸活",
            "姿勢",
            "ヨガ",
            "瞑想",
            "筋トレ",
        ],
        "patterns": [
            "{t}の科学",
            "{t}のすすめ",
            "今日からできる{t}",
            "{t}習慣",
            "{t}大全",
            "{t}の教科書",
        ],
        "words": [
            "健康",
            "体",
            "習慣",
            "運動",
            "食事",
            "回復",
            "予防",
            "心",
            "生活",
            "人生",
        ],
    },
    "旅行": {
        "topics": [
            "京都",
            "北海道",
            "沖縄",
            "ヨーロッパ",
            "東南アジア",
            "温泉",
            "四国",
            "ニューヨーク",
            "パリ",
            "ひとり旅",
            "世界遺産",
        ],
        "patterns": [
            "{t}を歩く",
            "{t}ガイド",
            "{t}の旅",
            "大人の{t}",
            "{t}さんぽ",
            "まるごと{t}",
        ],
        "words": [
            "観光",
            "名所",
            "宿",
            "グルメ",
            "交通",
            "季節",
            "歴史",
            "文化",
            "写真",
            "世界",
            "日本",
        ],
    },
    "経済": {
        "topics": [
            "株式投資",
            "金融",
            "円安",
            "年金",
            "貿易",
            "インフレ",
            "仮想通貨",
            "家計",
            "資産運用",
            "税金",
            "日本経済",
        ],
        "patterns": [
            "{t}の教科書",
            "{t}入門",
            "{t}のしくみ",
            "図解{t}",
            "{t}で読む世界",
            "{t}の未来",
        ],
        "words": [
            "お金",
            "市場",
            "政策",
            "投資",
            "景気",
            "リスク",
            "社会",
            "世界",
            "日本",
            "設計",
            "歴史",
        ],
    },
    "教育": {
        "topics": [
            "学習法",
            "英語",
            "子育て",
            "読書",
            "算数",
            "受験",
            "プログラミング教育",
            "記憶術",
            "勉強",
            "作文",
            "国語",
        ],
        "patterns": [
            "{t}のコツ",
            "{t}の教科書",
            "{t}入門",
            "伸びる{t}",
            "{t}ドリル",
            "{t}大全",
        ],
        "words": [
            "学習",
            "子ども",
            "先生",
            "試験",
            "習慣",
            "理解",
            "記憶",
            "教室",
            "成長",
            "人生",
        ],
    },
    "芸術": {
        "topics": [
            "印象派",
            "写真",
            "建築",
            "デザイン",
            "音楽",
            "浮世絵",
            "映画",
            "ジャズ",
            "現代アート",
            "彫刻",
            "書道",
        ],
        "patterns": [
            "{t}の世界",
            "{t}入門",
            "{t}を楽しむ",
            "{t}の歴史",
            "{t}の見方",
            "{t}ノート",
        ],
        "words": [
            "作品",
            "美",
            "表現",
            "作家",
            "展覧会",
            "色",
            "形",
            "鑑賞",
            "文化",
            "歴史",
            "設計",
        ],
    },
    "小説": {
        "topics": [
            "夏",
            "海辺の町",
            "春の約束",
            "夜行列車",
            "手紙",
            "桜",
            "雨の日",
            "古書店",
            "約束の場所",
            "秋の終わり",
            "放課後",
        ],
        "patterns": [
            "{t}の記憶",
            "{t}のあとで",
            "{t}に降る雪",
            "さよなら{t}",
            "{t}物語",
            "{t}をさがして",
        ],
        "words": [
            "家族",
            "恋",
            "旅",
            "友情",
            "別れ",
            "町",
            "記憶",
            "季節",
            "人生",
            "約束",
            "世界",
        ],
    },
}

SURNAMES = [
    "佐藤",
    "鈴木",
    "高橋",
    "田中",
    "伊藤",
    "渡辺",
    "山本",
    "中村",
    "小林",
    "加藤",
    "吉田",
    "山田",
    "佐々木",
    "山口",
    "松本",
    "井上",
    "木村",
    "林",
    "斎藤",
    "清水",
    "山崎",
    "森",
    "池田",
    "橋本",
    "阿部",
    "石川",
    "山下",
    "中島",
    "前田",
    "藤田",
    "小川",
    "後藤",
    "岡田",
    "長谷川",
    "村上",
    "近藤",
    "石井",
    "坂本",
    "遠藤",
    "青木",
]
GIVEN = [
    "太郎",
    "花子",
    "健一",
    "美咲",
    "大輔",
    "由美",
    "翔太",
    "陽子",
    "直樹",
    "愛",
    "拓也",
    "恵",
    "和也",
    "真理",
    "隆",
    "彩",
    "誠",
    "優子",
    "学",
    "麻衣",
    "剛",
    "裕子",
    "雅人",
    "千尋",
    "亮",
    "沙織",
    "浩二",
    "遥",
    "修",
    "舞",
    "啓介",
    "奈々",
    "智也",
    "香織",
    "悠斗",
    "瞳",
    "勇気",
    "咲",
    "康介",
    "葵",
]
PUBLISHERS = [
    "青葉書房",
    "月影出版",
    "北斗社",
    "朝霧書院",
    "星海社",
    "白鷺堂",
    "緑風館",
    "明星出版",
    "桜庭書店",
    "雲母書房",
    "蒼天社",
    "銀杏出版",
    "彩雲堂",
    "浪漫書房",
    "旭日出版",
    "紫苑社",
    "東雲書院",
    "瑞穂出版",
    "琥珀堂",
    "若草書房",
    "天城社",
    "波音出版",
    "風待書房",
    "灯台社",
    "木漏れ日出版",
    "夕凪書院",
    "常盤堂",
    "霞ヶ関出版",
    "千草書房",
    "鳳凰社",
]

# 紹介文は「導入 + 本文 + 結び」を組み合わせて作る(本ごとに文章が変わる)
INTRO = [
    "本書は{t}について、{w1}や{w2}を中心にわかりやすく解説する一冊。",
    "{t}をテーマに、{w1}と{w2}の関係を丁寧に描く。",
    "{w1}を軸に{t}を掘り下げる、読み応えのある一冊。",
    "{t}にまつわる{w1}と{w2}を、豊富な例で紹介する。",
    "{t}の魅力を、{w1}という切り口から語り尽くす。",
    "いま注目される{t}を、{w1}と{w2}の両面から捉え直す。",
    "{t}とは何か。{w1}の視点から基本を整理する。",
    "著者が長年向き合ってきた{t}について、{w1}を交えて綴る。",
    "{t}を初めて学ぶ人のために、{w1}から順に説明する。",
    "{t}の現場で見えてきた{w1}と{w2}の本質に迫る。",
    "{w1}と{w2}、この二つから{t}の全体像が見えてくる。",
    "{t}をめぐる{w1}の変遷を、最新の話題とともにたどる。",
]
BODY = [
    "{w3}にも触れ、読み終えた後に新しい発見がある。",
    "{w2}や{w3}といった身近な話題から入るので、初めての人でも読み進められる。",
    "{w3}についての章も収録している。",
    "図や具体例を多く用い、{w3}まで一気に理解できる構成。",
    "{w2}の考え方を押さえたうえで、{w3}へと話を広げていく。",
    "各章の終わりに{w3}に関する問いを用意し、理解を確かめられる。",
    "{w3}をめぐる意外な事実も紹介し、読み物としても楽しめる。",
    "{w2}の基本から{w3}の応用まで、段階的に学べる。",
    "コラムでは{w3}にまつわるエピソードを取り上げる。",
    "{w2}を深く知ることで、{w3}の見え方が変わってくる。",
    "実例をもとに{w2}を検証し、{w3}との違いを明らかにする。",
    "専門用語はやさしく言い換え、{w3}の話題も無理なく読める。",
    "{w2}についての誤解を解きほぐし、{w3}への理解を深める。",
    "身近な{w3}を題材に、{w2}の仕組みを解きほぐす。",
]
CLOSING = [
    "最初の一冊として最適。",
    "手元に置いておきたい一冊。",
    "読み終えたとき、世界の見え方が少し変わる。",
    "忙しい人にも読みやすい、コンパクトな構成。",
    "何度でも読み返したくなる一冊。",
    "{t}を知りたい全ての人におすすめ。",
    "学生から社会人まで、幅広い読者に向けて書かれている。",
    "巻末には{w1}に関する用語集つき。",
    "新しい視点を求める人にこそ読んでほしい。",
    "日々の暮らしにも役立つヒントが満載。",
    "ページをめくるたびに新しい気づきがある。",
    "{w1}が好きな人も、そうでない人も楽しめる。",
]

FORMAT_TWEAKS = {"入門": "にゅうもん", "Python": "パイソン", "Java": "ジャバ"}


def make_title(genre, used):
    g = GENRES[genre]
    t = random.choice(g["topics"])
    title = random.choice(g["patterns"]).format(t=t)
    base = title
    n = 1
    while title in used:
        n += 1
        title = (
            random.choice(
                [
                    f"{base} 第{n}版",
                    f"{base}(改訂版)",
                    f"{base} 上",
                    f"{base} 下",
                    f"{base} {n}",
                    f"続・{base}",
                ]
            )
            if n < 6
            else f"{base} vol.{n}"
        )
    used.add(title)
    return title, t


def make_text(genre, topic, used_texts):
    g = GENRES[genre]
    # 他ジャンルの語も少し混ぜて、ジャンルをまたぐ検索ヒットを作る
    for _ in range(1000):
        pool = g["words"] + [
            random.choice(GENRES[random.choice(list(GENRES))]["words"])
        ]
        w1, w2, w3 = random.sample(pool, 3)
        parts = [random.choice(INTRO), random.choice(BODY)]
        if random.random() < 0.7:
            parts.append(random.choice(CLOSING))
        text = "".join(parts).format(t=topic, w1=w1, w2=w2, w3=w3)
        if text not in used_texts:  # 他の本と同じ文章は使わない
            used_texts.add(text)
            return text
    raise RuntimeError("重複しない紹介文を作れませんでした(パーツを増やしてください)")


def isbn13(i):
    # 978-4-0xxxxxxx の連番(チェックディジット付き)
    body = "9784" + str(i).zfill(8)  # 12桁
    s = sum(int(c) * (1 if k % 2 == 0 else 3) for k, c in enumerate(body))
    check = (10 - s % 10) % 10
    return body + str(check)


def sql_str(s):
    return "'" + s.replace("'", "''") + "'"


def main():
    genre_names = list(GENRES)
    used = set()
    used_texts = set()
    names, authors, publishers, texts, books = [], [], [], [], []
    for i in range(1, N + 1):
        genre = random.choice(genre_names)
        title, topic = make_title(genre, used)
        names.append((i, title))
        authors.append((i, random.choice(SURNAMES) + " " + random.choice(GIVEN)))
        publishers.append((i, random.choice(PUBLISHERS)))
        texts.append((i, make_text(genre, topic, used_texts)))
        books.append((i, i, i, i, i, isbn13(i), 0, 0, 0))

    conn = sqlite3.connect(DB_PATH)
    try:
        cur = conn.cursor()
        # 毎回テーブルをDROPして作り直す
        for t in TABLES.values():
            cur.execute(f"DROP TABLE IF EXISTS {t}")
        cur.execute(f"""CREATE TABLE {TABLES['name']} (
            id INTEGER PRIMARY KEY, name TEXT NOT NULL)""")
        cur.execute(f"""CREATE TABLE {TABLES['author']} (
            id INTEGER PRIMARY KEY, author TEXT NOT NULL)""")
        cur.execute(f"""CREATE TABLE {TABLES['publisher']} (
            id INTEGER PRIMARY KEY, publisher TEXT NOT NULL)""")
        cur.execute(f"""CREATE TABLE {TABLES['textsource']} (
            id INTEGER PRIMARY KEY, textsource TEXT NOT NULL)""")
        cur.execute(f"""CREATE TABLE {TABLES['books']} (
            id INTEGER, name_id INTEGER, author_id INTEGER, publisher_id INTEGER,
            textsource_id INTEGER, isbn TEXT NOT NULL,
            kashidashi INTEGER, kinsho INTEGER, yoyaku INTEGER)""")
        for key, col, rows in [
            ("name", "name", names),
            ("author", "author", authors),
            ("publisher", "publisher", publishers),
            ("textsource", "textsource", texts),
        ]:
            cur.executemany(
                f"INSERT INTO {TABLES[key]} (id, {col}) VALUES (?, ?)", rows
            )
            print(f"{TABLES[key]}: {len(rows)}件")
        cur.executemany(
            f"INSERT INTO {TABLES['books']} (id, name_id, author_id, publisher_id, textsource_id, "
            f"isbn, kashidashi, kinsho, yoyaku) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            books,
        )
        print(f"{TABLES['books']}: {len(books)}件")
        conn.commit()
    except Exception:
        conn.rollback()  # 失敗したら全部取り消し
        raise
    finally:
        conn.close()


if __name__ == "__main__":
    main()

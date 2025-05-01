from flask import Flask, render_template, request, redirect, url_for, session
import uuid

app = Flask(__name__)
app.secret_key = "super-secret-key"

# セッションごとのゲーム状態管理
game_sessions = {}

# 国名リスト、優先リスト、使用済みリストの初期化
countries = [
    "アイスランド", "アイルランド", "アゼルバイジャン", "アフガニスタン", "アメリカ",
    "アラブシュチョウコクレンポウ", "アルジェリア", "アルゼンチン", "アルバニア", "アンドラ",
    "アンゴラ", "アンティグアバーブーダ", "イエメン", "イギリス", "イスラエル", "イタリア", "イラク", "イラン",
    "インド", "インドネシア", "ウガンダ", "ウクライナ", "ウズベキスタン", "ウルグアイ",
    "エクアドル", "エストニア", "エチオピア", "エジプト", "エリトリア", "エルサルバドル", "エスワティニ",
    "オーストラリア", "オーストリア", "オマーン", "オランダ", "カーボベルデ",
    "カザフスタン", "カタール", "カナダ", "カメルーン", "ガイアナ", "ガーナ", "ガボン",
    "カンボジア", "キプロス", "キューバ", "ギリシャ", "キリバス", "キルギス", "キタマケドニア", "ギニアビサウ",
    "グアテマラ", "クックショトウ", "クロアチア", "グレナダ", "クウェート", "ケニア", "コンゴキョウワコク",
    "コンゴミンシュキョウワコク", "コートジボワール", "コソボ", "コモロ", "コロンビア", "サウジアラビア",
    "サモア", "サントメプリンシペ", "サンマリノ",
    "ザンビア", "シエラレオネ", "シリア", "シンガポール", "シオラレオネ", "ジブチ", "ジャマイカ",
    "ジンバブエ", "スイス", "スウェーデン", "スーダン", "スペイン", "スリナム",
    "スリランカ", "スロバキア", "スロベニア", "セーシェル", "セネガル", "セルビア", "セキドウギニア",
    "セントクリストファーネービス", "セントビンセントオヨビグレナディーンショトウ", "セントルシア",
    "ソマリア", "ソロモンショトウ", "タイ", "タジキスタン", "ダイカンミンコク", "タイワン",
    "タンザニア", "チェコ", "チュウカジンミンキョウワコク", "チリ", "チャド", "チュニジア",
    "チョウセンミンシュシュギジンミンキョウワコク",
    "ツバル", "デンマーク", "トーゴ", "トルクメニスタン", "トルコ", "ドイツ", "トンガ", "ドミニカコク", 
    "トリニダードトバゴ", "ドミニカキョウワコク", "ナイジェリア", "ナウル", "ナミビア", "ニウエ", "ニッポン",
    "ニカラグア", "ニジェール", "ニュージーランド", "ネパール", "ノルウェー",
    "ハイチ", "パキスタン", "パナマ", "パラグアイ", "パラオ", "バチカンシコク", "バルバドス",
    "バヌアツ", "バハマ", "バングラデシュ", "バーレーン", "ハンガリー", "パプアニューギニア",
    "ヒガシティモール", "フィジー", "フィリピン", "フィンランド", "ブータン", "ブラジル", "ブルガリア",
    "ブルキナファソ", "ブルネイ", "ブルンジ", "ベトナム", "ベナン",
    "ベネズエラ", "ベラルーシ", "ベリーズ", "ベルギー", "ペルー",
    "ポーランド", "ボスニアヘルツェゴビナ", "ボツワナ", "ボリビア", "ポルトガル", "ホンジュラス",
    "マーシャルショトウ", "マダガスカル", "マルタ", "マレーシア", "ミクロネシア",
    "ミャンマー", "ミナミアフリカキョウワコク", "ミナミスーダン", "メキシコ",
    "モーリシャス", "モーリタニア", "モザンビーク",
    "モナコ", "モルディブ", "モルドバ", "モンゴル", "モンテネグロ",
    "ヨルダン", "ラオス", "ラトビア", "リトアニア", "リビア",
    "リベリア", "ルクセンブルク", "ルーマニア", "ルワンダ", "レバノン",
    "レソト", "ロシア"
]

# 優先リスト
priority_list = {
    'ア': ['アンゴラ', 'アンドラ'],
    'イ': 'インド',
    'ウ': 'ウクライナ',
    'エ': 'エスワティニ',
    'オ': 'オランダ',
    'カ': 'カーボベルデ',
    'キ': 'ギリシャ',
    'ク': 'グアテマラ',
    'コ': 'コモロ',
    'サ': 'サンマリノ',
    'シ': 'シエラレオネ',
    'ス': 'スリナム',
    'セ': 'セネガル',
    'ソ': 'ソロモンショトウ',
    'タ': 'タイ',
    'チ': 'チリ',
    'ツ': 'ツバル',
    'テ': 'デンマーク',
    'ト': 'ドイツ',
    'ナ': 'ナウル',
    'ニ': 'ニウエ',
    'マ': 'マリ',
    'ミ': 'ミャンマー',
    'モ': 'モンテネグロ',
    'ハ': 'バヌアツ',
    'フ': 'ブルキナファソ',
    'ヘ': 'ベトナム',
    'ホ': ['ボスニアヘルツェゴビナ', 'ボツワナ'],
    'ラ': 'ラトビア',
    'リ': ['リビア', 'リベリア', 'リトアニア'],
    'レ': 'レソト',
    'ル': 'ルワンダ',
}

priority2_list = {
    'ア': ['アイスランド', 'アイルランド', 'アメリカ','アラブシュチョウコクレンポウ', 'アルジェリア',  'アルバニア', 'アンティグアバーブーダ'],
    'イ': 'イスラエル',
    'ウ': ['ウガンダ','ウルグアイ'],
    'エ': 'エクアドル',
    'オ': 'オーストラリア',
    'カ': ['カタール', 'カナダ', 'ガイアナ', 'ガーナ', 'カンボジア'],
    'タ': ['タンザニア','ダイカンミンコク'],
    'チ': 'チリ',
    'ト': ['トーゴ', 'トルコ', 'トンガ', 'ドミニカコク','トリニダードトバゴ', 'ドミニカキョウワコク'],
    'ニ': ['ニカラグア', 'ニジェール', 'ニュージーランド'],
    'ミ': 'ミナミアフリカキョウワコク',
    'ハ': 'バヌアツ',
    'フ': ['フィジー', 'フィンランド', 'ブラジル', 'ブルガリア','ブルネイ', 'ブルンジ',],
}

def normalize_word(word):
    if not word:
        return None
    mapping = {
        'ガ': 'カ', 'ギ': 'キ', 'グ': 'ク', 'ゲ': 'ケ', 'ゴ': 'コ',
        'ザ': 'サ', 'ジ': 'シ', 'ズ': 'ス', 'ゼ': 'セ', 'ゾ': 'ソ',
        'ダ': 'タ', 'ヂ': 'チ', 'ヅ': 'ツ', 'デ': 'テ', 'ド': 'ト',
        'バ': 'ハ', 'ビ': 'ヒ', 'ブ': 'フ', 'ベ': 'ヘ', 'ボ': 'ホ',
        'パ': 'ハ', 'ピ': 'ヒ', 'プ': 'フ', 'ペ': 'ヘ', 'ポ': 'ホ',
        'ェ': 'エ', 'ュ': 'ユ', 'ャ': 'ヤ',
    }
    normalized_chars = []
    for i, char in enumerate(word):
        if char == 'ー':
            if i > 0:
                normalized_chars.append(normalized_chars[-1])
        else:
            normalized_chars.append(mapping.get(char, char))
    return ''.join(normalized_chars)
    
@app.route("/sitemap.xml", methods=["GET"])
def sitemap():
    pages = []

    # 静的に登録するURL一覧（必要に応じて増やす）
    base_url = "https://shiritori-game-ihgf.onrender.com"  # あなたの Render URL に書き換えてください
    pages.append({
        "loc": f"{base_url}/",
        "lastmod": datetime.utcnow().date().isoformat()
    })
    pages.append({
        "loc": f"{base_url}/result",  # 結果ページなど
        "lastmod": datetime.utcnow().date().isoformat()
    })

    # XML 形式で出力
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'

    for page in pages:
        xml += "  <url>\n"
        xml += f"    <loc>{page['loc']}</loc>\n"
        xml += f"    <lastmod>{page['lastmod']}</lastmod>\n"
        xml += "  </url>\n"

    xml += "</urlset>"

    return Response(xml, mimetype="application/xml")

@app.before_request
def initialize_session():
    if "session_id" not in session:
        session["session_id"] = str(uuid.uuid4())
    if session["session_id"] not in game_sessions:
        game_sessions[session["session_id"]] = {"used_countries": [], "last_syllable": None}

def reset_game():
    session_id = session["session_id"]
    game_sessions[session_id] = {"used_countries": [], "last_syllable": None}

def get_computer_response(last_syllable):
    session_id = session["session_id"]
    used_countries = game_sessions[session_id]["used_countries"]

    # 優先リスト1
    if last_syllable in priority_list:
        preferred = priority_list[last_syllable]
        if isinstance(preferred, list):
            for country in preferred:
                if country not in used_countries:
                    return country
        else:
            if preferred not in used_countries:
                return preferred

    # 優先リスト2
    if last_syllable in priority2_list:
        preferred = priority2_list[last_syllable]
        if isinstance(preferred, list):
            for country in preferred:
                if country not in used_countries:
                    return country
        else:
            if preferred not in used_countries:
                return preferred

    # 通常検索
    for country in countries:
        if country.startswith(last_syllable) and country not in used_countries:
            return country

    return None

@app.route('/', methods=['GET', 'POST'])
def index():
    session_id = session["session_id"]
    game_state = game_sessions[session_id]
    used = game_state["used_countries"]
    last_syllable = game_state["last_syllable"]
    message = ""

    if request.method == 'POST':
        player_input = request.form.get('player_input')

        if player_input not in countries:
            message = "無効な国名です。"
            return render_template('index.html', message=message, used_countries=used, countries=countries)

        if player_input in used:
            message = "その国名はすでに使用されています。"
            return render_template('index.html', message=message, used_countries=used, countries=countries)

        if player_input in ["スリナム", "ギリシャ"]:
            reset_game()
            message = f"「{normalize_word(player_input)[-1]}」で始まる国が見つかりません。あなたの勝ちです！"
            return render_template('index.html', message=message, used_countries=[], countries=countries)

        normalized_last_char = normalize_word(player_input)[-1]

        if last_syllable is None:
            if normalized_last_char == 'ン':
                reset_game()
                message = "あなたの負けです！"
                return render_template('index.html', message=message, used_countries=[], countries=countries)
            used.append(player_input)
            game_state["last_syllable"] = normalized_last_char
        else:
            if normalize_word(player_input)[0] != last_syllable:
                message = f"「{last_syllable}」で始まる国名を入力してください。"
                return render_template('index.html', message=message, used_countries=used, countries=countries)

            if normalized_last_char == 'ン':
                reset_game()
                message = "あなたの負けです！"
                return render_template('index.html', message=message, used_countries=[], countries=countries)
            used.append(player_input)
            game_state["last_syllable"] = normalized_last_char

        computer_response = get_computer_response(game_state["last_syllable"])

        if not computer_response:
            reset_game()
            message = "その国の最後の文字で始まる国が見つかりません。あなたの勝ちです！"
            return render_template('index.html', message=message, used_countries=[], countries=countries)

        if computer_response in ["スリナム", "ギリシャ"]:
            reset_game()
            message = f"「{normalize_word(computer_response)[-1]}」で始まる国がありません。私の勝ちです！"
            return render_template('index.html', player_input=player_input, computer_response=computer_response, message=message, used_countries=[], countries=countries)

        if normalize_word(computer_response)[-1] == 'ン':
            reset_game()
            message = "私の負けです！"
            return render_template('index.html', player_input=player_input, computer_response=computer_response, message=message, used_countries=[], countries=countries)

        used.append(computer_response)
        game_state["last_syllable"] = normalize_word(computer_response)[-1]

        return render_template('index.html',
                               player_input=player_input,
                               computer_response=computer_response,
                               message=message,
                               used_countries=used,
                               countries=countries)

    return render_template('index.html', message=message, used_countries=used, countries=countries)

@app.route('/reset')
def reset():
    reset_game()
    return redirect(url_for('index'))

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

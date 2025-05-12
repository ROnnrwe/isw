from flask import Flask, render_template, request, redirect, url_for, session
import random

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# 후보자 데이터를 하드코딩
candidates = [
    {"name": "아오이 유우", "image": "images/aoiyuu.jpeg"},
    {"name": "나가사와 마사미", "image": "images/masami.jpeg"},
    {"name": "이시하라 사토미", "image": "images/satomi.jpeg"},
    {"name": "히로세 스즈", "image": "images/suzu.jpeg"},
    {"name": "키타가와 케이코", "image": "images/keiko.jpeg"},
    {"name": "아리무라 카스미", "image": "images/kasumi.jpeg"},
    {"name": "고마츠 나나", "image": "images/nana.jpeg"},
    {"name": "혼다 츠바사", "image": "images/tsubasa.jpeg"},
    {"name": "나가노 메이", "image": "images/mei.jpeg"},
    {"name": "사사키 노조미", "image": "images/nozomi.jpeg"},
    {"name": "호리키타 마키", "image": "images/maki.jpeg"},
    {"name": "하마베 미나미", "image": "images/minami.jpeg"},
    {"name": "카와구치 하루나", "image": "images/haruna.jpeg"},
    {"name": "이마다 미오", "image": "images/mio.jpeg"},
    {"name": "하시모토 칸나", "image": "images/kanna.jpeg"},
    {"name": "나카와 유키에", "image": "images/yukie.jpeg"},
    {"name": "논", "image": "images/non.jpeg"},
    {"name": "시바사키 코우", "image": "images/kou.jpeg"},
    {"name": "아시카와 이즈미", "image": "images/izumi.jpg"},
    {"name": "아야세 하루카", "image": "images/haruka.jpeg"},
    {"name": "아라가키 유이", "image": "images/yui.jpeg"},
    {"name": "히로스에 료코", "image": "images/ryoko.jpeg"},
    {"name": "카호", "image": "images/kaho.jpeg"},
    {"name": "마츠다 세이코", "image": "images/seiko.jpeg"},
    {"name": "시라이시 마이", "image": "images/mai.jpeg"},
    {"name": "다케우치 유코", "image": "images/yuko.jpeg"},
    {"name": "우에노 주리", "image": "images/juri.jpeg"},
    {"name": "나카죠 아야미", "image": "images/ayami.jpeg"},
    {"name": "타카하시 히카루", "image": "images/hikaru.jpeg"},
    {"name": "후카다 쿄코", "image": "images/kyoko.jpeg"},
    {"name": "미요시 아야카", "image": "images/ayaka.jpeg"},
    {"name": "요시나가 사유리", "image": "images/sayuri.jpeg"}
]

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/start')
def start():
    random.shuffle(candidates)  # 후보자 목록을 섞어서 대결 시작
    session['round'] = candidates
    session['new_round'] = []
    return redirect(url_for('match'))

@app.route('/match', methods=['GET', 'POST'])
def match():
    if 'round' not in session or len(session['round']) <= 1:
        return redirect(url_for('winner'))

    if request.method == 'POST':
        winner_name = request.form['winner']
        new_round = session.get('new_round', [])

        for candidate in session['round']:
            if candidate['name'] == winner_name:
                new_round.append(candidate)
                break

        session['new_round'] = new_round
        session['round'] = session['round'][2:]

        if len(session['round']) == 0:
            session['round'] = session['new_round']
            session['new_round'] = []

        return redirect(url_for('match'))

    left = session['round'][0]
    right = session['round'][1]
    return render_template('match.html', left=left, right=right)

@app.route('/winner')
def winner():
    final_winner = None
    if 'round' in session and len(session['round']) == 1:
        final_winner = session['round'][0]
    return render_template('winner.html', winner=final_winner)

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
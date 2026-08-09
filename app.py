import sqlite3
from flask import Flask, render_template, request

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    initial = request.args.get('initial', '')
    keyword = request.args.get('q', '')
    
    conn = get_db_connection()
    
    # 초성 필터링 또는 검색어 쿼리
    if initial:
        vtubers = conn.execute('SELECT * FROM vtuber WHERE initial_sound = ? ORDER BY name', (initial,)).fetchall()
    elif keyword:
        vtubers = conn.execute('SELECT * FROM vtuber WHERE name LIKE ? ORDER BY name', (f'%{keyword}%',)).fetchall()
    else:
        vtubers = conn.execute('SELECT * FROM vtuber ORDER BY name').fetchall()
        
    conn.close()
    
    initials = ['ㄱ', 'ㄴ', 'ㄷ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅅ', 'ㅇ', 'ㅈ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']
    return render_template('index.html', vtubers=vtubers, initials=initials, current_initial=initial, keyword=keyword)

if __name__ == '__main__':
    app.run(debug=True)
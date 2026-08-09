import sqlite3
from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'virtual_db_super_secret_key'
ADMIN_PASSWORD = 'admin_password_123!'

# 1. 초성 추출 함수
def get_initial_sound(text):
    if not text:
        return '기타'
    CHOSUNG_LIST = ['ㄱ', 'ㄲ', 'ㄴ', 'ㄷ', 'ㄸ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅃ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅉ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']
    char_code = ord(text[0]) - 44032
    if 0 <= char_code <= 11172:
        return CHOSUNG_LIST[char_code // 588]
    return '기타'

# 2. DB 연결 함수
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# 3. 로그인 필수 데코레이터 (라우트보다 무조건 위에 위치)
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in'):
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# -------------------------------------------------------------
# 라우트 선언
# -------------------------------------------------------------

@app.route('/')
def index():
    initial = request.args.get('initial', '')
    keyword = request.args.get('q', '')
    
    conn = get_db_connection()
    if initial:
        vtubers = conn.execute('SELECT * FROM vtuber WHERE initial_sound = ? ORDER BY name', (initial,)).fetchall()
    elif keyword:
        vtubers = conn.execute('SELECT * FROM vtuber WHERE name LIKE ? ORDER BY name', (f'%{keyword}%',)).fetchall()
    else:
        vtubers = conn.execute('SELECT * FROM vtuber ORDER BY name').fetchall()
    conn.close()
    
    initials = ['ㄱ', 'ㄴ', 'ㄷ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅅ', 'ㅇ', 'ㅈ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']
    return render_template('index.html', vtubers=vtubers, initials=initials, current_initial=initial, keyword=keyword)

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['password'] == ADMIN_PASSWORD:
            session['logged_in'] = True
            return redirect(url_for('bulk_add'))
        else:
            error = '비밀번호가 올바르지 않습니다.'
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('index'))

@app.route('/admin/bulk', methods=['GET', 'POST'])
@login_required
def bulk_add():
    if request.method == 'POST':
        raw_data = request.form.get('bulk_data', '')
        lines = raw_data.strip().split('\n')
        
        insert_rows = []
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            if '\t' in line:
                parts = [p.strip() for p in line.split('\t')]
            else:
                parts = [p.strip() for p in line.split(',')]
            
            if len(parts) >= 1 and parts[0]:
                name = parts[0]
                name_en = parts[1] if len(parts) > 1 else ''
                initial = get_initial_sound(name)
                platform = parts[2] if len(parts) > 2 else ''
                status = parts[3] if len(parts) > 3 else '활동중'
                agency = parts[4] if len(parts) > 4 else ''
                gender = parts[5] if len(parts) > 5 else ''
                birthday = parts[6] if len(parts) > 6 else ''
                age = parts[7] if len(parts) > 7 else ''
                debut_date = parts[8] if len(parts) > 8 else ''
                species = parts[9] if len(parts) > 9 else ''
                fan_name = parts[10] if len(parts) > 10 else ''
                oshi_mark = parts[11] if len(parts) > 11 else ''
                main_platform_url = parts[12] if len(parts) > 12 else ''
                youtube_url = parts[13] if len(parts) > 13 else ''
                
                insert_rows.append((
                    name, name_en, initial, platform, status, agency,
                    gender, birthday, age, debut_date, species,
                    fan_name, oshi_mark, main_platform_url, youtube_url
                ))
        
        if insert_rows:
            conn = get_db_connection()
            conn.executemany("""
                INSERT INTO vtuber (
                    name, name_en, initial_sound, platform, status, agency,
                    gender, birthday, age, debut_date, species,
                    fan_name, oshi_mark, main_platform_url, youtube_url
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, insert_rows)
            conn.commit()
            conn.close()
            
        return redirect(url_for('index'))
        
    return render_template('bulk_add.html')

if __name__ == '__main__':
    app.run(debug=True)
import sqlite3

def get_initial_sound(text):
    if not text:
        return '기타'
    CHOSUNG_LIST = ['ㄱ', 'ㄲ', 'ㄴ', 'ㄷ', 'ㄸ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅃ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅉ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']
    char_code = ord(text[0]) - 44032
    if 0 <= char_code <= 11172:
        return CHOSUNG_LIST[char_code // 588]
    return '기타'

conn = sqlite3.connect('database.db')
with open('schema.sql', encoding='utf-8') as f:
    conn.executescript(f.read())

cur = conn.cursor()

# 14개 필드 규격 예시 데이터 (이름 ~ 유튜브 링크)
sample_data = [
    ('강지', 'Gangzi', '치지직', '활동중', '스텔라이브', '여성', '', '', '', '인간', '파스텔', '🐾', 'https://chzzk.naver.com', 'https://youtube.com'),
]

for row in sample_data:
    name = row[0]
    initial = get_initial_sound(name)
    cur.execute("""
        INSERT INTO vtuber (
            name, name_en, initial_sound, platform, status, agency,
            gender, birthday, age, debut_date, species,
            fan_name, oshi_mark, main_platform_url, youtube_url
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        row[0], row[1], initial, row[2], row[3], row[4],
        row[5], row[6], row[7], row[8], row[9],
        row[10], row[11], row[12], row[13]
    ))

conn.commit()
conn.close()
print("DB 초기화 완료!")
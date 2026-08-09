import sqlite3

# 한글 초성 추출 함수
def get_initial_sound(text):
    CHOSUNG_LIST = ['ㄱ', 'ㄲ', 'ㄴ', 'ㄷ', 'ㄸ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅃ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅉ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']
    char_code = ord(text[0]) - 44032
    if 0 <= char_code <= 11172:
        return CHOSUNG_LIST[char_code // 588]
    return '기타'

conn = sqlite3.connect('database.db')
with open('schema.sql', encoding='utf-8') as f:
    conn.executescript(f.read())

cur = conn.cursor()

# 테스트용 초기 데이터 (구글 시트/CSV 데이터를 이 형태로 순회하며 넣어주면 됩니다)
sample_data = [
    ('강지', '치지직', 'https://chzzk.naver.com'),
    ('고세구', 'SOOP', 'https://soop.com'),
    ('나나문', '유튜브', 'https://youtube.com'),
]

for name, platform, url in sample_data:
    initial = get_initial_sound(name)
    cur.execute(
        "INSERT INTO vtuber (name, initial_sound, platform, channel_url) VALUES (?, ?, ?, ?)",
        (name, initial, platform, url)
    )

conn.commit()
conn.close()
print("DB 초기화 완료!")
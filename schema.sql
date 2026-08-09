DROP TABLE IF EXISTS vtuber;

CREATE TABLE vtuber (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,          -- 이름
    name_en TEXT,               -- 영문이름
    initial_sound TEXT NOT NULL, -- 초성 (자동추출)
    platform TEXT,              -- 플랫폼 (치지직, SOOP 등)
    status TEXT DEFAULT '활동중',  -- 상태
    agency TEXT,                -- 소속팀/사
    gender TEXT,                -- 성별
    birthday TEXT,              -- 생일
    age TEXT,                   -- 나이
    debut_date TEXT,            -- 데뷔일
    species TEXT,               -- 종족
    fan_name TEXT,              -- 팬네임
    oshi_mark TEXT,             -- 오시마크
    main_platform_url TEXT,     -- 주 플랫폼 링크
    youtube_url TEXT,           -- 유튜브 링크
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
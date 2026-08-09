DROP TABLE IF EXISTS vtuber;

CREATE TABLE vtuber (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,          -- 이름 (예: 강지)
    initial_sound TEXT NOT NULL, -- 초성 (예: ㄱ)
    platform TEXT,              -- 주요 방송 플랫폼 (치지직, 아프리카, 유튜브 등)
    status TEXT DEFAULT '활동중',  -- 상태 (활동중, 졸업 등)
    channel_url TEXT,           -- 대표 채널 링크
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
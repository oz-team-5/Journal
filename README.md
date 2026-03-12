erDiagram
    users ||--o{ diaries : "writes"
    users ||--o{ token_blacklist : "invalidates"
    users ||--o{ bookmarks : "marks"
    users ||--o{ user_questions : "receives"
    quotes ||--o{ bookmarks : "is_bookmarked"
    questions ||--o{ user_questions : "is_asked"

    users {
        int id PK
        varchar username
        varchar password_hash
        timestamp created_at
    }

    diaries {
        int id PK
        int user_id FK
        varchar title
        text content
        timestamp created_at
    }

    token_blacklist {
        int id PK
        varchar token
        int user_id FK
        timestamp expired_at
    }

    quotes {
        int id PK
        text content
        varchar author
    }

    bookmarks {
        int id PK
        int user_id FK
        int quote_id FK
    }

    questions {
        int id PK
        varchar question_text
    }

    user_questions {
        int id PK
        int user_id FK
        int question_id FK
        timestamp received_at
    }
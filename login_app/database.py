import sqlite3

def init_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    
    # 테이블 생성 쿼리
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            nickname TEXT NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    
    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()

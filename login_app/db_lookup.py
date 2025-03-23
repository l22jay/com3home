import sqlite3

# 데이터베이스 연결
conn = sqlite3.connect('users.db')  # 'users.db'를 실제 파일 경로로 변경
cursor = conn.cursor()

# 테이블 목록 확인
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
print("Tables:", tables)

# 각 테이블의 데이터 조회
for table in tables:
    table_name = table[0]
    print(f"\nContents of table '{table_name}':")
    cursor.execute(f"SELECT * FROM {table_name};")
    rows = cursor.fetchall()
    
    for row in rows:
        print(row)

# 연결 종료
conn.close()

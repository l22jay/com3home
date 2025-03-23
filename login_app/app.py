from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # 비밀키 설정 (실제 배포 시에는 안전한 비밀키를 사용하세요)

# 데이터베이스에 연결하는 함수
def get_db_connection():
    conn = sqlite3.connect('users.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if not username or not password:
            return render_template('login.html', error='ID와 암호를 모두 입력해 주십시오.')

        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        conn.close()
        
        if user and check_password_hash(user['password'], password):
            session['username'] = username  # 로그인 성공 시 세션에 유저네임 저장
            return redirect(url_for('home'))
        else:
            return render_template('login.html', error='ID또는 암호가 잘못되었습니다.')

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        nickname = request.form.get('nickname')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if not username or not email or not nickname or not password or not confirm_password:
            return render_template('register.html', error='모든 입력란을 작성해 주십시오.')

        if password != confirm_password:
            return render_template('register.html', error='암호가 일치하지 않습니다.')

        conn = get_db_connection()
        try:
            existing_user = conn.execute('SELECT * FROM users WHERE username = ? OR email = ?', (username, email)).fetchone()
            if existing_user:
                if existing_user['username'] == username:
                    return render_template('register.html', error='이미 사용 중인 ID입니다.')
                if existing_user['email'] == email:
                    return render_template('register.html', error='이미 사용 중인 이메일입니다.')

            hashed_password = generate_password_hash(password)
            conn.execute('INSERT INTO users (username, email, nickname, password) VALUES (?, ?, ?, ?)',
                         (username, email, nickname, hashed_password))
            conn.commit()
            return redirect(url_for('register_complete'))
        except Exception as e:
            print(f'Error occurred during registration: {e}')
            return render_template('register.html', error='회원가입 중 오류가 발생했습니다.')
        finally:
            conn.close()

    return render_template('register.html')

@app.route('/register_complete')
def register_complete():
    return render_template('register_complete.html')

@app.route('/home')
def home():
    username = session.get('username')  # 세션에서 유저네임 가져오기
    if not username:
        return redirect(url_for('login'))  # 로그인하지 않은 경우 로그인 페이지로 리다이렉트

    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
    conn.close()

    if user:
        nickname = user['nickname']
    else:
        nickname = '사용자'  # 기본값 설정

    return render_template('home.html', username=username, nickname=nickname)

@app.route('/logout')
def logout():
    session.pop('username', None)  # 세션에서 유저네임 제거
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)  # 포트를 5000으로 설정
    #app.run(host="172.30.1.85", port=5000);

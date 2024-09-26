from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)  # Menggunakan __name__ dengan dua underscore
app.secret_key = 'your_secret_key'  # Pastikan ini nilai yang aman

# Konfigurasi MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'suppliers1'

# Inisialisasi MySQL
mysql = MySQL(app)

# Register Route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Hash password
        hashed_password = generate_password_hash(password)

        # Simpan ke database (username dan hashed_password saja)
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO tb_user (username, password) VALUES (%s, %s)", (username, hashed_password))
        mysql.connection.commit()
        cur.close()
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

# Login Route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password_candidate = request.form['password']

        # Cek data di database menggunakan username
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM tb_user WHERE username = %s", [username])
        user = cur.fetchone()
        cur.close()

        # Pastikan data pengguna ditemukan dan periksa password hash
        if user and check_password_hash(user[2], password_candidate):  # Kolom ke-2 untuk password (dianggap urutannya id, username, password)
            flash('You are logged in!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')

    return render_template('login.html')

# Dashboard Route
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

if __name__ == '__main__':
    app.run(debug=True)

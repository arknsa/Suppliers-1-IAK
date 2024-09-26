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

# Route untuk menampilkan semua produk
@app.route('/products')
def products():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM tb_product")
    products = cur.fetchall()
    cur.close()
    return render_template('products.html', products=products)

# Route untuk menambahkan produk
@app.route('/add_product', methods=['POST'])
def add_product():
    if request.method == 'POST':
        nama_product = request.form['nama_product']
        stock = request.form['stock']
        harga = request.form['harga']
        deskripsi = request.form['deskripsi']
        link_gambar_barang = request.form['link_gambar_barang']
        berat = request.form['berat']
        
        # Simpan produk ke database
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO tb_product (nama_product, stock, harga, deskripsi, link_gambar_barang, berat) VALUES (%s, %s, %s, %s, %s, %s)", 
                    (nama_product, stock, harga, deskripsi, link_gambar_barang, berat))
        mysql.connection.commit()
        cur.close()
        flash('Product added successfully!', 'success')
        return redirect(url_for('products'))

# Route untuk menghapus produk
@app.route('/delete_product/<int:id>', methods=['POST'])
def delete_product(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM tb_product WHERE id = %s", [id])
    mysql.connection.commit()
    cur.close()
    flash('Product deleted successfully!', 'success')
    return redirect(url_for('products'))

# Route untuk mengedit produk
@app.route('/edit_product/<int:id>', methods=['GET', 'POST'])
def edit_product(id):
    cur = mysql.connection.cursor()
    if request.method == 'POST':
        nama_product = request.form['nama_product']
        stock = request.form['stock']
        harga = request.form['harga']
        deskripsi = request.form['deskripsi']
        link_gambar_barang = request.form['link_gambar_barang']
        berat = request.form['berat']

        cur.execute("""
            UPDATE tb_product 
            SET nama_product = %s, stock = %s, harga = %s, deskripsi = %s, link_gambar_barang = %s, berat = %s 
            WHERE id = %s
        """, (nama_product, stock, harga, deskripsi, link_gambar_barang, berat, id))
        mysql.connection.commit()
        cur.close()
        flash('Product updated successfully!', 'success')
        return redirect(url_for('products'))
    
    cur.execute("SELECT * FROM tb_product WHERE id = %s", [id])
    product = cur.fetchone()
    cur.close()
    return render_template('edit_product.html', product=product)

# API untuk mengambil semua produk
@app.route('/api/products', methods=['GET'])
def all_products_api():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM tb_product")
    products = cur.fetchall()
    cur.close()
    
    all_products = []
    for product in products:
        all_products.append({
            'id': product[0],
            'nama_product': product[1],
            'stock': product[2],
            'harga': float(product[3]),
            'deskripsi': product[4],
            'link_gambar_barang': product[5],
            'berat': float(product[6])
        })
    return jsonify(all_products)

# API untuk membuat pesanan
@app.route('/api/orders', methods=['POST'])
def create_order():
    data = request.get_json()
    list_barang = data['list_barang']  # daftar barang yang dipesan
    alamat_pembeli = data['alamat_pembeli']
    kode_jasa = data['kode_jasa']

    # Buat nomor resi dummy untuk respon
    resi = 'RESI' + str(int(time.time()))

    # Simpan pesanan ke database, bisa dikembangkan lebih lanjut
    # misalnya membuat log transaksi atau detail pesanan

    return jsonify({'status': 'success', 'resi': resi})

# API untuk mengambil informasi supplier
@app.route('/api/suppliers', methods=['GET'])
def suppliers_info():
    # Mengembalikan informasi supplier (bisa diambil dari database atau data statis)
    suppliers = [
        {
            'name': 'Supplier A',
            'location': 'City A',
            'contact': '123-456-789'
        },
        {
            'name': 'Supplier B',
            'location': 'City B',
            'contact': '987-654-321'
        }
    ]
    return jsonify(suppliers)

if __name__ == '__main__':
    app.run(debug=True)
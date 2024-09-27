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

@app.route('/add_products', methods=['GET', 'POST'])
def add_products():
    if request.method == 'POST':
        try:
            # Ambil data dari form sesuai dengan name di HTML
            nama_product = request.form['nama_product']
            kategori = request.form['kategori']
            stock = request.form['stock']
            harga = request.form['harga']
            berat = request.form['berat']
            size = request.form['size']
            width = request.form['width']
            genre = request.form['genre']
            warna = request.form['warna']
            deskripsi = request.form['deskripsi']
            gambar = request.form['link_gambar_barang']

            # Simpan produk ke database
            cur = mysql.connection.cursor()
            cur.execute("""
                INSERT INTO tb_product 
                (nama_product, kategori, stock, harga, berat, size, width, genre, warna, deskripsi, gambar) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (nama_product, kategori, stock, harga, berat, size, width, genre, warna, deskripsi, gambar))
            
            # Commit dan tutup koneksi
            mysql.connection.commit()
            cur.close()
            
            # Menampilkan pesan dan redirect ke halaman yang sesuai
            flash('Product added successfully!', 'success')
            return redirect(url_for('add_products'))
        
        except Exception as e:
            # Log kesalahan jika terjadi
            print(f"Error: {e}")
            flash('Terjadi kesalahan saat menambah produk.', 'danger')
            return redirect(url_for('add_products'))

    # Jika metode GET, tampilkan form kosong untuk menambah produk
    return render_template('add_products.html')


# Route untuk menampilkan semua produk
@app.route('/manage_products')
def manage_products():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM tb_product")
    products = cur.fetchall()
    cur.close()
    return render_template('manage_products.html', products=products)

@app.route('/manage_account')
def manage_account():
    return render_template('manage_account.html')

@app.route('/manage_shipping')
def manage_shipping():
    return render_template('manage_shipping.html')

@app.route('/manage_stock')
def manage_stock():
    return render_template('manage_stock.html')

# Route untuk melihat produk
@app.route('/view_product/<int:id>', methods=['GET'])
def view_product(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM tb_product WHERE id = %s", [id])
    product = cur.fetchone()
    cur.close()
    
    if product:
        return render_template('view_product.html', product=product)
    else:
        flash('Product not found!', 'danger')
        return redirect(url_for('manage_products'))


# Route untuk menghapus produk
@app.route('/delete_product/<int:id>', methods=['GET', 'POST'])
def delete_product(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM tb_product WHERE id = %s", [id])
    mysql.connection.commit()
    cur.close()
    flash('Product deleted successfully!', 'success')
    return redirect(url_for('manage_products'))

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
        return redirect(url_for('manage_products'))
    
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
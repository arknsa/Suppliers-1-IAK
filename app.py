from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from models import db, Product, Retail, PengirimanDistributor, Transaksi, TransaksiBarang, Distributor, User, Supplier
from datetime import datetime
from flask_bcrypt import Bcrypt

app = Flask(__name__)

# Configurasi database, misalnya MySQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/suppliers'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'  # Ganti dengan kunci rahasia yang aman

db.init_app(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'


# Fungsi untuk memuat user berdasarkan id (dibutuhkan oleh Flask-Login)
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Route untuk login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Cek apakah user ada di database
        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            login_user(user)
            flash('Login berhasil!', 'success')
            return redirect(url_for('dashboard'))  # Ganti dengan halaman setelah login
        else:
            flash('Login gagal, username atau password salah!', 'danger')
            return redirect(url_for('login'))

    return render_template('login.html')

# Route untuk logout
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Anda telah logout!', 'success')
    return redirect(url_for('login'))

# Contoh halaman yang hanya bisa diakses setelah login
@app.route('/dashboard')
@login_required
def dashboard():
    return f'Hello, {current_user.username}! Selamat datang di dashboard.'

# Suppliers
@app.route('/suppliers')
def suppliers():
    suppliers_info = Supplier.query.all()  # Ambil semua supplier dari database
    return render_template('suppliers.html', suppliers=suppliers_info)

# Products
@app.route('/products')
def products():
    all_product = Product.query.all()  # Ambil semua produk dari database
    return render_template('products.html', products=all_product)

# Orders
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from datetime import datetime
from models import db, Transaksi, TransaksiBarang

app = Flask(__name__)

# Fungsi menghitung total harga
def calculate_total_price(list_barang):
    # Contoh sederhana: harga tiap barang adalah 1000
    return len(list_barang.split(',')) * 1000

# Fungsi menghitung total berat
def calculate_total_weight(list_barang):
    # Contoh sederhana: berat tiap barang adalah 1 kg
    return len(list_barang.split(',')) * 1

@app.route('/orders', methods=['GET', 'POST'])
def orders():
    if request.method == 'POST':
        list_barang = request.form.get('list_barang')  # Daftar barang yang dibeli
        alamat_pembeli = request.form.get('alamat_pembeli')  # Alamat pembeli
        kode_jasa = request.form.get('kode_jasa')  # Kode jasa pengiriman

        # Logika untuk membuat resi (nomor pengiriman unik)
        resi = f"RESI-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}"

        # Simpan transaksi baru di database
        new_transaksi = Transaksi(
            resi=resi,
            id_retail=None,  # Harus disesuaikan dengan data retail atau pembeli
            jumlah_barang=len(list_barang.split(',')),  # Hitung jumlah barang dari list
            total_harga=calculate_total_price(list_barang),  # Gunakan fungsi untuk menghitung total harga
            total_berat=calculate_total_weight(list_barang),  # Gunakan fungsi untuk menghitung total berat
            created_at=datetime.utcnow()
        )
        db.session.add(new_transaksi)
        db.session.commit()

        # Setelah pesanan berhasil, tampilkan halaman sukses dengan nomor resi
        return render_template('order_success.html', resi=resi)

    return render_template('orders.html')


# Route untuk menampilkan halaman Manage Product
@app.route('/manage_product')
def manage_product():
    products = Product.query.all()  # Ambil semua produk dari tabel
    return render_template('manage_product.html', products=products)

# Route untuk menambah produk baru
@app.route('/add_product', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        # Ambil data dari form HTML
        id_barang = request.form['id_barang']
        nama_product = request.form['nama_product']
        kategori = request.form['kategori']
        stock = int(request.form['stock'])
        harga = float(request.form['harga'])
        berat = float(request.form['berat'])
        size = float(request.form['size'])
        width = float(request.form['width'])
        genre = request.form['genre']
        warna = request.form['warna']
        deskripsi = request.form['deskripsi']
        link_gambar_barang = request.form['link_gambar_barang']

        # Buat objek produk baru
        new_product = Product(
            id_barang=id_barang, 
            nama_product=nama_product, 
            kategori=kategori, 
            stock=stock,
            harga=harga, 
            berat=berat, 
            size=size, 
            width=width, 
            genre=genre, 
            warna=warna,
            deskripsi=deskripsi, 
            link_gambar_barang=link_gambar_barang
        )
        
        db.session.add(new_product)
        db.session.commit()
        return redirect(url_for('manage_product'))
    
    return render_template('add_product.html')

# Route untuk edit produk
@app.route('/edit_product/<string:id_barang>', methods=['GET', 'POST'])
def edit_product(id_barang):
    product = Product.query.filter_by(id_barang=id_barang).first()

    if request.method == 'POST':
        # Update data produk dengan data dari form
        product.nama_product = request.form['nama_product']
        product.kategori = request.form['kategori']
        product.stock = int(request.form['stock'])
        product.harga = float(request.form['harga'])
        product.berat = float(request.form['berat'])
        product.size = float(request.form['size'])
        product.width = float(request.form['width'])
        product.genre = request.form['genre']
        product.warna = request.form['warna']
        product.deskripsi = request.form['deskripsi']
        product.link_gambar_barang = request.form['link_gambar_barang']

        db.session.commit()
        return redirect(url_for('manage_product'))

    return render_template('edit_product.html', product=product)

# Route untuk menghapus produk
@app.route('/delete_product/<string:id_barang>', methods=['POST'])
def delete_product(id_barang):
    product = Product.query.filter_by(id_barang=id_barang).first()
    db.session.delete(product)
    db.session.commit()
    return redirect(url_for('manage_product'))

# Route untuk melihat detail produk
@app.route('/view_product/<string:id_barang>')
def view_product(id_barang):
    product = Product.query.filter_by(id_barang=id_barang).first()
    return render_template('view_product.html', product=product)

# Route untuk menampilkan halaman Kelola Retail
@app.route('/manage_retail')
def manage_retail():
    retail_list = Retail.query.all()  # Ambil semua data retail dari database
    return render_template('manage_retail.html', retail_list=retail_list)

# Route untuk menambah retail baru
@app.route('/add_retail', methods=['GET', 'POST'])
def add_retail():
    if request.method == 'POST':
        # Ambil data dari form
        nama_retail = request.form['nama_retail']
        contact = request.form['contact']
        alamat_retail = request.form['alamat_retail']

        # Membuat objek Retail baru
        new_retail = Retail(nama_retail=nama_retail, contact=contact, alamat_retail=alamat_retail)
        db.session.add(new_retail)
        db.session.commit()

        return redirect(url_for('manage_retail'))

    return render_template('add_retail.html')

# Route untuk mengedit retail
@app.route('/edit_retail/<int:id_retail>', methods=['GET', 'POST'])
def edit_retail(id_retail):
    retail = Retail.query.filter_by(id_retail=id_retail).first()

    if request.method == 'POST':
        # Update data retail
        retail.nama_retail = request.form['nama_retail']
        retail.contact = request.form['contact']
        retail.alamat_retail = request.form['alamat_retail']
        db.session.commit()

        return redirect(url_for('manage_retail'))

    return render_template('edit_retail.html', retail=retail)

# Route untuk menghapus retail
@app.route('/delete_retail/<int:id_retail>', methods=['POST'])
def delete_retail(id_retail):
    retail = Retail.query.filter_by(id_retail=id_retail).first()
    db.session.delete(retail)
    db.session.commit()

    return redirect(url_for('manage_retail'))

# Route untuk menampilkan halaman Kelola Pengiriman
@app.route('/manage_shipping')
def manage_shipping():
    shipping_list = PengirimanDistributor.query.all()  # Ambil semua data pengiriman dari database
    return render_template('manage_shipping.html', shipping_list=shipping_list)

@app.route('/add_shipping', methods=['GET', 'POST'])
def add_shipping():
    if request.method == 'POST':
        id_pengiriman = request.form['id_pengiriman']
        id_distributor = request.form['id_distributor']
        id_product = request.form['id_product']
        jumlah = request.form['jumlah']
        tanggal_pengiriman = request.form['tanggal_pengiriman']
        total_berat = request.form['total_berat']
        total_harga = request.form['total_harga']
        status = request.form['status']

        new_shipping = PengirimanDistributor(
            id_pengiriman=id_pengiriman,
            id_distributor=id_distributor,
            id_product=id_product,
            jumlah=jumlah,
            tanggal_pengiriman=tanggal_pengiriman,
            total_berat=total_berat,
            total_harga=total_harga,
            status=status
        )
        db.session.add(new_shipping)
        db.session.commit()

        return redirect(url_for('manage_shipping'))

    # Mengambil data distributor dan produk untuk ditampilkan di dropdown
    distributors = Distributor.query.all()
    products = Product.query.all()
    return render_template('add_shipping.html', distributors=distributors, products=products)


# Route untuk mengedit pengiriman
@app.route('/edit_shipping/<string:id_pengiriman>', methods=['GET', 'POST'])
def edit_shipping(id_pengiriman):
    shipping = PengirimanDistributor.query.filter_by(id_pengiriman=id_pengiriman).first()

    if request.method == 'POST':
        shipping.id_distributor = request.form['id_distributor']
        shipping.id_product = request.form['id_product']
        shipping.jumlah = request.form['jumlah']
        shipping.tanggal_pengiriman = datetime.strptime(request.form['tanggal_pengiriman'], '%Y-%m-%d')
        shipping.total_berat = request.form['total_berat']
        shipping.total_harga = request.form['total_harga']
        shipping.status = request.form['status']
        shipping.distributor = request.form['distributor']

        db.session.commit()

        return redirect(url_for('manage_shipping'))

    return render_template('edit_shipping.html', shipping=shipping)

# Route untuk menghapus pengiriman
@app.route('/delete_shipping/<string:id_pengiriman>', methods=['POST'])
def delete_shipping(id_pengiriman):
    shipping = PengirimanDistributor.query.filter_by(id_pengiriman=id_pengiriman).first()
    db.session.delete(shipping)
    db.session.commit()

    return redirect(url_for('manage_shipping'))

# Route untuk menampilkan halaman Kelola Stok
@app.route('/manage_stock')
def manage_stock():
    stock_list = Product.query.all()  # Ambil semua data stok produk dari database
    return render_template('manage_stok.html', stock_list=stock_list)

@app.route('/add_stock', methods=['GET', 'POST'])
def add_stock():
    if request.method == 'POST':
        id_barang = request.form['id_barang']
        jumlah_stok = request.form['jumlah_stok']
        stok_minimum = request.form['stok_minimum']
        stok_maksimum = request.form['stok_maksimum']

        product = Product.query.filter_by(id=id_barang).first()
        if product:
            product.stock += int(jumlah_stok)
            product.stok_minimum = stok_minimum
            product.stok_maksimum = stok_maksimum
            db.session.commit()

        return redirect(url_for('manage_stock'))

    # Mengambil data produk untuk dropdown
    products = Product.query.all()
    return render_template('add_stock.html', products=products)


# Route untuk mengedit stok
@app.route('/edit_stock/<int:id>', methods=['GET', 'POST'])
def edit_stock(id):
    product = Product.query.get_or_404(id)
    
    if request.method == 'POST':
        product.stock = request.form['jumlah_stok']
        product.stok_minimum = request.form['stok_minimum']
        product.stok_maksimum = request.form['stok_maksimum']
        db.session.commit()

        return redirect(url_for('manage_stock'))

    return render_template('edit_stok.html', product=product)

# Route untuk menghapus stok
@app.route('/delete_stock/<int:id>', methods=['POST'])
def delete_stock(id):
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()

    return redirect(url_for('manage_stock'))

@app.route('/manage_transaksi')
def manage_transaksi():
    transaksi_list = Transaksi.query.all()  # Ambil semua data transaksi dari database
    return render_template('manage_transaksi.html', transaksi_list=transaksi_list)

# Route untuk menambah transaksi baru
@app.route('/add_transaksi', methods=['GET', 'POST'])
def add_transaksi():
    if request.method == 'POST':
        resi = request.form['resi']
        id_retail = request.form['id_retail']
        jumlah_barang = request.form['jumlah_barang']
        total_harga = request.form['total_harga']
        total_berat = request.form['total_berat']

        new_transaksi = Transaksi(
            resi=resi,
            id_retail=id_retail,
            jumlah_barang=jumlah_barang,
            total_harga=total_harga,
            total_berat=total_berat
        )
        db.session.add(new_transaksi)
        db.session.commit()

        return redirect(url_for('manage_transaksi'))

    # Mengambil data retail untuk dropdown
    retails = Retail.query.all()
    return render_template('add_transaksi.html', retails=retails)

# Route untuk mengedit transaksi
@app.route('/edit_transaksi/<int:id>', methods=['GET', 'POST'])
def edit_transaksi(id):
    transaksi = Transaksi.query.get_or_404(id)

    if request.method == 'POST':
        transaksi.resi = request.form['resi']
        transaksi.id_retail = request.form['id_retail']
        transaksi.jumlah_barang = request.form['jumlah_barang']
        transaksi.total_harga = request.form['total_harga']
        transaksi.total_berat = request.form['total_berat']
        db.session.commit()

        return redirect(url_for('manage_transaksi'))

    retails = Retail.query.all()
    return render_template('edit_transaksi.html', transaksi=transaksi, retails=retails)

# Route untuk menghapus transaksi
@app.route('/delete_transaksi/<int:id>', methods=['POST'])
def delete_transaksi(id):
    transaksi = Transaksi.query.get_or_404(id)
    db.session.delete(transaksi)
    db.session.commit()

    return redirect(url_for('manage_transaksi'))


if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin
from flask_bcrypt import Bcrypt

# Inisialisasi Flask
app = Flask(__name__)
# Konfigurasi database
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/suppliers'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy()
bcrypt = Bcrypt(app)

# Tabel Produk (tb_product)
class Product(db.Model):
    __tablename__ = 'tb_product'
    id = db.Column(db.Integer, primary_key=True)
    id_barang = db.Column(db.String(50), unique=True, nullable=False)
    nama_product = db.Column(db.String(100), nullable=False)
    kategori = db.Column(db.String(50), nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    stok_minimum = db.Column(db.Integer, nullable=False)
    stok_maksimum = db.Column(db.Integer, nullable=False)
    harga = db.Column(db.Numeric(15, 2), nullable=False)
    berat = db.Column(db.Numeric(10, 2), nullable=False)
    size = db.Column(db.Numeric(5, 2), nullable=False)
    width = db.Column(db.Numeric(5, 2), nullable=False)
    genre = db.Column(db.String(50), nullable=False)
    warna = db.Column(db.String(30), nullable=False)
    deskripsi = db.Column(db.Text, nullable=False)
    link_gambar_barang = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# Tabel User (tb_user)
class User(UserMixin, db.Model):
    __tablename__ = 'tb_user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def set_password(self, password):
        """Hashes the password and stores it."""
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        """Checks if the password matches the hashed password."""
        return bcrypt.check_password_hash(self.password, password)

# Tabel Supplier (tb_supplier)
class Supplier(db.Model):
    __tablename__ = 'tb_supplier'
    id_supplier = db.Column(db.Integer, primary_key=True)
    nama_supplier = db.Column(db.String(100), nullable=False)
    contact = db.Column(db.String(50), nullable=False)
    alamat_supplier = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Tabel Relasi Supplier dan Produk (tb_supplier_product)
class SupplierProduct(db.Model):
    __tablename__ = 'tb_supplier_product'
    id_supplier = db.Column(db.Integer, db.ForeignKey('tb_supplier.id_supplier'), primary_key=True)
    id_product = db.Column(db.Integer, db.ForeignKey('tb_product.id'), primary_key=True)

# Tabel Distributor (distributor)
class Distributor(db.Model):
    __tablename__ = 'distributor'
    id_distributor = db.Column(db.Integer, primary_key=True)
    nama_distributor = db.Column(db.String(100), nullable=False)
    contact = db.Column(db.String(50), nullable=False)
    alamat_distributor = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Tabel Retail (retail)
class Retail(db.Model):
    __tablename__ = 'retail'
    id_retail = db.Column(db.Integer, primary_key=True)
    nama_retail = db.Column(db.String(100), nullable=False)
    contact = db.Column(db.String(50), nullable=False)
    alamat_retail = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Tabel Transaksi (tb_transaksi)
class Transaksi(db.Model):
    __tablename__ = 'tb_transaksi'
    id = db.Column(db.Integer, primary_key=True)
    resi = db.Column(db.String(50), nullable=False)
    id_retail = db.Column(db.Integer, db.ForeignKey('retail.id_retail'), nullable=False)
    jumlah_barang = db.Column(db.Integer, nullable=False)
    total_harga = db.Column(db.Numeric(15, 2), nullable=False)
    total_berat = db.Column(db.Numeric(10, 2), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Tabel Transaksi Barang (tb_transaksi_barang)
class TransaksiBarang(db.Model):
    __tablename__ = 'tb_transaksi_barang'
    id = db.Column(db.Integer, primary_key=True)
    id_transaksi = db.Column(db.Integer, db.ForeignKey('tb_transaksi.id'), nullable=False)
    nama_barang = db.Column(db.String(100), nullable=False)
    jumlah = db.Column(db.Integer, nullable=False)

# Tabel Pembelian dari Supplier (tb_pembelian)
class Pembelian(db.Model):
    __tablename__ = 'tb_pembelian'
    id = db.Column(db.Integer, primary_key=True)
    id_supplier = db.Column(db.Integer, db.ForeignKey('tb_supplier.id_supplier'), nullable=False)
    id_product = db.Column(db.Integer, db.ForeignKey('tb_product.id'), nullable=False)
    jumlah = db.Column(db.Integer, nullable=False)
    total_harga = db.Column(db.Numeric(15, 2), nullable=False)
    tanggal_pembelian = db.Column(db.Date, nullable=False)

# Tabel Distribusi (distribusi)
class Distribusi(db.Model):
    __tablename__ = 'distribusi'
    id_distribusi = db.Column(db.Integer, primary_key=True)
    id_distributor = db.Column(db.Integer, db.ForeignKey('distributor.id_distributor'), nullable=False)
    id_retail = db.Column(db.Integer, db.ForeignKey('retail.id_retail'), nullable=False)
    id_product = db.Column(db.Integer, db.ForeignKey('tb_product.id'), nullable=False)
    jumlah = db.Column(db.Integer, nullable=False)
    tanggal_distribusi = db.Column(db.Date, nullable=False)

# Tabel Pengiriman dari Distributor ke Retail (pengiriman_distributor)
class PengirimanDistributor(db.Model):
    __tablename__ = 'pengiriman_distributor'
    id_pengiriman = db.Column(db.String(50), primary_key=True)
    id_distributor = db.Column(db.Integer, db.ForeignKey('distributor.id_distributor'), nullable=False)
    id_product = db.Column(db.Integer, db.ForeignKey('tb_product.id'), nullable=False)
    jumlah = db.Column(db.Integer, nullable=False)
    tanggal_pengiriman = db.Column(db.Date, nullable=False)
    total_berat = db.Column(db.Numeric(10, 2), nullable=False)
    total_harga = db.Column(db.Numeric(15, 2), nullable=False)
    status = db.Column(db.String(50), nullable=False)
    distributor = db.Column(db.String(100), nullable=False)

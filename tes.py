import requests

url = 'http://127.0.0.1:5000/orders'
data = {
  "list_barang": "Sepatu, Kemeja",
  "alamat_pembeli": "Jl. Pembeli No.1, Jakarta",
  "kode_jasa": "JNE"
}

response = requests.post(url, json=data)

# Cetak hasil respons
print(response.json())

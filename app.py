from flask import Flask, request, jsonify, render_template
import firebase_admin
from firebase_admin import credentials, firestore
import random
import string

app = Flask(__name__)

# Inisialisasi Firebase
cred = credentials.Certificate('iak6_distributor_key.json')  # Pastikan path benar
firebase_admin.initialize_app(cred)
db = firestore.client()

# Utility untuk generate no_resi
def generate_tracking_number(length=10):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

# Function untuk menghitung harga pengiriman dengan penyesuaian harga
def calculate_shipping_cost(kota_asal, kota_tujuan, berat):
    base_price_per_kg = 800  # Menurunkan harga dasar per kg
    multiplier = 1.0

    if kota_asal == 'Jakarta':
        if kota_tujuan == 'Ngawi':
            multiplier = 1.1
        elif kota_tujuan == 'Bali':
            multiplier = 1.3
        elif kota_tujuan == 'Surabaya':
            multiplier = 1.2
    elif kota_asal == 'Bandung':
        if kota_tujuan == 'Ngawi':
            multiplier = 1.05
        elif kota_tujuan == 'Bali':
            multiplier = 1.2
        elif kota_tujuan == 'Surabaya':
            multiplier = 1.15
    elif kota_asal == 'Semarang':
        if kota_tujuan == 'Ngawi':
            multiplier = 1.0
        elif kota_tujuan == 'Bali':
            multiplier = 1.2
        elif kota_tujuan == 'Surabaya':
            multiplier = 1.05

    harga_pengiriman = base_price_per_kg * berat * multiplier
    return harga_pengiriman

# Fungsi untuk generate dummy data
def generate_dummy_data():
    # Generate dummy data untuk tb_distributor
    kota_tujuan_list = ['Ngawi', 'Bali', 'Surabaya']
    kota_asal_list = ['Jakarta', 'Bandung', 'Semarang']
    distributor_data = []

    # Membuat 9 kombinasi dengan ID tetap DIS006, lama pengiriman (1-10 hari), dan harga ongkir per kg
    for kota_asal in kota_asal_list:
        for i, kota_tujuan in enumerate(kota_tujuan_list):
            id_distributor = 6  # ID tetap 6 (DIS006)
            harga_ongkir_per_kg = calculate_shipping_cost(kota_asal, kota_tujuan, 1)
            lama_pengiriman = f'{random.randint(1, 10)} hari'

            distributor_data.append({
                'id_distributor': id_distributor,
                'lama_pengiriman': lama_pengiriman,
                'kota_asal': kota_asal,
                'kota_tujuan': kota_tujuan,
                'harga_ongkir_per_kg': harga_ongkir_per_kg
            })

    # Simpan dummy data ke tb_distributor
    for distributor in distributor_data:
        db.collection('tb_distributor').document(f"{distributor['id_distributor']}_{distributor['kota_asal']}_{distributor['kota_tujuan']}").set(distributor)

    # Generate dummy data untuk tb_input_distributor
    input_distributor_data = []
    for i in range(1, 10):
        id_log = i  # Menggunakan integer untuk id_log
        kota_asal = kota_asal_list[i % 3]
        kota_tujuan = kota_tujuan_list[i % 3]
        berat = random.uniform(5, 50)  # Berat acak
        quantity = random.randint(1, 10)  # Quantity acak
        harga_pengiriman = calculate_shipping_cost(kota_asal, kota_tujuan, berat)

        input_distributor_data.append({
            'id_log': id_log,
            'kota_asal': kota_asal,
            'kota_tujuan': kota_tujuan,
            'quantity': quantity,
            'berat': berat,
            'harga_pengiriman': harga_pengiriman
        })

    # Simpan dummy data ke tb_input_distributor
    for input_data in input_distributor_data:
        db.collection('tb_input_distributor').document(str(input_data['id_log'])).set(input_data)

    # Generate dummy data untuk tb_fix_kirim_distributor sesuai dengan tb_input_distributor
    fix_kirim_data = []
    for i in range(1, 10):
        id_log = i  # Menggunakan integer untuk id_log
        no_resi = generate_tracking_number()
        status = ''  # Status default kosong sebelum POST
        input_data = input_distributor_data[i - 1]

        fix_kirim_data.append({
            'id_log': id_log,
            'kota_asal': input_data['kota_asal'],
            'kota_tujuan': input_data['kota_tujuan'],
            'quantity': input_data['quantity'],
            'berat': input_data['berat'],
            'harga_pengiriman': input_data['harga_pengiriman'],
            'status': status,
            'no_resi': ''  # No resi kosong sebelum POST
        })

    # Simpan dummy data ke tb_fix_kirim_distributor
    for fix_data in fix_kirim_data:
        db.collection('tb_fix_kirim_distributor').document(str(fix_data['id_log'])).set(fix_data)

    print("Dummy data generated successfully!")

# Route ke halaman utama (index.html)
@app.route('/')
def index():
    return render_template('index.html')

# API GET untuk mendapatkan daftar distributor
@app.route('/api/distributors6', methods=['GET'])
def get_distributors():
    distributors = db.collection('tb_distributor').stream()
    distributor_list = []
    for distributor in distributors:
        distributor_list.append(distributor.to_dict())
    return jsonify(distributor_list)

# API POST untuk mengecek harga dan menambah data ke tb_input_distributor
@app.route('/api/distributors6/orders/cek_ongkir', methods=['POST'])
def cek_harga():
    data = request.get_json()
    id_log = data.get('id_log')
    kota_asal = data.get('kota_asal')
    kota_tujuan = data.get('kota_tujuan')
    berat = data.get('berat')

    harga_pengiriman = calculate_shipping_cost(kota_asal, kota_tujuan, berat)

    # Simpan ke tb_input_distributor
    db.collection('tb_input_distributor').document(str(id_log)).set({
        'kota_asal': kota_asal,
        'kota_tujuan': kota_tujuan,
        'quantity': data.get('quantity'),
        'berat': berat,
        'harga_pengiriman': harga_pengiriman
    })

    return jsonify({'id_log': id_log, 'harga_pengiriman': harga_pengiriman})

# API POST untuk fix pengiriman dan simpan data ke tb_fix_kirim_distributor
@app.route('/api/distributors6/orders/fix_kirim', methods=['POST'])
def fix_kirim():
    data = request.get_json()
    id_log = data.get('id_log')

    # Ambil data dari tb_input_distributor berdasarkan id_log
    input_data = db.collection('tb_input_distributor').document(str(id_log)).get().to_dict()

    if not input_data:
        return jsonify({'error': 'Invalid id_log'}), 404

    # Generate no_resi dan update status
    no_resi = generate_tracking_number()
    status = 'On Progress'

    # Simpan ke tb_fix_kirim_distributor
    db.collection('tb_fix_kirim_distributor').document(str(id_log)).set({
        'kota_asal': input_data['kota_asal'],
        'kota_tujuan': input_data['kota_tujuan'],
        'quantity': input_data['quantity'],
        'berat': input_data['berat'],
        'harga_pengiriman': input_data['harga_pengiriman'],
        'status': status,
        'no_resi': no_resi
    })

    return jsonify({'id_log': id_log, 'harga_pengiriman': input_data['harga_pengiriman'], 'no_resi': no_resi})

# API GET untuk mendapatkan status pengiriman berdasarkan no_resi
@app.route('/api/status/<string:no_resi>', methods=['GET'])
def get_status(no_resi):
    docs = db.collection('tb_fix_kirim_distributor').where('no_resi', '==', no_resi).stream()
    status_data = None
    for doc in docs:
        status_data = doc.to_dict()
        break

    if status_data:
        return jsonify({'status': status_data['status']})
    else:
        return jsonify({'error': 'No resi not found'}), 404

if __name__ == '__main__':
    # generate_dummy_data()  # Generate dummy data saat aplikasi dijalankan
    app.run(debug=True)

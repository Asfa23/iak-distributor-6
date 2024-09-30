from flask import Flask, request, jsonify, render_template
import firebase_admin
from firebase_admin import credentials, firestore
import random
import string
from datetime import datetime
import math


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

    kota_asal = kota_asal.lower()  # Lowercase kota_asal
    kota_tujuan = kota_tujuan.lower()  # Lowercase kota_tujuan

    if kota_asal == 'jakarta':
        if kota_tujuan == 'ngawi':
            multiplier = 1.1
        elif kota_tujuan == 'bali':
            multiplier = 1.3
        elif kota_tujuan == 'surabaya':
            multiplier = 1.2
    elif kota_asal == 'bandung':
        if kota_tujuan == 'ngawi':
            multiplier = 1.05
        elif kota_tujuan == 'bali':
            multiplier = 1.2
        elif kota_tujuan == 'surabaya':
            multiplier = 1.15
    elif kota_asal == 'semarang':
        if kota_tujuan == 'ngawi':
            multiplier = 1.0
        elif kota_tujuan == 'bali':
            multiplier = 1.2
        elif kota_tujuan == 'surabaya':
            multiplier = 1.05

    harga_pengiriman = base_price_per_kg * berat * multiplier
    return harga_pengiriman

# Fungsi untuk menentukan lama pengiriman
def get_shipping_duration(kota_asal, kota_tujuan):
    kota_asal = kota_asal.lower()  # Lowercase kota_asal
    kota_tujuan = kota_tujuan.lower()  # Lowercase kota_tujuan

    # Logika lama pengiriman
    if kota_asal == 'jakarta' and kota_tujuan == 'surabaya':
        return '5 hari'
    elif kota_asal == 'jakarta' and kota_tujuan == 'bali':
        return '6 hari'
    elif kota_asal == 'jakarta' and kota_tujuan == 'ngawi':
        return '4 hari'
    elif kota_asal == 'bandung' and kota_tujuan == 'surabaya':
        return '4 hari'
    elif kota_asal == 'bandung' and kota_tujuan == 'bali':
        return '5 hari'
    elif kota_asal == 'bandung' and kota_tujuan == 'ngawi':
        return '3 hari'
    elif kota_asal == 'semarang' and kota_tujuan == 'surabaya':
        return '3 hari'
    elif kota_asal == 'semarang' and kota_tujuan == 'bali':
        return '4 hari'
    elif kota_asal == 'semarang' and kota_tujuan == 'ngawi':
        return '2 hari'
    else:
        return '6 hari'  # Default untuk rute yang tidak dikenali

# Fungsi untuk generate dummy data
def generate_dummy_data():
    # Generate dummy data untuk tb_distributor
    kota_tujuan_list = ['ngawi', 'bali', 'surabaya']  # Lowercase semua kota
    kota_asal_list = ['jakarta', 'bandung', 'semarang']  # Lowercase semua kota
    distributor_data = []

    # Membuat 9 kombinasi dengan ID tetap DIS006, lama pengiriman yang logis, dan harga ongkir per kg
    for kota_asal in kota_asal_list:
        for kota_tujuan in kota_tujuan_list:
            id_distributor = 6  # ID tetap 6 (DIS006)
            harga_ongkir_per_kg = calculate_shipping_cost(kota_asal, kota_tujuan, 1)
            lama_pengiriman = get_shipping_duration(kota_asal, kota_tujuan)  # Ambil lama pengiriman yang logis

            distributor_data.append({
                'id_distributor': id_distributor,
                'lama_pengiriman': lama_pengiriman,
                'kota_asal': kota_asal,  # Sudah lowercase
                'kota_tujuan': kota_tujuan,  # Sudah lowercase
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
        lama_pengiriman = get_shipping_duration(kota_asal, kota_tujuan)  # Ambil lama pengiriman

        input_distributor_data.append({
            'id_log': id_log,
            'kota_asal': kota_asal,
            'kota_tujuan': kota_tujuan,
            'quantity': quantity,
            'berat': berat,
            'harga_pengiriman': harga_pengiriman,
            'lama_pengiriman': lama_pengiriman  # Tambahkan lama_pengiriman
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
            'kota_asal': input_data['kota_asal'],  # Sudah lowercase
            'kota_tujuan': input_data['kota_tujuan'],  # Sudah lowercase
            'quantity': input_data['quantity'],
            'berat': input_data['berat'],
            'harga_pengiriman': input_data['harga_pengiriman'],
            'status': status,
            'no_resi': '',  # No resi kosong sebelum POST
            'tanggal_pembelian': datetime.now().strftime('%Y-%m-%d')  # Tambahkan tanggal pembelian
        })

    # Simpan dummy data ke tb_fix_kirim_distributor
    for fix_data in fix_kirim_data:
        db.collection('tb_fix_kirim_distributor').document(str(fix_data['id_log'])).set(fix_data)

    print("Dummy data generated successfully!")

# Route ke halaman utama (home.html)
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

@app.route('/api/distributors', methods=['GET'])
def get_distributor():
    try:
        # Akses koleksi db_distributor
        distributor ={
            "id": "DIS03",
            "nama_dis": "Distributor 03",
            "keunggulan": "Murah Meriah",
            "pemilik": "Kelompok 06",
            "deskripsi": "Ini merupakan distributor termurah diantara distributor lainnya"
        }
        return  jsonify(distributor), 200
    except Exception as e:
        return jsonify("FALSE"), 400

# API POST untuk mengecek harga dan menambah data ke tb_input_distributor
@app.route('/api/distributors6/orders/cek_ongkir', methods=['POST'])
def cek_harga():
    data = request.get_json()
    id_log = data.get('id_log')
    kota_asal = data.get('kota_asal').lower()  # Lowercase kota_asal
    kota_tujuan = data.get('kota_tujuan').lower()  # Lowercase kota_tujuan
    berat = data.get('berat')

    # Hitung harga pengiriman
    harga_pengiriman = calculate_shipping_cost(kota_asal, kota_tujuan, berat)
    harga_pengiriman = math.ceil(harga_pengiriman)  # Pembulatan ke atas

    # Dapatkan lama pengiriman
    lama_pengiriman = get_shipping_duration(kota_asal, kota_tujuan)

    # Simpan ke tb_input_distributor
    db.collection('tb_input_distributor').document(str(id_log)).set({
        'id_log': id_log,  # Tambahkan id_log
        'kota_asal': kota_asal,
        'kota_tujuan': kota_tujuan,
        # 'quantity': data.get('quantity'),
        'berat': berat,
        'harga_pengiriman': harga_pengiriman,  # Harga pengiriman sudah dibulatkan
        'lama_pengiriman': lama_pengiriman  # Tambahkan lama_pengiriman
    })

    # Return response JSON
    return jsonify({
        'id_log': id_log,
        'harga_pengiriman': harga_pengiriman,  # Harga pengiriman yang sudah dibulatkan
        'lama_pengiriman': lama_pengiriman  # Lama pengiriman yang sudah dihitung
    })


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

    # Dapatkan tanggal pembelian
    tanggal_pembelian = datetime.now().strftime('%Y-%m-%d')

    # Pembulatan harga pengiriman
    harga_pengiriman = math.ceil(input_data['harga_pengiriman'])  # Pembulatan ke atas

    # Simpan ke tb_fix_kirim_distributor
    db.collection('tb_fix_kirim_distributor').document(str(id_log)).set({
        'id_log': id_log,  # Tambahkan id_log di sini
        'kota_asal': input_data['kota_asal'],
        'kota_tujuan': input_data['kota_tujuan'],
        # 'quantity': input_data['quantity'],
        'berat': input_data['berat'],
        'harga_pengiriman': harga_pengiriman,  # Tambahkan harga yang sudah dibulatkan
        'status': status,
        'no_resi': no_resi,
        'tanggal_pembelian': tanggal_pembelian,  # Tambahkan tanggal pembelian
        'lama_pengiriman': get_shipping_duration(input_data['kota_asal'], input_data['kota_tujuan'])  # Tambahkan lama pengiriman
    })

    return jsonify({
        'id_log': id_log,
        'harga_pengiriman': harga_pengiriman,  # Kembalikan harga yang sudah dibulatkan
        'no_resi': no_resi,
        'lama_pengiriman': get_shipping_duration(input_data['kota_asal'], input_data['kota_tujuan']),
        'tanggal_pembelian': tanggal_pembelian  # Tambahkan tanggal_pembelian di response
    })



# API GET untuk mendapatkan status pengiriman berdasarkan no_resi
@app.route('/api/status/<string:no_resi>', methods=['GET'])
def get_status(no_resi):
    docs = db.collection('tb_fix_kirim_distributor').where('no_resi', '==', no_resi).stream()
    status_data = None
    for doc in docs:
        status_data = doc.to_dict()
        break

    if status_data:
        return jsonify({
            'status': status_data['status'],
            'lama_pengiriman': status_data['lama_pengiriman']  # Kembalikan lama pengiriman
        })
    else:
        return jsonify({'error': 'No resi not found'}), 404

# Route ke tabel
@app.route('/dashboard')
def tabel():
    return render_template('home.html')

# API GET untuk mendapatkan daftar distributor
@app.route('/api/distributors6/tb_fix_kirim_distributor', methods=['GET'])
def get_tb_fix_kirim_distributor():
    distributors = db.collection('tb_fix_kirim_distributor').stream()
    distributor_list2 = []
    for distributor in distributors:
        distributor_list2.append(distributor.to_dict())
    return jsonify(distributor_list2)

# API GET untuk mendapatkan daftar distributor
@app.route('/api/distributors6/tb_input_distributor', methods=['GET'])
def get_tb_input_distributor():
    distributors = db.collection('tb_input_distributor').stream()
    distributor_list3 = []
    for distributor in distributors:
        distributor_list3.append(distributor.to_dict())
    return jsonify(distributor_list3)

@app.route('/api/distributors6/orders/update_status', methods=['POST'])
def update_status():
    data = request.get_json()
    id_log = data.get('id_log')
    new_status = data.get('status')

    # Update status di tb_fix_kirim_distributor
    distributor_ref = db.collection('tb_fix_kirim_distributor').document(str(id_log))

    # Periksa apakah data distributor ada
    if not distributor_ref.get().exists:
        return jsonify({'error': 'Invalid id_log'}), 404

    # Update status
    distributor_ref.update({
        'status': new_status
    })

    return jsonify({'message': 'Status updated successfully', 'id_log': id_log, 'new_status': new_status})

@app.route('/api/distributors6/tb_fix_kirim_distributor', methods=['POST'])
def create_shipment():
    data = request.get_json()
    
    # Generate tracking number
    tracking_number = generate_tracking_number()

    # Simpan data shipment dengan tracking number
    new_shipment = {
        'id_log': data['id_log'],
        'berat': data['berat'],
        'harga_pengiriman': data['harga_pengiriman'],
        'kota_asal': data['kota_asal'].lower(),  # Lowercase kota_asal
        'kota_tujuan': data['kota_tujuan'].lower(),  # Lowercase kota_tujuan
        'lama_pengiriman': data['lama_pengiriman'],
        'no_resi': tracking_number,  # Auto-generated tracking number
        'quantity': data['quantity'],
        'status': data['status'],
        'tanggal_pembelian': data['tanggal_pembelian']
    }

    # Simpan new_shipment ke database
    db.collection('tb_fix_kirim_distributor').document(str(data['id_log'])).set(new_shipment)
    
    return jsonify({'message': 'Shipment created successfully', 'tracking_number': tracking_number})

@app.route('/api/distributors6/orders/delete', methods=['POST'])
def delete_order():
    data = request.get_json()
    id_log = data.get('id_log')

    # Periksa apakah dokumen dengan id_log ada di tb_fix_kirim_distributor
    distributor_ref = db.collection('tb_fix_kirim_distributor').document(str(id_log))

    if not distributor_ref.get().exists:
        return jsonify({'error': 'Invalid id_log'}), 404

    # Hapus dokumen dari tb_fix_kirim_distributor
    distributor_ref.delete()

    # Hapus juga dari tb_input_distributor jika perlu
    input_distributor_ref = db.collection('tb_input_distributor').document(str(id_log))
    input_distributor_ref.delete()

    return jsonify({'message': f'Order with id_log {id_log} deleted successfully'})

@app.route('/api/calculate-shipping-cost', methods=['POST'])
def api_calculate_shipping_cost():
    data = request.json
    kota_asal = data.get('kota_asal')
    kota_tujuan = data.get('kota_tujuan')
    berat = data.get('berat')

    print(f'Received data: kota_asal={kota_asal}, kota_tujuan={kota_tujuan}, berat={berat}')  # Untuk debugging

    if not kota_asal or not kota_tujuan or not berat:
        return jsonify({'error': 'Invalid data'}), 400

    # Hitung harga pengiriman
    harga_pengiriman = calculate_shipping_cost(kota_asal, kota_tujuan, berat)

    return jsonify({'harga_pengiriman': harga_pengiriman})



if __name__ == '__main__':
    # generate_dummy_data()  # Generate dummy data saat aplikasi dijalankan
    app.run(debug=True)

import streamlit as st
import pandas as pd
import uuid
from datetime import datetime
import cv2
from pyzbar.pyzbar import decode
from PIL import Image
import numpy as np
import qrcode
import io
import hashlib
import json

class Block:
    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_string = json.dumps({
            "index": self.index,
            "timestamp": self.timestamp,
            "data": self.data,
            "previous_hash": self.previous_hash
        }, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        return Block(0, datetime.now().isoformat(), "Genesis Block", "0")

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, data):
        previous_block = self.get_latest_block()
        new_block = Block(previous_block.index + 1, datetime.now().isoformat(), data, previous_block.hash)
        self.chain.append(new_block)

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i-1]
            if current_block.hash != current_block.calculate_hash():
                return False
            if current_block.previous_hash != previous_block.hash:
                return False
        return True

st.set_page_config(
    page_title="CICI - Cinnamon Intelligent Coating Innovation",
    layout="wide",
    page_icon="gambar/cici.jpeg",
    initial_sidebar_state="expanded"
)

# Custom CSS for better design
st.markdown("""
<style>
    .main-header {
        font-size: 2.5em;
        color: #2E8B57;
        text-align: center;
        margin-bottom: 20px;
    }
    .tab-content {
        padding: 20px;
        border-radius: 10px;
        background-color: #f9f9f9;
        margin-bottom: 20px;
    }
    .success-msg {
        background-color: #d4edda;
        color: #155724;
        padding: 10px;
        border-radius: 5px;
        margin: 10px 0;
    }
    .error-msg {
        background-color: #f8d7da;
        color: #721c24;
        padding: 10px;
        border-radius: 5px;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)



# Tampilkan gambar cici.jpeg di samping judul header
header_col1, header_col2 = st.columns([1, 6])
with header_col1:
    st.image("gambar/cici.jpeg", width=70)
with header_col2:
    st.markdown('<h1 class="main-header" style="margin-top: 15px;">CICI - Cinnamon Intelligent Coating Innovation</h1>', unsafe_allow_html=True)

# Inisialisasi data
if 'data' not in st.session_state:
    st.session_state['data'] = []
    # Tambahkan contoh data
    contoh_data = [
        {
            'produk_id': '123e4567-e89b-12d3-a456-426614174000',
            'tahap': 'Peternak',
            'data': {'peternak': 'Ahmad', 'asal_hewan': 'Farm A', 'jenis_pakan': 'Rumput', 'sertifikat_halal_pakan': 'Ya'},
            'timestamp': datetime.now().isoformat(),
            'batch_number': 'BATCH001',
            'expiry_date': '2026-12-31'
        },
        {
            'produk_id': '123e4567-e89b-12d3-a456-426614174000',
            'tahap': 'Transportasi',
            'data': {'transportir': 'Budi', 'jenis_kendaraan': 'Truck', 'kebersihan_kendaraan': 'Ya'},
            'timestamp': datetime.now().isoformat(),
            'batch_number': 'BATCH001',
            'expiry_date': '2026-12-31'
        },
        {
            'produk_id': '123e4567-e89b-12d3-a456-426614174000',
            'tahap': 'Rumah Potong',
            'data': {'rumah_potong': 'RPH Halal', 'juru_sembelih': 'Cici', 'proses_halal': 'Ya', 'sertifikat_halal_rph': 'Ya'},
            'timestamp': datetime.now().isoformat(),
            'batch_number': 'BATCH001',
            'expiry_date': '2026-12-31'
        }
    ]
    st.session_state['data'].extend(contoh_data)

if 'blockchain' not in st.session_state:
    st.session_state['blockchain'] = Blockchain()
    # Rebuild blockchain from data
    for entry in st.session_state['data']:
        st.session_state['blockchain'].add_block(entry)

# Sidebar navigation
st.sidebar.title("🐄 Menu Navigasi")
menu = st.sidebar.radio(
    "Pilih Fitur:",
    ["📝 Input Data", "🔍 Tracing Produk", "⛓️ Blockchain", "ℹ️ Informasi Sistem"],
    index=0
)

# Key Metrics
st.sidebar.markdown("---")
st.sidebar.subheader("📊 Statistik Sistem")
total_products = len(set(d['produk_id'] for d in st.session_state['data']))
total_entries = len(st.session_state['data'])
blockchain_valid = st.session_state['blockchain'].is_chain_valid()
st.sidebar.metric("Total Produk", total_products)
st.sidebar.metric("Total Entri", total_entries)
st.sidebar.metric("Blockchain Status", "Valid ✅" if blockchain_valid else "Invalid ❌")

st.sidebar.markdown("---")
st.sidebar.caption("Cinnamon Intelligent Coating Innovation v1.0")
st.sidebar.caption("Dikembangkan dengan Python, Streamlit & Blockchain")

# Main content based on menu
if menu == "📝 Input Data":
    st.header("📝 Input Data Tahapan Produk")
    col1, col2 = st.columns(2)
    with col1:
        tahap = st.selectbox("Tahap", [
            "Peternak", "Transportasi", "Rumah Potong", "Distribusi", "Konsumen"
        ])
        produk_id = st.text_input("ID Produk (kosongkan untuk produk baru)")
        batch_number = st.text_input("Nomor Batch (opsional)")
    with col2:
        if not produk_id:
            produk_id = str(uuid.uuid4())
        st.write(f"**ID Produk:** {produk_id}")
        expiry_date = st.date_input("Tanggal Kadaluarsa (opsional)")
    
    data_tahap = {}
    if tahap == "Peternak":
        col1, col2 = st.columns(2)
        with col1:
            data_tahap['peternak'] = st.text_input("Nama Peternak")
            data_tahap['asal_hewan'] = st.text_input("Asal Hewan")
        with col2:
            data_tahap['jenis_pakan'] = st.text_input("Jenis Pakan")
            data_tahap['sertifikat_halal_pakan'] = st.selectbox("Pakan Bersertifikat Halal?", ["Ya", "Tidak"])
    elif tahap == "Transportasi":
        col1, col2 = st.columns(2)
        with col1:
            data_tahap['transportir'] = st.text_input("Nama Transportir")
            data_tahap['jenis_kendaraan'] = st.text_input("Jenis Kendaraan")
        with col2:
            data_tahap['kebersihan_kendaraan'] = st.selectbox("Kebersihan Kendaraan Terjaga?", ["Ya", "Tidak"])
    elif tahap == "Rumah Potong":
        col1, col2 = st.columns(2)
        with col1:
            data_tahap['rumah_potong'] = st.text_input("Nama Rumah Potong")
            data_tahap['juru_sembelih'] = st.text_input("Nama Juru Sembelih")
        with col2:
            data_tahap['proses_halal'] = st.selectbox("Proses Penyembelihan Halal?", ["Ya", "Tidak"])
            data_tahap['sertifikat_halal_rph'] = st.selectbox("RPH Bersertifikat Halal?", ["Ya", "Tidak"])
    elif tahap == "Distribusi":
        col1, col2 = st.columns(2)
        with col1:
            data_tahap['distributor'] = st.text_input("Nama Distributor")
            data_tahap['jenis_paket'] = st.text_input("Jenis Paket/Box")
        with col2:
            data_tahap['suhu_penyimpanan'] = st.text_input("Suhu Penyimpanan")
    elif tahap == "Konsumen":
        data_tahap['nama_konsumen'] = st.text_input("Nama Konsumen")
        tanggal_terima = st.date_input("Tanggal Terima")
        data_tahap['tanggal_terima'] = str(tanggal_terima) if tanggal_terima else None
    
    if st.button("Simpan Data Tahap"):
        data_entry = {
            'produk_id': produk_id,
            'tahap': tahap,
            'data': data_tahap,
            'timestamp': datetime.now().isoformat(),
            'batch_number': batch_number if batch_number else None,
            'expiry_date': str(expiry_date) if expiry_date else None
        }
        st.session_state['data'].append(data_entry)
        st.session_state['blockchain'].add_block(data_entry)
        st.success(f"✅ Data tahap {tahap} untuk produk {produk_id} berhasil disimpan.")
        
        # Generate QR Code with complete data
        qr_data = {
            'produk_id': produk_id,
            'batch_number': batch_number,
            'expiry_date': str(expiry_date),
            'tahap': tahap,
            'data': data_tahap,
            'timestamp': data_entry['timestamp']
        }
        qr = qrcode.QRCode(
            version=None,  # Auto size
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(json.dumps(qr_data))
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        buf = io.BytesIO()
        img.save(buf, format='PNG')
        buf.seek(0)
        col1, col2 = st.columns([1, 2])
        with col1:
            st.image(buf, caption=f"QR Code untuk Produk ID: {produk_id}", width=150)
        with col2:
            st.download_button(label="📥 Download QR Code", data=buf.getvalue(), file_name=f"qr_{produk_id}.png", mime="image/png")
            st.code(json.dumps(qr_data, indent=2), language='json')

elif menu == "🔍 Tracing Produk":
    st.header("🔍 Tracing Produk Berdasarkan ID")
    col1, col2 = st.columns([1, 2])
    with col1:
        cari_id = st.text_input("Masukkan ID Produk untuk tracing")
        st.write("Atau scan QR Code:")
        qr_file = st.file_uploader("Upload gambar QR Code", type=["png", "jpg", "jpeg"])
        if qr_file is not None:
            img = Image.open(qr_file)
            img = img.convert('RGB')
            img_cv = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
            decoded_objs = decode(img_cv)
            if decoded_objs:
                qr_text = decoded_objs[0].data.decode("utf-8")
                try:
                    qr_data = json.loads(qr_text)
                    qr_id = qr_data.get('produk_id', qr_text)
                    st.success(f"✅ Data lengkap dari QR: ID {qr_id}")
                    st.json(qr_data)
                except json.JSONDecodeError:
                    qr_id = qr_text
                    st.success(f"✅ ID Produk dari QR: {qr_id}")
                cari_id = qr_id
            else:
                st.error("❌ QR Code tidak terbaca.")
    with col2:
        if cari_id:
            hasil = [d for d in st.session_state['data'] if d['produk_id'] == cari_id]
            if hasil:
                # Product Summary
                st.subheader("📋 Ringkasan Produk")
                product_info = hasil[0]  # Get basic info from first entry
                col_a, col_b = st.columns(2)
                with col_a:
                    st.write(f"**ID Produk:** {cari_id}")
                    if product_info.get('batch_number'):
                        st.write(f"**Batch:** {product_info['batch_number']}")
                with col_b:
                    if product_info.get('expiry_date'):
                        st.write(f"**Kadaluarsa:** {product_info['expiry_date']}")
                    stages_completed = len(set(h['tahap'] for h in hasil))
                    st.write(f"**Tahapan Terekam:** {stages_completed}/5")
                
                # Check halal compliance for this product
                halal_stages = 0
                total_stages = len(hasil)
                for h in hasil:
                    data = h['data']
                    if isinstance(data, dict):
                        halal_fields = [v for k, v in data.items() if 'halal' in k.lower()]
                        if halal_fields and all(str(v) == 'Ya' for v in halal_fields):
                            halal_stages += 1
                    else:
                        # If data is not dict, assume not halal
                        pass
                
                compliance = (halal_stages / total_stages * 100) if total_stages > 0 else 0
                if compliance == 100:
                    st.success(f"✅ Produk Halal (Kepatuhan: {compliance:.0f}%)")
                elif compliance > 0:
                    st.warning(f"⚠️ Kepatuhan Halal Parsial ({compliance:.0f}%)")
                else:
                    st.error(f"❌ Tidak Halal (Kepatuhan: {compliance:.0f}%)")
                
                st.markdown("---")
                st.subheader("📍 Riwayat Produk:")
                for h in hasil:
                    with st.expander(f"📍 Tahap: {h['tahap']}"):
                        if h.get('batch_number'):
                            st.write(f"**Batch:** {h['batch_number']}")
                        if h.get('expiry_date'):
                            st.write(f"**Kadaluarsa:** {h['expiry_date']}")
                        st.json(h['data'])
                        st.caption(f"⏰ Waktu input: {h['timestamp']}")
            else:
                st.warning("⚠️ Data tidak ditemukan untuk ID tersebut.")
                st.info("Pastikan ID produk sudah benar dan data telah diinput dalam sistem.")

elif menu == "⛓️ Blockchain":
    st.header("⛓️ Blockchain")
    is_valid = st.session_state['blockchain'].is_chain_valid()
    if is_valid:
        st.success("✅ Blockchain Valid")
    else:
        st.error("❌ Blockchain Tidak Valid")
    
    # Display as DataFrame
    chain_data = []
    for block in st.session_state['blockchain'].chain:
        if isinstance(block.data, dict):
            tahap = block.data.get('tahap', 'Genesis')
            pid = block.data.get('produk_id', '')[:8] if block.data.get('produk_id') else ''
        else:
            tahap = 'Genesis'
            pid = ''
        chain_data.append({
            'Index': block.index,
            'Hash': block.hash[:16] + '...',  # Shorten hash for display
            'Previous Hash': block.previous_hash[:16] + '...' if block.previous_hash != '0' else '0',
            'Timestamp': block.timestamp,
            'Data Summary': f"{tahap} - {pid}..."
        })
    
    df = pd.DataFrame(chain_data)
    st.dataframe(df, use_container_width=True)
    
    # Option to view full details
    selected_block = st.selectbox("Pilih Block untuk detail lengkap:", [f"Block {b.index}" for b in st.session_state['blockchain'].chain])
    if selected_block:
        idx = int(selected_block.split()[1])
        block = st.session_state['blockchain'].chain[idx]
        st.subheader(f"Detail {selected_block}")
        st.write("**Hash:**", block.hash)
        st.write("**Previous Hash:**", block.previous_hash)
        st.write("**Timestamp:**", block.timestamp)
        if isinstance(block.data, dict):
            st.json(block.data)
        else:
            st.write("**Data:**", block.data)

elif menu == "ℹ️ Informasi Sistem":
    st.header("ℹ️ Informasi Sistem")
    st.markdown("""
    ### CICI - Cinnamon Intelligent Coating Innovation
    
    **Deskripsi:**
    Sistem ini dirancang untuk melacak produk peternakan halal dari peternak hingga konsumen menggunakan teknologi blockchain untuk memastikan integritas data.
    
    **Fitur Utama:**
    - 📝 **Input Data**: Masukkan data tahapan produk dengan QR code otomatis
    - 🔍 **Tracing Produk**: Lacak riwayat produk berdasarkan ID atau QR code
    - ⛓️ **Blockchain**: Lihat rantai blok untuk verifikasi integritas data
    - 📊 **Statistik Real-time**: Pantau jumlah produk dan entri
    
    **Teknologi:**
    - **Frontend**: Streamlit
    - **Database**: CSV file
    - **Blockchain**: Implementasi sederhana dengan SHA-256 hashing
    - **QR Code**: Generasi dan scanning menggunakan qrcode dan pyzbar
    
    **Keamanan:**
    - Data tersimpan dalam format CSV
    - Blockchain memastikan data tidak dapat diubah tanpa deteksi
    - QR code untuk identifikasi produk yang mudah
    
    **Cara Penggunaan:**
    1. Pilih menu Input Data untuk menambah data produk
    2. Sistem akan generate QR code otomatis
    3. Gunakan Tracing untuk memverifikasi produk
    4. Lihat Blockchain untuk audit trail
    
    **Kontak:**
    Untuk pertanyaan atau dukungan, hubungi administrator sistem.
    """)
    
    # Additional system info
    st.subheader("🔧 Detail Teknis")
    col1, col2 = st.columns(2)
    with col1:
        st.write("**Versi Python:**", "3.13")
        st.write("**Library Utama:**", "Streamlit, Pandas, OpenCV")
    with col2:
        st.write("**Blockchain Blocks:**", len(st.session_state['blockchain'].chain))
        st.write("**Data File:**", "data.csv")
    
    st.subheader("📈 Ringkasan Kepatuhan Halal")
    from collections import defaultdict
    
    # Group data by product ID
    products = defaultdict(list)
    for d in st.session_state['data']:
        products[d['produk_id']].append(d)
    
    halal_products = 0
    total_products = len(products)
    
    for pid, entries in products.items():
        # Check if all stages have halal compliance
        is_halal = True
        for entry in entries:
            data = entry['data']
            if isinstance(data, dict):
                halal_fields = [v for k, v in data.items() if 'halal' in k.lower()]
                if not halal_fields or not all(str(v) == 'Ya' for v in halal_fields):
                    is_halal = False
                    break
            else:
                is_halal = False
                break
        if is_halal:
            halal_products += 1
    
    if total_products > 0:
        compliance_rate = (halal_products / total_products) * 100
        st.metric("Tingkat Kepatuhan Halal", f"{compliance_rate:.1f}%", 
                 f"{halal_products}/{total_products} produk")
        
        # Add warning if low compliance
        if compliance_rate < 80:
            st.warning("⚠️ Tingkat kepatuhan halal rendah. Periksa sertifikasi produk.")
        else:
            st.success("✅ Tingkat kepatuhan halal baik.")
    else:
        st.metric("Tingkat Kepatuhan Halal", "0%")
        st.info("Belum ada data produk.")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 20px;">
    <p>© 2026 CICI - Cinnamon Intelligent Coating Innovation</p>
    <p><em>Bismillah Cukurucoat Menang - Fakultas Peternakan UGM</em></p>
</div>
""", unsafe_allow_html=True)

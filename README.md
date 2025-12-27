# PROYEK ELEARNING V1

**PROYEK INI MASIH DALAM PENGEMBANGAN**


## DIBUAT OLEH:

    La Ati ( 23650231 )
    Backend Developer
        
    Dyah Chandra Priyanka ( 22650156 )
    UI/UX & Frontend Developer

## Framework
- Flask

## Database
- Support PostgreSQL & Serverless PostgreSQL seperti Supabase

## Migrasi Database
Sebelum migrasi, pastikan `migrate.init_app(app, db)` pada `main.py` aktif (untuk production).

### Jika projek baru:

    export FLASK_APP=main.py
    flask db init
    flask db migrate -m "initial migration"
    flask db upgrade

### jika sudah beberapa kali migrasi:

    export FLASK_APP=main.py
    flask db migrate -m "initial migration"
    flask db upgrade

## run:

    flask --app main.py run

## Alur kerja sistem:    
Dosen memanajemen (CRUD) kelas dan matakuliah nya masing masing
Mahasiswa dapat melakukan join kelas semua DOSEN


## Demo Proyek: 
    https://elearning.butonvalley.com
    
    Dosen: 
        email: dosen1@gmail.com
        password: 12345
        
    Mahasiswa: 
        email: mahasiswa1@gmail.com
        password: 12345

# UPDATE: PROYEK ELEARNING V1.1

## Role Dosen
- **Fitur Tugas Kelas**
  - Tambah tugas
  - Periksa jawaban mahasiswa

## Role Mahasiswa
- **Fitur Tugas Kelas**
  - Lihat semua tugas kelas
  - Kirim jawaban tugas kelas
  - Jika jawaban tugas kelas sudah dikirim, form kirim jawaban berubah menjadi label **CEKLIST Telah Dikirim**, jika sudah diberi nilai maka akan berubah menjadi label **Nilai: (nominal nilai)**
- **Fitur IPK Kelas**
  - IPK kelas merupakan jumlah keseluruhan nilai tugas kelas dibagi dengan jumlah tugas kelas

### Notes
- Next Update V1.3 (Pengelolaan File Tugas dan Jawaban Tugas ke Serverless Storage)
- Code program pada Fitur Tugas dapat dilihat pada timeline commit
    
    
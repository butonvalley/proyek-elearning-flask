PROYEK ELEARNING V1.0

Framework:
Flask

DATABASE:
suppoert Postgresql & Serveless postgresql seperti supabase


migrations:
    export FLASK_APP=main.py
    flask db init
    flask db migrate -m "initial migration"
    flask db upgrade


run:
    flask --app main.py run

Alur kerja sistem:    
    Dosen memanajemen (CRUD) kelas dan matakuliah nya masing masing
    Mahasiswa dapat melakukan join kelas serta matakuliah semua DOSEN

DIBUAT OLEH:

    La Ati ( 22650156 )
    Backend Developer
        
    Dyah Chandra Priyanka ( 22650156 )
    UI/UX & Frontend Developer


PROYEK INI MASIH DALAM PENGEMBANGAN

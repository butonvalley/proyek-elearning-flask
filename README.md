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


PROYEK INI MASIH DALAM PENGEMBANGAN
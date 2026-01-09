import os
import uuid
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_user,current_user,login_required,logout_user
from configs.db import db
from forms.dosen_form import DosenForm
from forms.kelas_form import KelasForm
from forms.kelas_mahasiswa_form import KelasMahasiswaForm
from forms.login_form import LoginForm
from forms.logout_form import LogoutForm
from forms.mahasiswa_form import MahasiswaForm
from forms.matakuliah_form import MataKuliahForm
from forms.materi_form import MateriForm
from forms.register_form import RegisterForm
from forms.tugas_form import TugasForm
from forms.tugas_mahasiswa_form import TugasMahasiswaForm
from models.dosen import Dosen
from models.kelas import Kelas
from models.kelas_mahasiswa import KelasMahasiswa
from models.mahasiswa import Mahasiswa
from models.matakuliah import MataKuliah
from models.materi import Materi
from models.tugas import Tugas
from models.tugas_mahasiswa import TugasMahasiswa
from models.user import User

from werkzeug.security import generate_password_hash,check_password_hash

from utils.generator import generate_unique_username

from sqlalchemy.orm import aliased
from datetime import datetime,timezone

from utils.supabase_client import delete_file_storage_supabase, upload_file_storage_supabase

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
@login_required
def home_view():
    #pada pengembangan versi selanjutnya buatkan form_logout sebagai context global 
    form_logout = LogoutForm()

    # ======================
    # JIKA DOSEN
    # ======================
    if getattr(current_user, "dosen", None):
        dosen = current_user.dosen

        # semua matakuliah milik dosen
        matakuliah = MataKuliah.query.filter_by(
            dosen_id=dosen.id
        ).all()

        # semua kelas dari matakuliah dosen
        kelas = (
            Kelas.query
            .join(MataKuliah)
            .filter(MataKuliah.dosen_id == dosen.id)
            .all()
        )

        return render_template(
            "profil_dosen.html",
            form_logout=form_logout,
            matakuliah=matakuliah,
            kelas=kelas
        )

    # ======================
    # JIKA MAHASISWA
    # ======================
    if getattr(current_user, "mahasiswa", None):

        # semua matakuliah (global)
        matakuliah = MataKuliah.query.all()

        # semua kelas (global)
        kelas = Kelas.query.all()

        return render_template(
            "profil_mahasiswa.html",
            form_logout=form_logout,
            matakuliah=matakuliah,
            kelas=kelas
        )

    # ======================
    # BELUM PUNYA ROLE
    # ======================
    return redirect(url_for("main.register_data_mahasiswa_view"))

@main_bp.route("/join-kelas/<id>")
@login_required
def join_kelas_view(id):
    form_logout = LogoutForm()

    # ======================
    # JIKA DOSEN
    # ======================
    if getattr(current_user, "dosen", None):
        dosen = current_user.dosen

        # ambil kelas berdasarkan slug dan pastikan milik dosen
        kelas = Kelas.query.join(MataKuliah).filter(
            Kelas.id == id,
            MataKuliah.dosen_id == dosen.id
        ).first()

        if not kelas:
            flash("Anda tidak punya hak akses ke kelas ini.", "error")
            return redirect(url_for("main.home_view"))
        
        km = KelasMahasiswa.query.filter_by(
            kelas_id=kelas.id
        ).all()
        form_kelas_mahasiswa = KelasMahasiswaForm()
        form_tugas= TugasForm()
        tugas_kelas = Tugas.query.filter_by(kelas_id = kelas.id).all()

        form_materi= MateriForm()
        materi_kelas = Materi.query.filter_by(kelas_id = kelas.id).all()
      
        return render_template(
            "join_kelas_dosen.html",
            form_logout=form_logout,
            kelas=kelas,
            kelas_mahasiswa = km,
            tugas_kelas = tugas_kelas,
            kelas_mahasiswa_form = form_kelas_mahasiswa,
            form_tugas=form_tugas,
            form_materi=form_materi,
            materi_kelas=materi_kelas
        )

    # ======================
    # JIKA MAHASISWA
    # ======================
    if getattr(current_user, "mahasiswa", None):
        mahasiswa = current_user.mahasiswa

        # ambil kelas berdasarkan slug
        kelas = Kelas.query.filter_by(id=id).first()
        if not kelas:
            flash("Kelas tidak ditemukan.", "error")
            return redirect(url_for("main.home_view"))

        # cek apakah mahasiswa sudah terdaftar di kelas
        km = KelasMahasiswa.query.filter_by(
            kelas_id=kelas.id,
            mahasiswa_id=mahasiswa.id
        ).first()

        if not km:
            # otomatis tambah mahasiswa ke kelas
            km = KelasMahasiswa(kelas_id=kelas.id, mahasiswa_id=mahasiswa.id)
            db.session.add(km)
            db.session.commit()
            flash(f"Anda berhasil bergabung di {kelas.nama}", "success")
        else:
            flash(f"Anda sudah terdaftar di {kelas.nama}", "info")
        
        Jawaban = aliased(TugasMahasiswa)

        tugas_kelas = (
            db.session.query(Tugas, Jawaban)
            .outerjoin(
                Jawaban,
                (Jawaban.tugas_id == Tugas.id) &
                (Jawaban.mahasiswa_id == mahasiswa.id)
            )
            .filter(Tugas.kelas_id == kelas.id)
            .all()
        )

        total_tugas = len(tugas_kelas)

        total_nilai = sum(
            jawaban.nilai
            for _, jawaban in tugas_kelas
            if jawaban and jawaban.nilai is not None
        )

        if total_tugas > 0:
            nilai_ipk_kelas = total_nilai / total_tugas
        else:
            nilai_ipk_kelas = 0

        form_tugas = TugasMahasiswaForm()
        materi_kelas = Materi.query.filter_by(kelas_id = kelas.id).all()

        return render_template(
            "join_kelas_mahasiswa.html",
            form_logout=form_logout,
            kelas=kelas,
            tugas_kelas = tugas_kelas,
            nilai_ipk_kelas=round(nilai_ipk_kelas, 2),
            form_tugas = form_tugas,
            materi_kelas=materi_kelas,
            tanggal_hari_ini=datetime.now(timezone.utc).replace(tzinfo=None)
        )

    # ======================
    # BELUM PUNYA ROLE
    # ======================
    return redirect(url_for("main.register_data_mahasiswa_view"))

@main_bp.route("/kelas-mahasiswa-update", methods=["POST"])
@login_required
def kelas_mahasiswa_update():
    form = KelasMahasiswaForm()

    # ==========================
    # CEK ROLE DOSEN
    # ==========================
    dosen = getattr(current_user, "dosen", None)
    if not dosen:
        flash("Akses ditolak", "error")
        return redirect(url_for("main.home_view"))

    # ==========================
    # VALIDASI FORM
    # ==========================
    if not form.validate_on_submit():
        flash("Data tidak valid", "error")
        return redirect(request.referrer)

    try:
        kelas_mahasiswa_id = request.form.get("kelas_mahasiswa_id")

        km = KelasMahasiswa.query.get(kelas_mahasiswa_id)
        if not km:
            flash("Data kelas mahasiswa tidak ditemukan", "error")
            return redirect(request.referrer)

        # ==========================
        # CEK KEPEMILIKAN KELAS
        # ==========================
        if km.kelas.matakuliah.dosen_id != dosen.id:
            flash("Anda tidak berhak mengubah data ini", "error")
            return redirect(url_for("main.home_view"))

        # ==========================
        # UPDATE DATA
        # ==========================
        km.nilai_akhir = form.nilai_akhir.data
        km.status = "Selesai"

        db.session.commit()
        flash("Data mahasiswa berhasil diperbarui", "success")

    except Exception as e:
        db.session.rollback()
        flash("Terjadi kesalahan saat update data", "error")
        print(e)

    return redirect(request.referrer)

@main_bp.route("/login", methods=["GET", "POST"])
def login_view():
    if current_user.is_authenticated:
        # Redirect sesuai role
        if hasattr(current_user, "dosen") and current_user.dosen:
            return redirect(url_for("main.home_view"))
        elif hasattr(current_user, "mahasiswa") and current_user.mahasiswa:
            return redirect(url_for("main.home_view"))
        else:
            return redirect(url_for("main.register_data_mahasiswa_view"))
        
    form = LoginForm()

    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        user = User.query.filter_by(email=email).first()
        if not user:
            flash("Login Gagal Periksa Email atau Password anda", "error")
            return redirect(url_for("main.login_view"))

        if not user.is_active:
            flash("Akun tidak aktif", "error")
            return redirect(url_for("main.login_view"))

        if not check_password_hash(user.password, password):
            flash("Login Gagal Periksa Email atau Password anda", "error")
            return redirect(url_for("main.login_view"))

        # login sukses
        login_user(user)

         # redirect berdasarkan role
        if (hasattr(user, "dosen") and user.dosen) or (hasattr(user, "mahasiswa") and user.mahasiswa):
            return redirect(url_for("main.home_view"))

     
        #user belum punya role
        return redirect(url_for("main.register_data_mahasiswa_view"))

    return render_template("login.html", form=form)

@main_bp.route("/register", methods=["GET", "POST"])
def register_view():
    form = RegisterForm()

    if form.validate_on_submit():
        email = form.email.data
        # cek username sudah ada
        if User.query.filter_by(email=email).first():
            flash("Email sudah digunakan", "error")
            return redirect(url_for("main.register_view"))
      
        try:
            # buat user
            user = User(
                fullname=form.fullname.data,
                email=email,
                username=generate_unique_username(email),
                password=generate_password_hash(form.password.data),
                is_active=True,
                is_superuser=False
            )
            db.session.add(user)
            db.session.flush()  
            # flush agar user.id tersedia tanpa commit

            # commit
            db.session.commit()

            flash("Registrasi berhasil, silakan login", "success")
            return redirect(url_for("main.login_view"))

        except Exception as e:
            db.session.rollback()
            flash("Terjadi kesalahan saat registrasi", "error")
            print(e)

    return render_template("register.html", form=form)

@main_bp.route("/register-data-mahasiswa", methods=["GET", "POST"])
@login_required
def register_data_mahasiswa_view():
    form = MahasiswaForm()

    # cek apakah user sudah punya Mahasiswa
    mahasiswa = getattr(current_user, "mahasiswa", None)

    if form.validate_on_submit():
        try:
            if not mahasiswa:
                # create new Mahasiswa
                mahasiswa = Mahasiswa(
                    id=str(uuid.uuid4()),
                    user_id=current_user.id,
                    nim=form.nim.data,
                    alamat=form.alamat.data,
                    angkatan=form.angkatan.data
                )
                db.session.add(mahasiswa)
            else:
                # update existing
                mahasiswa.nim = form.nim.data
                mahasiswa.alamat = form.alamat.data
                mahasiswa.angkatan = form.angkatan.data

            db.session.commit()
            flash("Data Mahasiswa berhasil disimpan", "success")
            return redirect(url_for("main.home_view"))

        except Exception as e:
            db.session.rollback()
            flash("Terjadi kesalahan saat menyimpan Data Mahasiswa", "error")
            print(e)

    # jika mahasiswa sudah ada, isi default form
    if mahasiswa and request.method == "GET":
        form.nim.data = mahasiswa.nim
        form.alamat.data = mahasiswa.alamat
        form.angkatan.data = mahasiswa.angkatan

    return render_template("register_data_mahasiswa.html", form=form)

@main_bp.route("/register-data-dosen", methods=["GET", "POST"])
@login_required
def register_data_dosen_view():
    form = DosenForm()
    

    # cek apakah user sudah punya Dosen
    dosen = getattr(current_user, "dosen", None)

    if form.validate_on_submit():
        try:
            if not dosen:
                # create new Dosen
                dosen = Dosen(
                    id=str(uuid.uuid4()),
                    user_id=current_user.id,
                    nidn=form.nidn.data,
                    matakuliah=form.matakuliah.data
                )
                db.session.add(dosen)
            else:
                # update existing
                dosen.nidn = form.nidn.data
                dosen.matakuliah = form.matakuliah.data

            # update matakuliah
            selected_ids = form.matakuliah.data  # list of string
            matakuliah_objs = MataKuliah.query.filter(MataKuliah.id.in_(selected_ids)).all()
            dosen.matakuliah = matakuliah_objs

            db.session.commit()
            flash("Data Dosen berhasil disimpan", "success")
            return redirect(url_for("main.home_view"))

        except Exception as e:
            db.session.rollback()
            flash("Terjadi kesalahan saat menyimpan Data Dosen", "error")
            print(e)

    # jika dosen sudah ada, isi default form
    if dosen and request.method == "GET":
        form.nidn.data = dosen.nidn
        
    return render_template("register_data_dosen.html", form=form)

@main_bp.route("/logout", methods=["POST"])
@login_required
def logout_view():
    form = LogoutForm()
    if form.validate_on_submit():
        logout_user()
        flash("Anda berhasil logout.", "success")
        return redirect(url_for("main.login_view"))

    return redirect(url_for("main.home_view"))

@main_bp.route("/tambah-kelas", methods=["GET", "POST"])
@login_required
def add_kelas_view():
    form_logout = LogoutForm()
    form = KelasForm()

    #hanya dosen yang boleh
    dosen = getattr(current_user, "dosen", None)
    if not dosen:
        flash("Akses ditolak. Hanya dosen yang dapat menambah kelas.", "error")
        return redirect(url_for("main.home_view"))

    # hanya matakuliah milik dosen
    form.matakuliah_id.choices = [
        (mk.id, f"{mk.kode} - {mk.nama}")
        for mk in dosen.matakuliah
    ]

    if form.validate_on_submit():
        try:
            kelas = Kelas(
                nama=form.nama.data,
                semester=form.semester.data,
                tahun_ajaran=form.tahun_ajaran.data,
                matakuliah_id=form.matakuliah_id.data
            )

            db.session.add(kelas)
            db.session.commit()

            flash("Data Kelas berhasil disimpan", "success")
            return redirect(url_for("main.home_view"))

        except Exception as e:
            db.session.rollback()
            flash("Terjadi kesalahan saat menyimpan Data Kelas", "error")
            print(e)

    return render_template("tambah_kelas.html", form_logout = form_logout,form=form)

@main_bp.route("/tambah-matakuliah", methods=["GET", "POST"])
@login_required
def add_matakuliah_view():
    form = MataKuliahForm()

    # hanya dosen
    dosen = getattr(current_user, "dosen", None)
    if not dosen:
        flash("Akses ditolak. Hanya dosen yang dapat menambah Mata Kuliah.", "error")
        return redirect(url_for("main.home_view"))

    if form.validate_on_submit():
        try:
            matakuliah = MataKuliah(
                kode=form.kode.data,
                nama=form.nama.data,
                sks=form.sks.data,
                dosen_id=dosen.id   
            )

            db.session.add(matakuliah)
            db.session.commit()

            flash("Mata Kuliah berhasil ditambahkan", "success")
            return redirect(url_for("main.home_view"))

        except Exception as e:
            db.session.rollback()
            flash("Terjadi kesalahan saat menambah Mata Kuliah", "error")
            print(e)

    return render_template("tambah_matakuliah.html", form_logout = LogoutForm(), form=form)

@main_bp.route("/kelas/<kelas_id>/tugas/tambah", methods=["GET", "POST"])
@login_required
def tambah_tugas(kelas_id):
    dosen = getattr(current_user, "dosen", None)
    if not dosen:
        flash("Akses ditolak", "error")
        return redirect(url_for("main.home_view"))

    kelas = Kelas.query.get_or_404(kelas_id)
    form = TugasForm()

    if form.validate_on_submit():
        filename = None
        if form.file_tugas.data:
                     
            filename = upload_file_storage_supabase(
                form.file_tugas.data,
                os.environ.get("SUPABASE_BUCKET_TUGAS")
            )
           
        tugas = Tugas(
            kelas_id=kelas.id,
            dosen_id=dosen.id,
            judul=form.judul.data,
            deskripsi=form.deskripsi.data,
            file_tugas=filename,
            deadline=form.deadline.data
        )
        db.session.add(tugas)
        db.session.commit()

        flash("Tugas berhasil diupload", "success")
        return redirect(url_for("main.join_kelas_view", id=kelas.id))

    form_logout = LogoutForm()
    return render_template("tambah_tugas.html", form=form, kelas=kelas,form_logout=form_logout)

@main_bp.route("/kelas/<kelas_id>/tugas/<tugas_id>/hapus", methods=["POST"])
@login_required
def hapus_tugas(kelas_id, tugas_id):
    # ======================
    # CEK ROLE DOSEN
    # ======================
    dosen = getattr(current_user, "dosen", None)
    if not dosen:
        flash("Akses ditolak", "error")
        return redirect(url_for("main.home_view"))

    # ======================
    # AMBIL TUGAS
    # ======================
    tugas = Tugas.query.get_or_404(tugas_id)

    # ======================
    # VALIDASI KEPEMILIKAN
    # ======================
    if tugas.dosen_id != dosen.id or tugas.kelas_id != kelas_id:
        flash("Anda tidak memiliki hak untuk menghapus tugas ini", "error")
        return redirect(url_for("main.join_kelas_view", id=kelas_id))

    try:
        # ======================
        # HAPUS FILE DI SUPABASE
        # ======================
        if tugas.file_tugas:
            delete_file_storage_supabase(
                os.environ.get("SUPABASE_BUCKET_TUGAS"),
                tugas.file_tugas
            )

        # ======================
        # HAPUS DATABASE
        # ======================
        db.session.delete(tugas)
        db.session.commit()

        flash("Tugas berhasil dihapus", "success")

    except Exception as e:
        db.session.rollback()
        flash(f"Gagal menghapus tugas: {str(e)}", "error")

    return redirect(url_for("main.join_kelas_view", id=kelas_id))

#upload Jawaban oleh Mahasiswa
@main_bp.route("/tugas/<tugas_id>/jawaban", methods=["POST"])
@login_required
def upload_jawaban(tugas_id):
    mahasiswa = getattr(current_user, "mahasiswa", None)
    if not mahasiswa:
        flash("Akses ditolak", "error")
        return redirect(url_for("main.home_view"))

    tugas = Tugas.query.get_or_404(tugas_id)
    form = TugasMahasiswaForm()

    if form.validate_on_submit():
        filename = None
        if form.file_jawaban.data:
                     
            filename = upload_file_storage_supabase(
                form.file_jawaban.data,
                os.environ.get("SUPABASE_BUCKET_JAWABAN")
            )

        jawaban = TugasMahasiswa(
            tugas_id=tugas.id,
            mahasiswa_id=mahasiswa.id,
            file_jawaban=filename
        )
        db.session.add(jawaban)
        db.session.commit()

        flash("Jawaban berhasil dikumpulkan", "success")

    return redirect(url_for("main.join_kelas_view", id=tugas.kelas_id))

#Hapus Jawaban oleh Mahasiswa
@main_bp.route("/tugas/<tugas_id>/hapus", methods=["POST"])
@login_required
def hapus_jawaban(tugas_id):
    # ======================
    # CEK ROLE MAHASISWA
    # ======================
    mahasiswa = getattr(current_user, "mahasiswa", None)
    if not mahasiswa:
        flash("Akses ditolak", "error")
        return redirect(url_for("main.home_view"))

    tugas = Tugas.query.get_or_404(tugas_id)
    if not tugas:
        flash("Akses ditolak", "error")
        return redirect(url_for("main.home_view"))

    # ======================
    # AMBIL JAWABAN
    # ======================
    jawaban = TugasMahasiswa.query.filter(TugasMahasiswa.tugas_id == tugas_id,
        TugasMahasiswa.mahasiswa_id == mahasiswa.id).first_or_404()

   
    try:
        # ======================
        # HAPUS FILE DI SUPABASE
        # ======================
        if jawaban.file_jawaban:
            delete_file_storage_supabase(
                os.environ.get("SUPABASE_BUCKET_JAWABAN"),
                jawaban.file_jawaban
            )

        # ======================
        # HAPUS DATABASE
        # ======================
        db.session.delete(jawaban)
        db.session.commit()

        flash("Jawaban berhasil dihapus", "success")

    except Exception as e:
        db.session.rollback()
        flash(f"Gagal menghapus jawaban: {str(e)}", "error")

    return redirect(url_for("main.join_kelas_view", id=tugas.kelas_id))

#periksa tugas oleh dosen
@main_bp.route("/kelas/<kelas_id>/tugas/<tugas_id>/periksa", methods=["GET", "POST"])
@login_required
def periksa_jawaban_tugas(kelas_id, tugas_id):
    form_logout = LogoutForm()

    # ======================
    # VALIDASI DOSEN
    # ======================
    dosen = getattr(current_user, "dosen", None)
    if not dosen:
        flash("Akses ditolak. Hanya dosen yang dapat mengakses halaman ini.", "error")
        return redirect(url_for("main.home_view"))

    # ======================
    # AMBIL KELAS & TUGAS
    # ======================
    kelas = Kelas.query.filter_by(id=kelas_id).first_or_404()
    tugas = Tugas.query.filter_by(id=tugas_id, kelas_id=kelas.id).first_or_404()

    # Pastikan tugas milik dosen tersebut
    if tugas.dosen_id != dosen.id:
        flash("Anda tidak memiliki hak atas tugas ini.", "error")
        return redirect(url_for("main.join_kelas_view", id=kelas.id))

    # ======================
    # POST → UPDATE NILAI
    # ======================
    if request.method == "POST":
        jawaban_id = request.form.get("jawaban_id")
        nilai = request.form.get("nilai")

        jawaban = TugasMahasiswa.query.filter_by(
            id=jawaban_id,
            tugas_id=tugas.id
        ).first()

        if jawaban:
            jawaban.nilai = float(nilai)
            db.session.commit()
            flash("Nilai berhasil disimpan.", "success")
        else:
            flash("Data jawaban tidak ditemukan.", "error")

        return redirect(
            url_for("main.periksa_jawaban_tugas", kelas_id=kelas.id, tugas_id=tugas.id)
        )

    # ======================
    # GET → AMBIL JAWABAN
    # ======================
    jawaban_mahasiswa = (
        TugasMahasiswa.query
        .filter_by(tugas_id=tugas.id)
        .join(Mahasiswa)
        .all()
    )
    form_tugas_mahasiswa = TugasMahasiswaForm()
    return render_template(
        "periksa_tugas.html",
        kelas=kelas,
        tugas=tugas,
        jawaban_mahasiswa=jawaban_mahasiswa,
        form_tugas_mahasiswa=form_tugas_mahasiswa,
        form_logout=form_logout
    )

@main_bp.route("/kelas/<kelas_id>/materi/tambah", methods=["GET", "POST"])
@login_required
def tambah_materi(kelas_id):
    dosen = getattr(current_user, "dosen", None)
    if not dosen:
        flash("Akses ditolak", "error")
        return redirect(url_for("main.home_view"))
    
    kelas = Kelas.query.get_or_404(kelas_id)
    if not kelas:
        flash("Kelas tidak ditemukan", "error")
        return redirect(url_for("main.join_kelas_view",id=kelas_id))
    
    form = MateriForm()
    if form.validate_on_submit():
        file_url = None
        if form.file.data:
            # gunakan fungsi upload supabase (sesuaikan bucket)
            file_url = upload_file_storage_supabase(
                form.file.data, os.environ.get("SUPABASE_BUCKET_MATERI")
            )

        materi = Materi(
            kelas_id=kelas_id,
            dosen_id=dosen.id,
            judul=form.judul.data,
            deskripsi=form.deskripsi.data,
            link_eksternal=form.link_eksternal.data,
            file=file_url
        )
        db.session.add(materi)
        db.session.commit()

        flash("Materi berhasil ditambahkan", "success")
        return redirect(url_for("main.join_kelas_view", id=kelas_id))
    form_logout = LogoutForm()
    return render_template("tambah_materi.html", form=form, kelas=kelas,form_logout=form_logout)

@main_bp.route("/kelas/<kelas_id>/materi/<materi_id>/hapus", methods=["POST"])
@login_required
def hapus_materi(kelas_id, materi_id):
    # ======================
    # CEK ROLE DOSEN
    # ======================
    dosen = getattr(current_user, "dosen", None)
    if not dosen:
        flash("Akses ditolak", "error")
        return redirect(url_for("main.home_view"))

    # ======================
    # AMBIL MATERI
    # ======================
    materi = Materi.query.get_or_404(materi_id)

    # ======================
    # VALIDASI KEPEMILIKAN
    # ======================
    if materi.dosen_id != dosen.id or materi.kelas_id != kelas_id:
        flash("Anda tidak memiliki hak untuk menghapus tugas ini", "error")
        return redirect(url_for("main.join_kelas_view", id=kelas_id))

    try:
        # ======================
        # HAPUS FILE DI SUPABASE
        # ======================
        if materi.file:
            delete_file_storage_supabase(
                os.environ.get("SUPABASE_BUCKET_MATERI"),
                materi.file
            )

        # ======================
        # HAPUS DATABASE
        # ======================
        db.session.delete(materi)
        db.session.commit()

        flash("Materi berhasil dihapus", "success")

    except Exception as e:
        db.session.rollback()
        flash(f"Gagal menghapus tugas: {str(e)}", "error")

    return redirect(url_for("main.join_kelas_view", id=kelas_id))

#Tentang - Syarat dan Ketentuan dalam pengembangan tahap selanjutnya diganti dengan model dan form PAGE
@main_bp.route("/tentang-kami")
def about_view():
    form = LogoutForm()
    return render_template("tentang.html",form_logout=form)

@main_bp.route("/syarat-ketentuan")
def tos_view():
    form = LogoutForm()
    return render_template("syarat.html",form_logout=form)

@main_bp.route("/page/<slug>")
def page_view():   
    return render_template("page.html")
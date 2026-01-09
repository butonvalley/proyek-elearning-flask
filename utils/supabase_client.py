import uuid
from supabase import create_client
import os
from werkzeug.utils import secure_filename

supabase_client = create_client(os.environ.get('SUPABASE_URL'), os.environ.get('SUPABASE_SECRET_KEY'))

def upload_file_storage_supabase(file, bucket: str):
    
    try:
        # Nama file aman
        original_filename = secure_filename(file.filename)

        if not original_filename:
            raise Exception("Nama file tidak valid")

        # Ambil ekstensi
        ext = os.path.splitext(original_filename)[1]

        # Nama file random
        file_path = f"{uuid.uuid4()}{ext}"

        # Baca file
        file_bytes = file.read()

        # Content-Type otomatis
        content_type = file.mimetype or "application/octet-stream"

        supabase_client.storage.from_(bucket).upload(
            file_path,
            file_bytes,
            {
                "content-type": content_type
            }
        )

        public_url = supabase_client.storage.from_(bucket).get_public_url(file_path)
        return public_url

    except Exception as e:
        raise Exception(f"Gagal upload file: {str(e)}")



def delete_file_storage_supabase(bucket: str, url):
    try:
        public_prefix = f"/storage/v1/object/public/{bucket}/"

        if public_prefix not in url:
            raise Exception("URL tidak valid untuk Supabase Storage")

        file_path = url.split(public_prefix)[1].split("?")[0]

        supabase_client.storage.from_(bucket).remove([file_path])

        return True

    except Exception as e:
        raise Exception(f"Gagal hapus file: {str(e)}")
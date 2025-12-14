
import re
import uuid

def generate_unique_username(email):
    base = email.split("@")[0]
    base = re.sub(r"[^a-zA-Z0-9]", "", base).lower()
    base = base[:15]
    suffix = uuid.uuid4().hex[:3]

    return f"{base}_{suffix}"
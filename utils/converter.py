def konversi_nilai_ke_huruf(nilai, penilaian):
    if not penilaian:
        return "-"
    if nilai >= penilaian.nilai_a_min:
        return "A"
    elif nilai >= penilaian.nilai_b_min:
        return "B"
    elif nilai >= penilaian.nilai_c_min:
        return "C"
    elif nilai >= penilaian.nilai_d_min:
        return "D"
    else:
        return "E"


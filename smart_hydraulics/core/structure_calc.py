import math

def hitung_lebar_efektif(B_total, n_pilar, H1, kp=0.01, ka=0.1):
    """
    Menghitung Lebar Efektif Bendung (Be) sesuai KP-02
    B_total: Lebar bendung total (jarak antar tembok pangkal)
    n_pilar: Jumlah pilar
    H1: Tinggi energi di hulu (m)
    kp: Koefisien kontraksi pilar (bulat=0.01, persegi=0.02)
    ka: Koefisien kontraksi pangkal (bulat=0.1, persegi=0.2)
    """
    Be = B_total - 2 * (n_pilar * kp + ka) * H1
    return Be

def hitung_h1_bendung(Q_desain, B_total, n_pilar, Cd=1.3, max_iter=50):
    """
    Mencari H1 (Tinggi Energi) jika Q diketahui.
    Rumus: Q = Cd * 2/3 * sqrt(2g) * Be * H1^1.5
    Karena Be bergantung pada H1, ini harus iteratif.
    """
    g = 9.81
    H1 = 1.0 # Tebakan awal
    
    for _ in range(max_iter):
        # 1. Hitung lebar efektif dengan H1 saat ini
        Be = hitung_lebar_efektif(B_total, n_pilar, H1)
        
        # 2. Hitung Q berdasarkan H1 dan Be saat ini
        Q_calc = Cd * (2/3) * math.sqrt(2*g) * Be * (H1**1.5)
        
        # 3. Cek error
        if abs(Q_calc - Q_desain) < 0.001:
            return H1, Be
            
        # 4. Koreksi H1 (Simple adjustment)
        H1 = H1 * (Q_desain / Q_calc)**(1/1.5)
        
    return H1, Be # Return hasil terakhir estimasi
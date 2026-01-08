import numpy as np

def solve_manning_h(Q, b, m, S, n, max_iter=100, tol=1e-6):
    """
    Mencari kedalaman normal (h) untuk saluran trapesium
    menggunakan metode Newton-Raphson.
    Input:
    Q = Debit (m3/s)
    b = Lebar dasar (m)
    m = Kemiringan talud (1:m)
    S = Kemiringan memanjang saluran
    n = Koefisien kekasaran Manning
    Output:
    h = Kedalaman air normal (m)
    v = Kecepatan aliran (m/s)
    """
    h = 1.0 # Tebakan awal tinggi air (1 meter)
    
    for i in range(max_iter):
        A = (b + m * h) * h
        P = b + 2 * h * np.sqrt(1 + m**2)
        R = A / P
        T = b + 2 * m * h # Lebar atas (Top width) untuk turunan
        
        # Manning Equation: Q = (1/n) * A * R^(2/3) * S^0.5
        # Kita buat fungsi f(h) = (1/n) * A * R^(2/3) * S^0.5 - Q = 0
        Q_calc = (1/n) * A * (R**(2/3)) * (S**0.5)
        f = Q_calc - Q
        
        if abs(f) < tol:
            v = Q / A
            return h, v, "Konvergen"
        
        # Turunan f(h) terhadap h (df/dh) untuk Newton Raphson
        # dQ/dh = Q * ( (5T - 2R(dP/dh)) / (3A) ) -> Pendekatan hidrolis
        dP_dh = 2 * np.sqrt(1 + m**2)
        dA_dh = T
        dR_dh = (P*dA_dh - A*dP_dh) / (P**2)
        
        # Turunan Q terhadap h secara numerik sederhana
        df = (S**0.5 / n) * ( (5/3)*A**(2/3)*P**(-2/3)*T - (2/3)*A**(5/3)*P**(-5/3)*dP_dh )
        
        # Update h
        h_new = h - (f / df)
        
        if h_new <= 0: h_new = 0.01 # Cegah nilai negatif
        h = h_new
        
    return h, Q/((b + m * h) * h), "Tidak Konvergen"
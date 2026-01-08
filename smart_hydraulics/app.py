import streamlit as st
from hydraulic_calc import solve_manning_h
from structure_calc import hitung_h1_bendung

st.set_page_config(page_title="Modul Desain Hidrolis", layout="wide")

st.title("🚧 Modul Desain Saluran & Bendung (Fase 3)")

# --- BAGIAN 1: INPUT VARIABEL (NANTINYA OTOMATIS DARI FASE 2) ---
with st.sidebar:
    st.header("🔗 Konektor Data (Simulasi)")
    st.info("Variabel ini nanti otomatis terisi dari Modul Hidrologi")
    
    # Inilah 'Variabel Q' yang Anda tanyakan
    # Nanti diganti: Q_desain = st.session_state['q_desain_hidrologi']
    Q_desain = st.number_input("Debit Desain (Q) m³/dt", value=5.5, step=0.1)

# --- BAGIAN 2: MODUL DESAIN SALURAN ---
st.subheader("1. Desain Saluran Trapesium")
col1, col2, col3 = st.columns(3)
with col1:
    b_sal = st.number_input("Lebar Dasar (b)", value=2.0)
with col2:
    m_sal = st.number_input("Kemiringan Talud (m)", value=1.0)
with col3:
    S_sal = st.number_input("Kemiringan Saluran (S)", value=0.0005, format="%.5f")

if st.button("Hitung Dimensi Saluran"):
    h_normal, v_aliran, status = solve_manning_h(Q_desain, b_sal, m_sal, S_sal, n=0.025)
    
    st.success(f"Kedalaman Air Normal (h): **{h_normal:.3f} m**")
    st.info(f"Kecepatan Aliran (v): {v_aliran:.3f} m/s")
    
    # Validasi KP-03 Sederhana
    if v_aliran > 0.7:
        st.warning("⚠️ Kecepatan > 0.7 m/s (Potensi erosi jika saluran tanah)")
    elif v_aliran < 0.25:
        st.warning("⚠️ Kecepatan < 0.25 m/s (Potensi endapan lumpur)")

st.markdown("---")

# --- BAGIAN 3: MODUL DESAIN BENDUNG ---
st.subheader("2. Desain Mercu Bendung (KP-02)")
col_b1, col_b2 = st.columns(2)
with col_b1:
    B_bendung = st.number_input("Lebar Sungai Rata-rata (m)", value=15.0)
with col_b2:
    elev_dasar = st.number_input("Elevasi Dasar Sungai (+m)", value=100.0)

if st.button("Hitung Tinggi Muka Air Bendung"):
    H1, Be = hitung_h1_bendung(Q_desain, B_bendung, n_pilar=0)
    
    elev_muka_air = elev_dasar + 1.5 # Misal tinggi mercu 1.5m
    elev_banjir = elev_muka_air + H1
    
    st.metric("Tinggi Energi (H1)", f"{H1:.3f} m")
    st.metric("Lebar Efektif (Be)", f"{Be:.3f} m")
    st.metric("Elevasi Muka Air Banjir", f"+{elev_banjir:.3f} m")
"""
🎯 CAPSTONE PROJECT - DASHBOARD ANALISIS PENDIDIKAN INDONESIA

Dashboard gabungan untuk 2 pertanyaan bisnis:
1. Estimasi Pelajar yang Dapat Dijangkau (3-6 Bulan)
2. Korelasi IPTI dengan Angka Partisipasi Sekolah (2020-2025)

Author: Capstone Project
"""

import streamlit as st
import pandas as pd
import os
from pathlib import Path

# Import custom modules
from utils.notebook_executor import load_pertanyaan_satu_from_notebook, load_pertanyaan_dua_from_notebook


# ============================================================================
# CONFIG STREAMLIT
# ============================================================================

st.set_page_config(
    page_title="Dashboard Analisis Pendidikan",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS untuk tampilan yang lebih baik
st.markdown("""
    <style>
    .main-header {
        text-align: center;
        padding: 20px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
        color: blue;
        margin-bottom: 20px;
    }
    .sub-header {
        color: #667eea;
        border-bottom: 3px solid #667eea;
        padding-bottom: 10px;
        margin-top: 20px;
        margin-bottom: 15px;
    }
    .metric-box {
        background-color: #e8edff;
        padding: 15px;
        border-radius: 8px;
        border-left: 4px solid #667eea;
        box-shadow: 0 2px 12px rgba(102, 126, 234, 0.25);
    }
    </style>
""", unsafe_allow_html=True)


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

@st.cache_resource
def load_pertanyaan_satu():
    """Load dan cache hasil analisis pertanyaan 1 dari main.ipynb."""
    # Tentukan path ke notebook dari lokasi script ini
    # Path(__file__).parent = capstone-streamlit/
    # Path(__file__).parent.parent = Capstone Project Dicoding/
    # Path(__file__).parent.parent / "pertanyaan_satu" = Capstone Project Dicoding/pertanyaan_satu/
    app_dir = Path(__file__).parent
    root_dir = app_dir.parent
    notebook_path = root_dir / "pertanyaan_satu" / "main.ipynb"
    
    st.write(f"DEBUG: Resolved notebook path: {notebook_path}")
    st.write(f"DEBUG: Path exists: {notebook_path.exists()}")
    
    return load_pertanyaan_satu_from_notebook(str(notebook_path.resolve()))


@st.cache_resource
def load_pertanyaan_dua():
    """Load dan cache hasil analisis pertanyaan 2 dari Untitled3.ipynb."""
    # Tentukan path ke notebook dari lokasi script ini
    app_dir = Path(__file__).parent
    root_dir = app_dir.parent
    notebook_path = root_dir / "pertanyaan_dua" / "Untitled3.ipynb"
    
    st.write(f"DEBUG: Resolved notebook path: {notebook_path}")
    st.write(f"DEBUG: Path exists: {notebook_path.exists()}")
    
    return load_pertanyaan_dua_from_notebook(str(notebook_path.resolve()))


# ============================================================================
# MAIN APP LOGIC
# ============================================================================

def main():
    """Main app logic."""
    
    # Header
    st.markdown("""
        <div class="main-header">
            <h1>📊 Dashboard Analisis Jangkauan Kebutuhan Beasiswa </h1>
            <p>Capstone Project - DICODING</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Sidebar untuk navigasi
    st.sidebar.title("Navigasi Dashboard")
    
    # Dropdown untuk pilih pertanyaan
    pertanyaan = st.sidebar.radio(
        "Pilih Pertanyaan Bisnis:",
        options=[
            "Estimasi Pelajar Terjangkau",
            "Korelasi IPTI vs APS"
        ],
        help="Pilih salah satu untuk melihat analisisnya"
    )
    
    # ========================================================================
    # PERTANYAAN SATU
    # ========================================================================
    
    if pertanyaan == "Estimasi Pelajar Terjangkau":
        st.markdown('<h2 class="sub-header">📍 Estimasi Pelajar yang Dapat Dijangkau (3-6 Bulan)</h2>', unsafe_allow_html=True)
        
        # Deskripsi
        st.write("""
        **Tujuan Analisis:**
        > Menjawab pertanyaan: *"Seberapa banyak pelajar yang dapat dijangkau untuk menjadi pengguna 
        platform organisasi dalam 3-6 bulan ke depan?"*
        
        **Metodologi:**
        1. Menghitung jumlah pelajar aktif (total siswa - putus sekolah)
        2. Normalisasi metrik akses: telepon seluler, internet, sinyal
        3. Menghitung skor jangkauan gabungan (40% telepon + 40% internet + 20% sinyal)
        4. Estimasi pelajar terjangkau = pelajar aktif × skor jangkauan
        5. Feature engineering untuk memprioritaskan berdasarkan kondisi dropout
        """)
        
        try:
            # Load data
            result_q1 = load_pertanyaan_satu()
            data_after_fe = result_q1['after_fe']
            visualisasi = result_q1['visualisasi']
            
            # Tabs untuk pilih tampilan
            tab1, tab2, tab3, tab4 = st.tabs([
                "📊 Data Summary",
                "📈 Top 10 Rankings",
                "📊 Heatmap",
                "📉 Scatter Analysis"
            ])
            
            # TAB 1: Data Summary
            with tab1:
                st.markdown("#### Data Summary Pertanyaan Satu")
                
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("""
                    <div class="metric-box">
                    <b>Jumlah Provinsi</b><br>
                    {0}
                    </div>
                    """.format(len(data_after_fe)), unsafe_allow_html=True)
                
                with col2:
                    st.markdown("""
                    <div class="metric-box">
                    <b>Total Estimasi Terjangkau</b><br>
                    {0:,.0f}
                    </div>
                    """.format(data_after_fe['estimasi_pelajar_terjangkau'].sum()), unsafe_allow_html=True)
                
                st.markdown("#### Ranking Hasil After Feature Engineering")
                top10_after = data_after_fe.nlargest(10, 'skor_prioritas_baru')[[
                    'Provinsi', 'pelajar_aktif', 'skor_jangkauan',
                    'skor_dropout_rendah', 'skor_prioritas_baru',
                    'estimasi_pelajar_terjangkau'
                ]].copy()
                top10_after = top10_after.reset_index(drop=True)
                top10_after.index = range(1, len(top10_after) + 1)
                top10_after.index.name = 'Ranking'
                st.dataframe(top10_after, use_container_width=True)
            
            # TAB 2: Top 10 Rankings
            with tab2:
                st.markdown("#### Top 10 Ranking After Feature Engineering")
                plt_obj = visualisasi['2_Estimasi_After_FE']()
                st.pyplot(plt_obj)

            # TAB 3: Heatmap
            with tab3:
                st.markdown("#### Heatmap Indikator After Feature Engineering")
                plt_obj = visualisasi['7_Heatmap_After_FE']()
                st.pyplot(plt_obj)

            # TAB 4: Scatter
            with tab4:
                st.markdown("#### Scatter Analysis After Feature Engineering")
                plt_obj = visualisasi['9_Scatter_After_FE']()
                st.pyplot(plt_obj)
        
        except Exception as e:
            st.error(f"❌ Terjadi error saat memuat data: {str(e)}")
            st.info("Pastikan `pertanyaan_satu/main.ipynb` sudah ada dan sudah dijalankan sepenuhnya.")
    
    # ========================================================================
    # PERTANYAAN DUA
    # ========================================================================
    
    elif pertanyaan == "Korelasi IPTI vs APS":
        st.markdown('<h2 class="sub-header">Korelasi IPTIK dengan Peserta dan Lulusan SMA (2020-2025)</h2>', unsafe_allow_html=True)
        
        # Deskripsi
        st.write("""
        **Tujuan Analisis:**
        > Menjawab pertanyaan: *"Bagaimana korelasi antara Indeks Pembangunan Teknologi Informasi (IPTIK) 
        suatu provinsi dengan data peserta dan lulusan SMA dari tahun 2020 - 2025?"*
        
        **Metodologi:**
        1. Merge 3 dataset IPTIK (2019-2024) menjadi 6 tahun continuous
        2. Merge 6 dataset peserta/lulusan per tahun (2020-2025)
        3. Hitung rata-rata IPTIK, peserta, lulusan, dan gap peserta-lulusan
        4. Analisis korelasi menggunakan Pearson correlation
        5. Visualisasi: bar charts, line plots, heatmap, scatter plots
        """)
        
        try:
            # Load data
            result_q2 = load_pertanyaan_dua()
            df_iptik = result_q2['df_iptik']
            df_aps = result_q2['df_aps']
            corr_matrix = result_q2['corr_matrix']
            visualisasi = result_q2['visualisasi']
            
            # Tabs untuk pilih tampilan
            tab1, tab2, tab3, tab4, tab5 = st.tabs([
                "📊 Data Summary",
                "📈 Top 10 Rankings",
                "📊 Tren Waktu",
                "🔗 Korelasi",
                "📉 Scatter Analysis"
            ])
            
            # TAB 1: Data Summary
            with tab1:
                st.markdown("#### Data Summary Pertanyaan Dua")
                
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("""
                    <div class="metric-box">
                    <b>Jumlah Provinsi (IPTIK)</b><br>
                    {0}
                    </div>
                    """.format(len(df_iptik)), unsafe_allow_html=True)
                
                with col2:
                    st.markdown("""
                    <div class="metric-box">
                    <b>Jumlah Provinsi (Peserta/Lulusan)</b><br>
                    {0}
                    </div>
                    """.format(len(df_aps)), unsafe_allow_html=True)
                
                # Top 10 IPTIK
                st.markdown("#### Ranking Provinsi IPTIK (2024)")
                df_iptik_display = df_iptik.copy().reset_index()
                # Filter Indonesia/agregasi yang mungkin masih ada
                provinsi_filter = ['INDONESIA', '38 PROVINSI', 'TOTAL', 'JUMLAH', 'LUAR NEGERI']
                # Normalize untuk case-insensitive filter
                df_iptik_display['Provinsi'] = df_iptik_display['Provinsi'].astype(str).str.strip().str.upper()
                df_iptik_display = df_iptik_display[~df_iptik_display['Provinsi'].isin(provinsi_filter)]
                df_iptik_display = df_iptik_display.drop('Rank', axis=1, errors='ignore')
                df_iptik_display.index = range(1, len(df_iptik_display) + 1)
                df_iptik_display.index.name = 'Ranking'
                st.dataframe(df_iptik_display.head(10), use_container_width=True)
                
                # Top 10 Peserta/Lulusan
                st.markdown("#### Ranking Provinsi Peserta/Lulusan (2025)")
                df_aps_display = df_aps.copy().reset_index()
                # Filter Indonesia/agregasi yang mungkin masih ada
                provinsi_filter = ['INDONESIA', '38 PROVINSI', 'TOTAL', 'JUMLAH', 'LUAR NEGERI']
                # Normalize untuk case-insensitive filter
                df_aps_display['Provinsi'] = df_aps_display['Provinsi'].astype(str).str.strip().str.upper()
                df_aps_display = df_aps_display[~df_aps_display['Provinsi'].isin(provinsi_filter)]
                df_aps_display = df_aps_display.drop('Rank', axis=1, errors='ignore')
                df_aps_display.index = range(1, len(df_aps_display) + 1)
                df_aps_display.index.name = 'Ranking'
                st.dataframe(df_aps_display.head(10), use_container_width=True)
                
                # Correlation summary
                st.markdown("#### Summary Korelasi")
                corr_iptik_avg = corr_matrix.loc['IPTIK_avg', ['Peserta_avg', 'Lulusan_avg', 'Gap_avg']]
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Korelasi IPTIK vs Peserta", f"{corr_iptik_avg['Peserta_avg']:.3f}")
                with col2:
                    st.metric("Korelasi IPTIK vs Lulusan", f"{corr_iptik_avg['Lulusan_avg']:.3f}")
                with col3:
                    st.metric("Korelasi IPTIK vs Gap", f"{corr_iptik_avg['Gap_avg']:.3f}")
            
            # TAB 2: Top 10 Rankings
            with tab2:
                st.markdown("#### Top 10 Rankings Berbagai Metrik")
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.markdown("**Top 10 IPTIK Average**")
                    plt_obj = visualisasi['1_Top10_IPTIK']()
                    st.pyplot(plt_obj)
                
                with col2:
                    st.markdown("**Top 10 Peserta Rata-rata**")
                    plt_obj = visualisasi['2_Top10_APS_13-15']()
                    st.pyplot(plt_obj)
                
                with col3:
                    st.markdown("**Top 10 Lulusan Rata-rata**")
                    plt_obj = visualisasi['3_Top10_APS_16-18']()
                    st.pyplot(plt_obj)
                
                # Baris kedua
                col4, col5 = st.columns(2)
                with col4:
                    st.markdown("**Top 10 Gap Peserta-Lulusan**")
                    plt_obj = visualisasi['4_Top10_APS_19-23']()
                    st.pyplot(plt_obj)
            
            # TAB 3: Tren Waktu
            with tab3:
                st.markdown("#### Tren Waktu Peserta/Lulusan per Provinsi (Top 10)")
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.markdown("**Tren Peserta (2020-2025)**")
                    plt_obj = visualisasi['5_Tren_APS_13-15']()
                    st.pyplot(plt_obj)
                
                with col2:
                    st.markdown("**Tren Lulusan (2020-2025)**")
                    plt_obj = visualisasi['6_Tren_APS_16-18']()
                    st.pyplot(plt_obj)
                
                with col3:
                    st.markdown("**Tren Gap Peserta-Lulusan (2020-2025)**")
                    plt_obj = visualisasi['7_Tren_APS_19-23']()
                    st.pyplot(plt_obj)
                
                st.info("""
                **Insight dari tren:**
                - Garis menunjukkan pergerakan peserta/lulusan per provinsi
                - Slope positif = peningkatan jumlah
                - Slope negatif = penurunan jumlah
                """)
            
            # TAB 4: Korelasi
            with tab4:
                st.markdown("#### Heatmap Korelasi IPTIK vs Peserta/Lulusan")
                
                plt_obj = visualisasi['8_Correlation_Heatmap']()
                st.pyplot(plt_obj)
                
                st.info("""
                **Interpretasi Heatmap:**
                - **Korelasi Positif** (warna merah): Peningkatan satu metrik → peningkatan metrik lain
                - **Korelasi Negatif** (warna biru): Peningkatan satu metrik → penurunan metrik lain
                - **Nilai 0** (warna putih): Tidak ada korelasi linear
                """)
                
                # Detail korelasi
                st.markdown("#### Nilai Korelasi Detail")
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("**IPTIK Average vs Peserta/Lulusan Metrics:**")
                    corr_detail = corr_matrix.loc['IPTIK_avg', ['Peserta_avg', 'Lulusan_avg', 'Gap_avg']]
                    st.dataframe(corr_detail.to_frame(name='Correlation'))
                
                with col2:
                    st.markdown("**IPTIK Year-by-Year vs Gap:**")
                    corr_yearly = corr_matrix.loc[['IPTIK_2019', 'IPTIK_2020', 'IPTIK_2021', 'IPTIK_2022', 'IPTIK_2023', 'IPTIK_2024'], 'Gap_avg']
                    st.dataframe(corr_yearly.to_frame(name='Correlation with Gap'))
            
            # TAB 5: Scatter Analysis
            with tab5:
                st.markdown("#### Scatter Plot: IPTIK Average vs Peserta/Lulusan")
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.markdown("**IPTIK vs Peserta**")
                    plt_obj = visualisasi['9_Scatter_IPTIK_vs_APS_13-15']()
                    st.pyplot(plt_obj)
                
                with col2:
                    st.markdown("**IPTIK vs Lulusan**")
                    plt_obj = visualisasi['10_Scatter_IPTIK_vs_APS_16-18']()
                    st.pyplot(plt_obj)
                
                with col3:
                    st.markdown("**IPTIK vs Gap**")
                    plt_obj = visualisasi['11_Scatter_IPTIK_vs_APS_19-23']()
                    st.pyplot(plt_obj)
                
                st.info("""
                **Interpretasi Scatter Plot:**
                - Setiap titik mewakili 1 provinsi
                - Garis merah = tren linear (best fit)
                - Slope positif = korelasi positif
                - Kumpul di sekitar garis = korelasi kuat
                """)
        
        except Exception as e:
            st.error(f"❌ Terjadi error saat memuat data: {str(e)}")
            st.info("Pastikan `pertanyaan_dua/Untitled3.ipynb` sudah ada dan sudah dijalankan sepenuhnya.")
    
    # Footer
    st.markdown("""
    ---
    <div style="text-align: center; margin-top: 30px; padding: 20px; color: #666;">
    <p>Dashboard Capstone Project | Estimasi Pelajar & Korelasi IPTI</p>
    <p style="font-size: 12px;">Data Source: Pemerintah Indonesia | Last Updated: 2025</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()

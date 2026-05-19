"""
🎯 CAPSTONE PROJECT - DASHBOARD ANALISIS PENDIDIKAN INDONESIA

Dashboard gabungan untuk 2 pertanyaan bisnis:
1. Estimasi Pelajar yang Dapat Dijangkau (3-6 Bulan)
2. Korelasi IPTI dengan Angka Partisipasi Sekolah (2020-2025)

Author: Capstone Project
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
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
    """Load dan cache hasil analisis pertanyaan 2 dari Hasil_Analisis_Pertanyaan_Bisnis_Kedua.ipynb."""
    # Tentukan path ke notebook dari lokasi script ini
    app_dir = Path(__file__).parent
    root_dir = app_dir.parent
    notebook_path = root_dir / "pertanyaan_dua" / "Hasil_Analisis_Pertanyaan_Bisnis_Kedua.ipynb"
    
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
        st.markdown('<h2 class="sub-header">Korelasi IPTIK dengan APS - Angka Partisipasi Sekolah (2020-2025)</h2>', unsafe_allow_html=True)
        
        # Deskripsi
        st.write("""
        **Tujuan Analisis:**
        > Menjawab pertanyaan: *"Bagaimana korelasi antara Indeks Pembangunan Teknologi Informasi (IPTIK) 
        suatu provinsi dengan Angka Partisipasi Sekolah (APS) berdasarkan kelompok umur dari tahun 2020 - 2025?"*
        
        **Metodologi:**
        1. Merge 3 dataset IPTIK (2019-2024) menjadi data kontinyu
        2. Merge 6 dataset APS per tahun (2020-2025) berdasarkan kelompok umur: 13-15 (SMP), 16-18 (SMA), 19-23 (Pasca SMA)
        3. Hitung rata-rata IPTIK dan APS untuk setiap kelompok umur
        4. Analisis korelasi menggunakan Pearson correlation antara IPTIK dan APS
        5. Visualisasi: bar charts, line plots, heatmap, scatter plots
        """)
        
        try:
            # Load data
            result_q2 = load_pertanyaan_dua()
            df_iptik = result_q2['df_iptik']
            df_aps = result_q2['df_aps']
            corr_matrix = result_q2['corr_matrix']
            df_corr = result_q2.get('df_corr')  # Merged data with both IPTIK and APS
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
                    <b>Jumlah Provinsi (APS - Kelompok Umur)</b><br>
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
                
                # Top 10 APS Tertinggi
                st.markdown("#### Ranking Provinsi berdasarkan APS Rata-Rata (2025)")
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
                st.markdown("#### Summary Korelasi IPTIK dengan APS")
                try:
                    # Gunakan nama kolom yang sebenarnya ada di correlation matrix
                    if corr_matrix is not None and 'IPTIK_avg' in corr_matrix.index:
                        corr_iptik_avg_row = corr_matrix.loc['IPTIK_avg']
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Korelasi IPTIK vs APS (13-15)", f"{corr_iptik_avg_row['APS_avg_age_13-15']:.3f}")
                        with col2:
                            st.metric("Korelasi IPTIK vs APS (16-18)", f"{corr_iptik_avg_row['APS_avg_age_16-18']:.3f}")
                        with col3:
                            st.metric("Korelasi IPTIK vs APS (19-23)", f"{corr_iptik_avg_row['APS_avg_age_19-23']:.3f}")
                    else:
                        st.warning("Correlation matrix tidak memiliki IPTIK_avg index")
                        if corr_matrix is not None:
                            st.write(f"Index: {corr_matrix.index.tolist()}")
                except KeyError as e:
                    st.error(f"KeyError: {e}")
                    st.write(f"Correlation matrix index: {corr_matrix.index.tolist() if corr_matrix is not None else 'None'}")
                except Exception as e:
                    st.error(f"Error accessing correlation data: {e}")
                    st.write(f"Correlation matrix type: {type(corr_matrix)}")
            
            # TAB 2: Top 10 Rankings
            with tab2:
                st.markdown("#### Top 10 Rankings Berbagai Metrik")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("**Top 10 IPTIK Average (2024)**")
                    # Calculate IPTIK average from year columns
                    df_iptik_calc = df_iptik.copy()
                    year_cols = [c for c in df_iptik_calc.columns if c not in ['Provinsi', 'Rank']]
                    if year_cols:
                        df_iptik_calc['IPTIK_avg'] = df_iptik_calc[year_cols].mean(axis=1)
                        df_top10_iptik = df_iptik_calc.nlargest(10, 'IPTIK_avg')[['Provinsi', 'IPTIK_avg']].copy()
                    else:
                        # If no year columns, use all columns except Provinsi
                        df_iptik_calc['IPTIK_avg'] = df_iptik_calc[[c for c in df_iptik_calc.columns if c != 'Provinsi']].mean(axis=1)
                        df_top10_iptik = df_iptik_calc.nlargest(10, 'IPTIK_avg')[['Provinsi', 'IPTIK_avg']].copy()
                    
                    fig, ax = plt.subplots(figsize=(8, 5))
                    ax.barh(df_top10_iptik['Provinsi'], df_top10_iptik['IPTIK_avg'], color='steelblue')
                    ax.set_xlabel('IPTIK Average')
                    ax.invert_yaxis()
                    plt.tight_layout()
                    st.pyplot(fig)
                
                with col2:
                    st.markdown("**Top 10 APS (Age 16-18)**")
                    # Plot top 10 APS 16-18 (secondary education)
                    # Calculate average across years for age 16-18
                    if 'APS_avg_1618' in df_aps.columns:
                        df_top10_aps = df_aps.nlargest(10, 'APS_avg_1618')[['Provinsi', 'APS_avg_1618']].copy()
                        df_top10_aps = df_top10_aps.rename(columns={'APS_avg_1618': 'APS_Rata2'})
                    else:
                        # Kalkulasi dari kolom tahun jika ada
                        aps_cols = [c for c in df_aps.columns if '16-18' in c or '16_18' in c]
                        if aps_cols:
                            df_top10_aps = df_aps.copy()
                            df_top10_aps['APS_Rata2'] = df_top10_aps[[c for c in df_aps.columns if '16-18' in c or '16_18' in c]].mean(axis=1)
                            df_top10_aps = df_top10_aps.nlargest(10, 'APS_Rata2')[['Provinsi', 'APS_Rata2']]
                        else:
                            st.warning("Kolom APS tidak ditemukan untuk visualisasi")
                            df_top10_aps = None
                    
                    if df_top10_aps is not None:
                        fig, ax = plt.subplots(figsize=(8, 5))
                        ax.barh(df_top10_aps['Provinsi'], df_top10_aps['APS_Rata2'], color='coral')
                        ax.set_xlabel('APS Average (16-18)')
                        ax.invert_yaxis()
                        plt.tight_layout()
                        st.pyplot(fig)
            
            # TAB 3: Tren Waktu
            with tab3:
                st.markdown("#### Tren Waktu IPTIK per Provinsi (Top 10 by 2024)")
                
                # Calculate IPTIK average and get top 10
                df_iptik_calc = df_iptik.copy()
                year_cols = [c for c in df_iptik_calc.columns if c not in ['Provinsi', 'Rank']]
                if year_cols:
                    df_iptik_calc['IPTIK_avg'] = df_iptik_calc[year_cols].mean(axis=1)
                    top10_provinsi = df_iptik_calc.nlargest(10, 'IPTIK_avg')['Provinsi'].tolist()
                else:
                    st.warning("Tidak ada kolom tahun ditemukan")
                    top10_provinsi = df_iptik['Provinsi'].head(10).tolist()
                
                df_tren = df_iptik[df_iptik['Provinsi'].isin(top10_provinsi)][['Provinsi'] + year_cols].copy()
                
                fig, ax = plt.subplots(figsize=(12, 6))
                for provinsi in top10_provinsi:
                    row = df_tren[df_tren['Provinsi'] == provinsi].iloc[0]
                    ax.plot(year_cols, [row[col] for col in year_cols], marker='o', label=provinsi)
                
                ax.set_xlabel('Tahun')
                ax.set_ylabel('IPTIK Index')
                ax.set_title(f'Tren IPTIK per Provinsi (Top 10, {min(year_cols)}-{max(year_cols)})')
                ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=8)
                ax.grid(True, alpha=0.3)
                plt.tight_layout()
                st.pyplot(fig)
                
                st.info("""
                **Insight dari tren:**
                - Garis menunjukkan pergerakan IPTIK per provinsi tahun 2019-2024
                - Slope positif = peningkatan IPTIK
                - Slope negatif = penurunan IPTIK
                """)
            
            # TAB 4: Korelasi
            with tab4:
                st.markdown("#### Heatmap Korelasi IPTIK vs APS")
                
                fig, ax = plt.subplots(figsize=(10, 6))
                sns.heatmap(corr_matrix, annot=True, fmt='.3f', cmap='coolwarm', center=0, 
                           ax=ax, cbar_kws={'label': 'Correlation'})
                ax.set_title('Correlation Matrix: IPTIK vs APS Metrics')
                plt.tight_layout()
                st.pyplot(fig)
                
                st.info("""
                **Interpretasi Heatmap:**
                - **Nilai Positif** (warna merah): Korelasi positif - saat satu naik, yang lain cenderung naik
                - **Nilai Negatif** (warna biru): Korelasi negatif - saat satu naik, yang lain cenderung turun
                - **Nilai 0** (warna putih): Tidak ada korelasi linear
                
                **Kolom APS:**
                - **APS_avg_age_13-15**: Peserta pada usia 13-15 tahun (SMP)
                - **APS_avg_age_16-18**: Peserta pada usia 16-18 tahun (SMA)
                - **APS_avg_age_19-23**: Peserta pada usia 19-23 tahun (Pasca SMA)
                """)
                
                # Detail korelasi
                st.markdown("#### Nilai Korelasi Detail")
                try:
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown("**IPTIK Average vs APS Metrics:**")
                        if 'IPTIK_avg' in corr_matrix.index:
                            corr_detail = corr_matrix.loc['IPTIK_avg', ['APS_avg_age_13-15', 'APS_avg_age_16-18', 'APS_avg_age_19-23']]
                            st.dataframe(corr_detail.to_frame(name='Correlation'))
                        else:
                            st.warning("IPTIK_avg tidak ditemukan di correlation matrix index")
                    
                    with col2:
                        st.markdown("**IPTIK Year-by-Year vs APS (16-18):**")
                        if 'IPTIK_avg' in corr_matrix.index:
                            year_indices = [idx for idx in corr_matrix.index if idx.startswith('IPTIK_')]
                            if year_indices:
                                corr_yearly = corr_matrix.loc[year_indices, 'APS_avg_age_16-18']
                                st.dataframe(corr_yearly.to_frame(name='Correlation with APS (16-18)'))
                except Exception as e:
                    st.error(f"Error displaying correlation details: {e}")
            
            # TAB 5: Scatter Analysis
            with tab5:
                st.markdown("#### Scatter Plot: IPTIK Average vs APS Metrics")
                
                if df_corr is not None:
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.markdown("**IPTIK vs APS (Age 13-15)**")
                        if 'IPTIK_avg' in df_corr.columns and 'APS_avg_age_13-15' in df_corr.columns:
                            fig, ax = plt.subplots(figsize=(6, 5))
                            x_data = df_corr['IPTIK_avg'].dropna()
                            y_data = df_corr['APS_avg_age_13-15'].dropna()
                            ax.scatter(x_data, y_data, alpha=0.6, s=100)
                            if len(x_data) > 1 and len(y_data) > 1:
                                z = np.polyfit(x_data, y_data, 1)
                                p = np.poly1d(z)
                                x_line = np.linspace(x_data.min(), x_data.max(), 100)
                                ax.plot(x_line, p(x_line), "r--", alpha=0.8, label='Trend')
                            ax.set_xlabel('IPTIK Average')
                            ax.set_ylabel('APS Average (13-15)')
                            try:
                                if 'IPTIK_avg' in corr_matrix.index and 'APS_avg_age_13-15' in corr_matrix.columns:
                                    corr_val = corr_matrix.loc['IPTIK_avg', 'APS_avg_age_13-15']
                                    ax.set_title(f"Correlation: {corr_val:.3f}")
                            except Exception:
                                pass
                            ax.legend()
                            ax.grid(True, alpha=0.3)
                            plt.tight_layout()
                            st.pyplot(fig)
                    
                    with col2:
                        st.markdown("**IPTIK vs APS (Age 16-18)**")
                        if 'IPTIK_avg' in df_corr.columns and 'APS_avg_age_16-18' in df_corr.columns:
                            fig, ax = plt.subplots(figsize=(6, 5))
                            x_data = df_corr['IPTIK_avg'].dropna()
                            y_data = df_corr['APS_avg_age_16-18'].dropna()
                            ax.scatter(x_data, y_data, alpha=0.6, s=100, color='coral')
                            if len(x_data) > 1 and len(y_data) > 1:
                                z = np.polyfit(x_data, y_data, 1)
                                p = np.poly1d(z)
                                x_line = np.linspace(x_data.min(), x_data.max(), 100)
                                ax.plot(x_line, p(x_line), "r--", alpha=0.8, label='Trend')
                            ax.set_xlabel('IPTIK Average')
                            ax.set_ylabel('APS Average (16-18)')
                            try:
                                if 'IPTIK_avg' in corr_matrix.index and 'APS_avg_age_16-18' in corr_matrix.columns:
                                    corr_val = corr_matrix.loc['IPTIK_avg', 'APS_avg_age_16-18']
                                    ax.set_title(f"Correlation: {corr_val:.3f}")
                            except Exception:
                                pass
                            ax.legend()
                            ax.grid(True, alpha=0.3)
                            plt.tight_layout()
                            st.pyplot(fig)
                    
                    with col3:
                        st.markdown("**IPTIK vs APS (Age 19-23)**")
                        if 'IPTIK_avg' in df_corr.columns and 'APS_avg_age_19-23' in df_corr.columns:
                            fig, ax = plt.subplots(figsize=(6, 5))
                            x_data = df_corr['IPTIK_avg'].dropna()
                            y_data = df_corr['APS_avg_age_19-23'].dropna()
                            ax.scatter(x_data, y_data, alpha=0.6, s=100, color='green')
                            if len(x_data) > 1 and len(y_data) > 1:
                                z = np.polyfit(x_data, y_data, 1)
                                p = np.poly1d(z)
                                x_line = np.linspace(x_data.min(), x_data.max(), 100)
                                ax.plot(x_line, p(x_line), "r--", alpha=0.8, label='Trend')
                            ax.set_xlabel('IPTIK Average')
                            ax.set_ylabel('APS Average (19-23)')
                            try:
                                if 'IPTIK_avg' in corr_matrix.index and 'APS_avg_age_19-23' in corr_matrix.columns:
                                    corr_val = corr_matrix.loc['IPTIK_avg', 'APS_avg_age_19-23']
                                    ax.set_title(f"Correlation: {corr_val:.3f}")
                            except Exception:
                                pass
                            ax.legend()
                            ax.grid(True, alpha=0.3)
                            plt.tight_layout()
                            st.pyplot(fig)
                else:
                    st.warning("Data merged untuk scatter plot tidak tersedia")
                
                st.info("""
                **Interpretasi Scatter Plot:**
                - Setiap titik mewakili 1 provinsi
                - Garis merah = tren linear (best fit)
                - Slope positif = korelasi positif
                - Kumpul di sekitar garis = korelasi kuat
                """)
        
        except Exception as e:
            st.error(f"❌ Terjadi error saat memuat data: {str(e)}")
            st.info("Pastikan `pertanyaan_dua/Hasil_Analisis_Pertanyaan_Bisnis_Kedua.ipynb` sudah ada dan sudah dijalankan sepenuhnya.")
    
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

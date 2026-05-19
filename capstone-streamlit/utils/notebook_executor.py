"""
Execute Jupyter Notebooks dan extract hasil akhir untuk Streamlit.
Langsung ambil data dari main.ipynb dan Untitled3.ipynb.
"""

import nbformat
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path


def execute_notebook(notebook_path, data_dir):
    """
    Execute notebook dan return global variables yang dibuat.
    
    Args:
        notebook_path (str): Path ke notebook file
        data_dir (str): Path ke folder data (untuk context eksekusi)
        
    Returns:
        dict: Global variables dari notebook execution
    """
    # Validate notebook exists
    if not os.path.exists(notebook_path):
        raise FileNotFoundError(f"Notebook tidak ditemukan: {notebook_path}")
    
    with open(notebook_path) as f:
        nb = nbformat.read(f, as_version=4)
    
    # Setup execution environment dengan data_dir sebagai working directory
    exec_globals = {
        'pd': pd,
        'np': np,
        'plt': plt,
        'sns': sns,
        '__file__': notebook_path,
    }
    
    # Change working directory untuk notebook execution
    import sys
    original_cwd = os.getcwd()
    notebook_dir = os.path.dirname(os.path.abspath(notebook_path))
    os.chdir(notebook_dir)
    
    try:
        # Jalankan setiap cell
        for idx, cell in enumerate(nb.cells):
            if cell.cell_type == 'code':
                try:
                    exec(cell.source, exec_globals)
                except Exception as e:
                    # Print full error untuk debugging
                    print(f"⚠️ Cell {idx} error: {str(e)}")
                    import traceback
                    traceback.print_exc()
                    continue
    finally:
        os.chdir(original_cwd)
    
    return exec_globals


def load_pertanyaan_satu_from_notebook(notebook_path):
    """
    Load data dari main.ipynb untuk pertanyaan satu.
    
    Args:
        notebook_path (str): Path ke main.ipynb
        
    Returns:
        dict: Berisi 'after_fe' (dataframe) dan 'visualisasi' (dict of functions)
    """
    # Debug: print path yang diterima
    print(f"\n📝 load_pertanyaan_satu_from_notebook called with path: {notebook_path}")
    
    # Determine data directory (sibling folder dari notebook)
    notebook_dir = os.path.dirname(os.path.abspath(notebook_path))
    data_dir = os.path.dirname(notebook_dir)  # Go up one level from pertanyaan_satu/
    
    print(f"   Resolved notebook_dir: {notebook_dir}")
    print(f"   Resolved data_dir: {data_dir}")
    print(f"   Notebook exists: {os.path.exists(notebook_path)}")
    
    # Execute notebook
    exec_globals = execute_notebook(notebook_path, data_dir)
    
    # Extract data yang penting
    latihan_fe = exec_globals.get('latihan_fe')
    
    if latihan_fe is None:
        raise ValueError("❌ latihan_fe tidak ditemukan di notebook. Pastikan cell feature engineering sudah dijalankan.")
    
    # Debug info
    print(f"\n✅ latihan_fe extracted successfully!")
    print(f"   - Shape: {latihan_fe.shape}")
    print(f"   - Columns: {list(latihan_fe.columns)}")
    print(f"   - pelajar_aktif: min={latihan_fe['pelajar_aktif'].min()}, max={latihan_fe['pelajar_aktif'].max()}, mean={latihan_fe['pelajar_aktif'].mean():.0f}")
    print(f"   - Null values in pelajar_aktif: {latihan_fe['pelajar_aktif'].isna().sum()}")
    print(f"   - Sample data:\n{latihan_fe[['Provinsi', 'pelajar_aktif', 'skor_prioritas_baru']].head()}\n")
    
    # Buat visualisasi functions (copy dari main.ipynb logic)
    def normalisasi_0_1(seri):
        min_val = seri.min()
        max_val = seri.max()
        min_kosong = pd.isna(min_val)
        max_kosong = pd.isna(max_val)
        rentang_nol = max_val == min_val
        if min_kosong or max_kosong or rentang_nol:
            return pd.Series(0.0, index=seri.index)
        return (seri - min_val) / (max_val - min_val)
    
    def get_top10_prioritas(data):
        filtered_data = data.copy()
        filtered_data['Provinsi'] = filtered_data['Provinsi'].astype(str).str.strip().str.upper()
        provinsi_tidak_valid = [
            'INDONESIA', '38 PROVINSI', 'TOTAL', 'NAN', '', 'JUMLAH',
            'LUAR NEGERI', 'LUAR_NEGARA', 'LUAR-NEGERI', 'SUMBER'
        ]
        filtered_data = filtered_data[~filtered_data['Provinsi'].isin(provinsi_tidak_valid)]
        return filtered_data.sort_values('skor_prioritas_baru', ascending=False).head(10)
    
    # Visualization functions
    def viz_2_estimasi_after_fe():
        plot_data = get_top10_prioritas(latihan_fe).sort_values('estimasi_pelajar_terjangkau', ascending=False)
        plt.figure(figsize=(12, 6))
        sns.barplot(
            data=plot_data,
            x='estimasi_pelajar_terjangkau',
            y='Provinsi',
            hue='Provinsi',
            dodge=False,
            legend=False,
            palette='viridis',
        )
        plt.title('Top 10 Provinsi dengan Estimasi Pelajar Terjangkau Tertinggi\n(After Feature Engineering)', 
                  fontsize=13, fontweight='bold')
        plt.xlabel('Estimasi Pelajar Terjangkau')
        plt.ylabel('Provinsi')
        plt.tight_layout()
        return plt
    
    def viz_7_heatmap_after_fe():
        top10 = get_top10_prioritas(latihan_fe)
        kolom_heatmap = [
            'pelajar_aktif',
            'persen_telepon',
            'persen_akses_internet_sma',
            'rasio_sinyal_lte',
            'skor_jangkauan',
        ]
        heatmap_data = top10.set_index('Provinsi')[kolom_heatmap].copy()
        heatmap_norm = heatmap_data.apply(normalisasi_0_1)
        plt.figure(figsize=(12, 7))
        sns.heatmap(
            heatmap_norm,
            cmap='YlGnBu',
            annot=True,
            fmt='.2f',
            linewidths=0.5,
            cbar_kws={'label': 'Skala Normalisasi (0-1)'},
        )
        plt.title('Heatmap Kesiapan dan Potensi Jangkauan (Top 10 Provinsi)\n(After Feature Engineering)', 
                  fontsize=13, fontweight='bold')
        plt.xlabel('Indikator')
        plt.ylabel('Provinsi')
        plt.tight_layout()
        return plt
    
    def viz_9_scatter_after_fe():
        top10_fe = get_top10_prioritas(latihan_fe)
        plt.figure(figsize=(10, 6))
        sns.scatterplot(
            data=top10_fe,
            x='pelajar_aktif',
            y='skor_jangkauan',
            size='estimasi_pelajar_terjangkau',
            hue='estimasi_pelajar_terjangkau',
            sizes=(40, 500),
            palette='crest',
            legend=False,
        )
        plt.title('Peta Potensi Pelajar Terjangkau per Provinsi\n(Top 10 After Feature Engineering)', 
                  fontsize=13, fontweight='bold')
        plt.xlabel('Pelajar Aktif')
        plt.ylabel('Skor Jangkauan (0-1)')
        plt.tight_layout()
        return plt
    
    return {
        'after_fe': latihan_fe,
        'visualisasi': {
            '2_Estimasi_After_FE': viz_2_estimasi_after_fe,
            '7_Heatmap_After_FE': viz_7_heatmap_after_fe,
            '9_Scatter_After_FE': viz_9_scatter_after_fe,
        }
    }


def load_pertanyaan_dua_from_notebook(notebook_path):
    """
    Load data dari Untitled3.ipynb untuk pertanyaan dua.
    
    Args:
        notebook_path (str): Path ke Untitled3.ipynb
        
    Returns:
        dict: Berisi data dan visualisasi functions
    """
    # Determine data directory
    notebook_dir = os.path.dirname(os.path.abspath(notebook_path))
    data_dir = os.path.dirname(notebook_dir)  # Go up one level
    
    # Execute notebook
    exec_globals = execute_notebook(notebook_path, data_dir)
    
    # Extract data yang penting
    df_iptik = exec_globals.get('df_iptik_final')
    df_aps = exec_globals.get('df_aps_final')
    corr_matrix = exec_globals.get('corr_matrix')
    
    if df_iptik is None or df_aps is None or corr_matrix is None:
        raise ValueError("❌ df_iptik, df_aps, atau corr_matrix tidak ditemukan di notebook.")
    
    # TODO: Tambah visualisasi functions untuk pertanyaan dua jika diperlukan
    # Untuk sekarang return data saja
    
    return {
        'df_iptik': df_iptik,
        'df_aps': df_aps,
        'corr_matrix': corr_matrix,
        'visualisasi': {}
    }

#!/usr/bin/env python3
"""Quick verification that path fix resolved the pelajar_aktif=0 bug."""

import sys
import os
from pathlib import Path

# Add capstone-streamlit to path for imports
capstone_streamlit = Path(__file__).parent / "capstone-streamlit"
sys.path.insert(0, str(capstone_streamlit))

# Import notebook executor
from utils.notebook_executor import load_pertanyaan_satu_from_notebook

# Test: load Q1 data
root_dir = Path(__file__).parent
notebook_path = root_dir / "pertanyaan_satu" / "main.ipynb"

print(f"\n📊 Testing path resolution fix...")
print(f"   Notebook path: {notebook_path}")
print(f"   Notebook exists: {notebook_path.exists()}")

result = load_pertanyaan_satu_from_notebook(str(notebook_path.resolve()))
latihan_fe = result['after_fe']

# Check the 3 provinces mentioned in bug report
test_provinces = ['ACEH', 'PAPUA', 'PAPUA BARAT DAYA']
expected_values = {
    'ACEH': 142610,
    'PAPUA': 35541,
    'PAPUA BARAT DAYA': 14907
}

print(f"\n✅ Verification Results:")
print(f"   Total provinces: {len(latihan_fe)}")
print(f"\n   Checking pelajar_aktif values:")

all_correct = True
for province in test_provinces:
    if province in latihan_fe['Provinsi'].values:
        value = latihan_fe[latihan_fe['Provinsi'] == province]['pelajar_aktif'].iloc[0]
        expected = expected_values[province]
        status = "✅" if abs(value - expected) < 1 else "❌"
        if abs(value - expected) >= 1:
            all_correct = False
        print(f"   {status} {province}: {value:.0f} (expected: {expected})")
    else:
        print(f"   ❌ {province}: NOT FOUND in data")
        all_correct = False

if all_correct:
    print(f"\n🎉 SUCCESS: All pelajar_aktif values are correct!")
else:
    print(f"\n⚠️  FAILED: Some values don't match expected results")
    sys.exit(1)

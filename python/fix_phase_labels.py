"""
fix_phase_labels.py
-------------------
Standardizes phase labels in cart_trials_clean.csv
"""

import pandas as pd
import os

csv_path = os.path.join(os.path.dirname(__file__), "..", "data", "cart_trials_clean.csv")

df = pd.read_csv(csv_path)
print(f"Loaded {df.shape[0]} records")
print("\nBefore fix:")
print(df["phase"].value_counts())

phase_map = {
    "PHASE1":           "Phase 1",
    "PHASE1 | PHASE2":  "Phase 1/2",
    "PHASE2":           "Phase 2",
    "PHASE2 | PHASE3":  "Phase 2/3",
    "PHASE3":           "Phase 3",
    "PHASE4":           "Phase 4",
    "EARLY_PHASE1":     "Early Phase 1",
    "":                 "N/A",
}

df["phase"] = df["phase"].replace(phase_map)
df["phase"] = df["phase"].fillna("N/A")

print("\nAfter fix:")
print(df["phase"].value_counts())

df.to_csv(csv_path, index=False)
print(f"\nSaved → {csv_path}")
print("Done!")

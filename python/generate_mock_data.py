"""
generate_mock_data.py
---------------------
Generates a realistic CAR-T clinical trials dataset (~500 records)
based on real CAR-T products, cancer types, and trial patterns.

Use this to build and test the pipeline locally.
When you run fetch_cart_data.py on your own machine with internet access,
replace this CSV with the real one — all downstream SQL and Python code
will work exactly the same way.
"""

import pandas as pd
import numpy as np
import os
import random
from datetime import date, timedelta

random.seed(42)
np.random.seed(42)

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ── Real CAR-T products and pipeline candidates ──────────────────────────────
CART_PRODUCTS = [
    "Axicabtagene ciloleucel (Yescarta)",
    "Tisagenlecleucel (Kymriah)",
    "Lisocabtagene maraleucel (Breyanzi)",
    "Idecabtagene vicleucel (Abecma)",
    "Ciltacabtagene autoleucel (Carvykti)",
    "Brexucabtagene autoleucel (Tecartus)",
    "Investigational CD19 CAR-T",
    "Investigational BCMA CAR-T",
    "Investigational CD22 CAR-T",
    "Investigational CD33 CAR-T",
    "Investigational Dual-target CAR-T",
    "Allogeneic CAR-T (off-the-shelf)",
    "Investigational GD2 CAR-T",
    "Investigational Mesothelin CAR-T",
]

CONDITIONS = [
    "Diffuse Large B-Cell Lymphoma",
    "Acute Lymphoblastic Leukemia",
    "Multiple Myeloma",
    "Follicular Lymphoma",
    "Mantle Cell Lymphoma",
    "Acute Myeloid Leukemia",
    "Chronic Lymphocytic Leukemia",
    "B-cell Non-Hodgkin Lymphoma",
    "Relapsed/Refractory B-cell Lymphoma",
    "Pediatric ALL",
    "T-cell Lymphoma",
    "Solid Tumor - Neuroblastoma",
    "Solid Tumor - Mesothelioma",
    "Solid Tumor - Lung Cancer",
]

SPONSORS = [
    ("Kite Pharma / Gilead",        "INDUSTRY"),
    ("Novartis",                     "INDUSTRY"),
    ("Bristol Myers Squibb",         "INDUSTRY"),
    ("Janssen / Johnson & Johnson",  "INDUSTRY"),
    ("Legend Biotech",               "INDUSTRY"),
    ("Gracell Biotechnologies",      "INDUSTRY"),
    ("Poseida Therapeutics",         "INDUSTRY"),
    ("National Cancer Institute",    "NIH"),
    ("Memorial Sloan Kettering",     "OTHER"),
    ("MD Anderson Cancer Center",    "OTHER"),
    ("University of Pennsylvania",   "OTHER"),
    ("Fred Hutchinson Cancer Center","OTHER"),
    ("Peking University",            "OTHER"),
    ("Chinese PLA General Hospital", "OTHER"),
    ("University of Toronto",        "OTHER"),
]

COUNTRIES_WEIGHTED = (
    ["United States"] * 40 +
    ["China"]         * 25 +
    ["United Kingdom"] * 8 +
    ["Germany"]        * 6 +
    ["France"]         * 5 +
    ["Australia"]      * 4 +
    ["Canada"]         * 4 +
    ["Japan"]          * 4 +
    ["South Korea"]    * 2 +
    ["Israel"]         * 2
)

PHASES = ["Phase 1", "Phase 1 | Phase 2", "Phase 2", "Phase 3", "N/A"]
PHASE_WEIGHTS = [0.35, 0.20, 0.30, 0.10, 0.05]

STATUSES = [
    "COMPLETED", "RECRUITING", "ACTIVE_NOT_RECRUITING",
    "TERMINATED", "WITHDRAWN", "NOT_YET_RECRUITING", "SUSPENDED"
]
STATUS_WEIGHTS = [0.28, 0.30, 0.18, 0.10, 0.05, 0.07, 0.02]

GENDERS = ["ALL", "ALL", "ALL", "FEMALE", "MALE"]  # weighted toward ALL

STD_AGES = [
    "ADULT",
    "ADULT | OLDER_ADULT",
    "CHILD | ADULT",
    "CHILD | ADULT | OLDER_ADULT",
]


def random_date(start_year=2010, end_year=2024):
    start = date(start_year, 1, 1)
    end   = date(end_year, 12, 31)
    delta = (end - start).days
    return start + timedelta(days=random.randint(0, delta))


def make_trial(i):
    nct_num    = f"NCT{40000000 + i:08d}"
    product    = random.choice(CART_PRODUCTS)
    condition  = random.choice(CONDITIONS)
    sponsor, sponsor_class = random.choice(SPONSORS)
    phase      = np.random.choice(PHASES, p=PHASE_WEIGHTS)
    status     = np.random.choice(STATUSES, p=STATUS_WEIGHTS)
    gender     = random.choice(GENDERS)
    std_age    = random.choice(STD_AGES)
    country    = random.choice(COUNTRIES_WEIGHTED)

    start_dt   = random_date(2010, 2023)
    duration   = random.randint(12, 72)   # months
    comp_dt    = start_dt + timedelta(days=duration * 30)
    comp_dt    = min(comp_dt, date(2026, 12, 31))

    # Enrollment varies by phase
    enrollment_ranges = {
        "Phase 1":           (6,  50),
        "Phase 1 | Phase 2": (20, 100),
        "Phase 2":           (50, 300),
        "Phase 3":           (200, 800),
        "N/A":               (5,  40),
    }
    lo, hi    = enrollment_ranges.get(phase, (10, 100))
    enrollment = random.randint(lo, hi)

    # Pediatric trials mostly ALL or pediatric conditions
    is_pediatric = "CHILD" in std_age or "Pediatric" in condition

    # Results more likely for completed older trials
    results_posted = (
        status == "COMPLETED" and
        start_dt.year < 2021 and
        random.random() > 0.4
    )

    min_age = 2  if is_pediatric else random.choice([18, 18, 18, 12, 6])
    max_age = random.choice([75, 80, 85, None])

    primary_outcomes = [
        "Overall Response Rate (ORR)",
        "Complete Response Rate (CRR)",
        "Progression-Free Survival (PFS)",
        "Overall Survival (OS)",
        "Safety and Tolerability",
        "Duration of Response (DOR)",
        "Cytokine Release Syndrome Incidence",
        "Maximum Tolerated Dose (MTD)",
    ]

    return {
        "trial_id":           nct_num,
        "title":              f"A Study of {product} in Patients with {condition}",
        "status":             status,
        "phase":              phase,
        "start_date":         start_dt.isoformat(),
        "completion_date":    comp_dt.isoformat(),
        "primary_completion": (start_dt + timedelta(days=duration * 25)).isoformat(),
        "enrollment":         enrollment,
        "enrollment_type":    random.choice(["ACTUAL", "ESTIMATED"]),
        "conditions":         condition,
        "intervention_names": product,
        "intervention_types": "BIOLOGICAL",
        "sponsor":            sponsor,
        "sponsor_class":      sponsor_class,
        "countries":          country,
        "min_age":            min_age,
        "max_age":            max_age if max_age else 99,
        "gender":             gender,
        "std_ages":           std_age,
        "primary_outcome":    random.choice(primary_outcomes),
        "results_posted":     results_posted,
        "start_year":         start_dt.year,
        "is_pediatric":       is_pediatric,
    }


# ── Generate 500 trials ──────────────────────────────────────────────────────
print("Generating 500 mock CAR-T clinical trial records...")
records = [make_trial(i) for i in range(1, 501)]
df = pd.DataFrame(records)

# Sort by start date
df["start_date"] = pd.to_datetime(df["start_date"])
df = df.sort_values("start_date").reset_index(drop=True)

# Save
out_path = os.path.join(OUTPUT_DIR, "cart_trials_clean.csv")
df.to_csv(out_path, index=False)

print(f"\nSaved → {out_path}")
print(f"Shape: {df.shape[0]} rows × {df.shape[1]} columns")
print("\nStatus breakdown:")
print(df["status"].value_counts().to_string())
print("\nPhase breakdown:")
print(df["phase"].value_counts().to_string())
print("\nTop 5 countries:")
print(df["countries"].value_counts().head(5).to_string())
print("\nTop 5 conditions:")
print(df["conditions"].value_counts().head(5).to_string())
print("\nDone. Ready for SQL import and analysis.")

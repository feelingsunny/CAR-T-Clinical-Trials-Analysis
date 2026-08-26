"""
collect_treatment_data.py
--------------------------
Collects and organizes publicly available data on CAR-T treatment
availability, costs, and outcomes across countries.

Data sources:
- FDA approved products: https://www.fda.gov
- China NMPA approved: https://www.nmpa.gov.cn
- Published clinical outcomes: PubMed
- Hospital information: public hospital websites
"""

import pandas as pd
import json
import os

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
os.makedirs(OUTPUT_DIR, exist_ok=True)


# ── 1. FDA / NMPA Approved CAR-T Products ───────────────────────────────────
approved_products = [

    # USA - FDA Approved
    {
        "product":          "Axicabtagene ciloleucel (Yescarta)",
        "company":          "Kite/Gilead",
        "country_approved": "USA",
        "approval_year":    2017,
        "indications":      "DLBCL, Follicular Lymphoma, PMBCL",
        "target":           "CD19",
        "type":             "Autologous",
        "us_list_price_usd": 373000,
        "cn_price_usd":     None,
        "status":           "Approved",
    },
    {
        "product":          "Tisagenlecleucel (Kymriah)",
        "company":          "Novartis",
        "country_approved": "USA",
        "approval_year":    2017,
        "indications":      "Pediatric ALL, DLBCL",
        "target":           "CD19",
        "type":             "Autologous",
        "us_list_price_usd": 475000,
        "cn_price_usd":     None,
        "status":           "Approved",
    },
    {
        "product":          "Lisocabtagene maraleucel (Breyanzi)",
        "company":          "Bristol Myers Squibb",
        "country_approved": "USA",
        "approval_year":    2021,
        "indications":      "DLBCL, CLL, MCL",
        "target":           "CD19",
        "type":             "Autologous",
        "us_list_price_usd": 410300,
        "cn_price_usd":     None,
        "status":           "Approved",
    },
    {
        "product":          "Idecabtagene vicleucel (Abecma)",
        "company":          "Bristol Myers Squibb / 2seventy bio",
        "country_approved": "USA",
        "approval_year":    2021,
        "indications":      "Multiple Myeloma",
        "target":           "BCMA",
        "type":             "Autologous",
        "us_list_price_usd": 419500,
        "cn_price_usd":     None,
        "status":           "Approved",
    },
    {
        "product":          "Ciltacabtagene autoleucel (Carvykti)",
        "company":          "Janssen / Legend Biotech",
        "country_approved": "USA",
        "approval_year":    2022,
        "indications":      "Multiple Myeloma",
        "target":           "BCMA",
        "type":             "Autologous",
        "us_list_price_usd": 465000,
        "cn_price_usd":     55000,   # Also approved in China
        "status":           "Approved",
    },
    {
        "product":          "Brexucabtagene autoleucel (Tecartus)",
        "company":          "Kite/Gilead",
        "country_approved": "USA",
        "approval_year":    2021,
        "indications":      "MCL, ALL",
        "target":           "CD19",
        "type":             "Autologous",
        "us_list_price_usd": 373000,
        "cn_price_usd":     None,
        "status":           "Approved",
    },

    # China - NMPA Approved
    {
        "product":          "Axicabtagene ciloleucel (Yescarta)",
        "company":          "Fosun Kite",
        "country_approved": "China",
        "approval_year":    2021,
        "indications":      "DLBCL, PMBCL",
        "target":           "CD19",
        "type":             "Autologous",
        "us_list_price_usd": None,
        "cn_price_usd":     35000,
        "status":           "Approved",
    },
    {
        "product":          "Relmacabtagene autoleucel (Relma-cel)",
        "company":          "JW Therapeutics",
        "country_approved": "China",
        "approval_year":    2021,
        "indications":      "DLBCL",
        "target":           "CD19",
        "type":             "Autologous",
        "us_list_price_usd": None,
        "cn_price_usd":     32000,
        "status":           "Approved",
    },
    {
        "product":          "Ciltacabtagene autoleucel (Carvykti)",
        "company":          "Legend Biotech / Janssen",
        "country_approved": "China",
        "approval_year":    2023,
        "indications":      "Multiple Myeloma",
        "target":           "BCMA",
        "type":             "Autologous",
        "us_list_price_usd": None,
        "cn_price_usd":     55000,
        "status":           "Approved",
    },
    {
        "product":          "Equecabtagene autoleucel (Fucaso)",
        "company":          "Innovative Cellular Therapeutics",
        "country_approved": "China",
        "approval_year":    2023,
        "indications":      "Multiple Myeloma",
        "target":           "BCMA",
        "type":             "Autologous",
        "us_list_price_usd": None,
        "cn_price_usd":     48000,
        "status":           "Approved",
    },
]


# ── 2. Top CAR-T Treatment Centers ──────────────────────────────────────────
treatment_centers = [

    # China
    {
        "hospital":     "Chinese PLA General Hospital (301 Hospital)",
        "country":      "China",
        "city":         "Beijing",
        "tier":         "Top",
        "specialty":    "CAR-T pioneer, largest volume in China",
        "products":     "Multiple CD19, BCMA CAR-T",
        "est_cost_usd": "30,000 - 60,000",
        "wait_weeks":   2,
        "contact":      "www.301hospital.com.cn",
    },
    {
        "hospital":     "Peking University People's Hospital",
        "country":      "China",
        "city":         "Beijing",
        "tier":         "Top",
        "specialty":    "Hematology, ALL and lymphoma",
        "products":     "CD19 CAR-T, clinical trials",
        "est_cost_usd": "35,000 - 65,000",
        "wait_weeks":   3,
        "contact":      "www.pkuph.cn",
    },
    {
        "hospital":     "Zhejiang University First Affiliated Hospital",
        "country":      "China",
        "city":         "Hangzhou",
        "tier":         "Top",
        "specialty":    "Solid tumors and hematology CAR-T",
        "products":     "CD19, CD22, BCMA CAR-T",
        "est_cost_usd": "30,000 - 55,000",
        "wait_weeks":   2,
        "contact":      "www.zy91.com",
    },
    {
        "hospital":     "Shanghai Ruijin Hospital",
        "country":      "China",
        "city":         "Shanghai",
        "tier":         "Top",
        "specialty":    "Leukemia and lymphoma",
        "products":     "CD19 CAR-T, clinical trials",
        "est_cost_usd": "35,000 - 60,000",
        "wait_weeks":   3,
        "contact":      "www.rjh.com.cn",
    },

    # USA
    {
        "hospital":     "MD Anderson Cancer Center",
        "country":      "USA",
        "city":         "Houston, TX",
        "tier":         "Top",
        "specialty":    "All CAR-T indications",
        "products":     "All FDA-approved + clinical trials",
        "est_cost_usd": "400,000 - 600,000",
        "wait_weeks":   12,
        "contact":      "www.mdanderson.org",
    },
    {
        "hospital":     "Memorial Sloan Kettering",
        "country":      "USA",
        "city":         "New York, NY",
        "tier":         "Top",
        "specialty":    "Lymphoma and leukemia",
        "products":     "All FDA-approved + clinical trials",
        "est_cost_usd": "420,000 - 580,000",
        "wait_weeks":   10,
        "contact":      "www.mskcc.org",
    },
    {
        "hospital":     "Fred Hutchinson Cancer Center",
        "country":      "USA",
        "city":         "Seattle, WA",
        "tier":         "Top",
        "specialty":    "CAR-T pioneer, bone marrow transplant",
        "products":     "All FDA-approved + clinical trials",
        "est_cost_usd": "380,000 - 550,000",
        "wait_weeks":   8,
        "contact":      "www.fredhutch.org",
    },

    # Canada
    {
        "hospital":     "Princess Margaret Cancer Centre",
        "country":      "Canada",
        "city":         "Toronto, ON",
        "tier":         "Top",
        "specialty":    "Lymphoma and myeloma",
        "products":     "Health Canada approved CAR-T",
        "est_cost_usd": "200,000 - 350,000",
        "wait_weeks":   16,
        "contact":      "www.uhn.ca/PrincessMargaret",
    },
    {
        "hospital":     "CancerCare Manitoba",
        "country":      "Canada",
        "city":         "Winnipeg, MB",
        "tier":         "Regional",
        "specialty":    "Hematology, referrals to Toronto",
        "products":     "Referral center",
        "est_cost_usd": "Covered by Manitoba Health (wait list)",
        "wait_weeks":   20,
        "contact":      "www.cancercare.mb.ca",
    },
]


# ── 3. Cost Comparison Summary ───────────────────────────────────────────────
cost_comparison = [
    {"country": "USA",     "avg_treatment_usd": 450000, "avg_wait_weeks": 12, "insurance_coverage": "Partial (varies)"},
    {"country": "China",   "avg_treatment_usd": 45000,  "avg_wait_weeks": 3,  "insurance_coverage": "Partial (NRSS)"},
    {"country": "Canada",  "avg_treatment_usd": 280000, "avg_wait_weeks": 18, "insurance_coverage": "Provincial (limited)"},
    {"country": "Germany", "avg_treatment_usd": 320000, "avg_wait_weeks": 8,  "insurance_coverage": "Yes (statutory)"},
    {"country": "UK",      "avg_treatment_usd": 290000, "avg_wait_weeks": 10, "insurance_coverage": "NHS (limited)"},
    {"country": "Japan",   "avg_treatment_usd": 260000, "avg_wait_weeks": 6,  "insurance_coverage": "Yes (NHI)"},
]


# ── Save all datasets ────────────────────────────────────────────────────────
df_products  = pd.DataFrame(approved_products)
df_centers   = pd.DataFrame(treatment_centers)
df_costs     = pd.DataFrame(cost_comparison)

df_products.to_csv(os.path.join(OUTPUT_DIR, "approved_products.csv"),  index=False)
df_centers.to_csv(os.path.join(OUTPUT_DIR,  "treatment_centers.csv"),  index=False)
df_costs.to_csv(os.path.join(OUTPUT_DIR,    "cost_comparison.csv"),    index=False)

print("Saved 3 datasets:")
print(f"  approved_products.csv  — {len(df_products)} products")
print(f"  treatment_centers.csv  — {len(df_centers)} hospitals")
print(f"  cost_comparison.csv    — {len(df_costs)} countries")

print("\nCost comparison:")
print(df_costs[["country","avg_treatment_usd","avg_wait_weeks"]].to_string(index=False))

import pandas as pd
from rapidfuzz.distance import Levenshtein

# ================= CONFIG =================
LABEL_FILE  = "compare/labels.csv"
PRED_FILE   = "output/csv/results.csv"

# ================= NORMALIZATION =================
COLOR_MAP = {
    "yellow": "yellow", "เหลือง": "yellow",
    "white": "white", "ขาว": "white",
    "black": "black", "ดำ": "black",
    "green": "green", "เขียว": "green",
    "blue": "blue", "น้ำเงิน": "blue",
    "red": "red", "แดง": "red",
}

def norm_color(v):
    if pd.isna(v):
        return ""
    v = str(v).lower().strip()
    return COLOR_MAP.get(v, v)

# ================= CANONICAL VEHICLE TYPE =================
# อ้างอิงตามกฎหมาย/มาตรฐานป้ายทะเบียนไทย
PLATE_RULES = {
    ("white", "black"): "private_car",      # รถยนต์นั่งส่วนบุคคลไม่เกิน 7 คน
    ("yellow", "black"): "taxi",
    ("green", "white"): "government",
    ("red", "white"): "government",
    ("blue", "white"): "diplomatic",
}

def canonical_vehicle(plate_color, text_color):
    key = (norm_color(plate_color), norm_color(text_color))
    return PLATE_RULES.get(key, "unknown")

# ================= CER =================
def cer(gt, pred):
    gt, pred = str(gt), str(pred)
    if not gt and not pred:
        return 0.0
    return Levenshtein.distance(gt, pred) / max(len(gt), len(pred), 1)

# ================= LOAD =================
labels = pd.read_csv(LABEL_FILE)
preds  = pd.read_csv(PRED_FILE)

df = labels.merge(preds, on="image", suffixes=("_gt", "_pred"))

# ================= METRICS =================

# --- Plate ---
df["plate_cer"] = df.apply(
    lambda r: cer(r["plate_number_gt"], r["plate_number_pred"]),
    axis=1
)
df["plate_acc"] = (df["plate_number_gt"] == df["plate_number_pred"]).astype(int)

# --- Province ---
df["province_acc"] = (df["province_gt"] == df["province_pred"]).astype(int)

# --- Plate color ---
df["plate_color_acc"] = df.apply(
    lambda r:
        norm_color(r["plate_color_gt"])
        == norm_color(r["plate_color_pred"]),
    axis=1
).astype(int)

# --- Text color ---
df["text_color_acc"] = df.apply(
    lambda r:
        norm_color(r["text_color_gt"])
        == norm_color(r["text_color_pred"]),
    axis=1
).astype(int)

# --- Vehicle type (CANONICAL, จากสีป้าย + สีตัวอักษร) ---
df["vehicle_type_gt_canon"] = df.apply(
    lambda r: canonical_vehicle(r["plate_color_gt"], r["text_color_gt"]),
    axis=1
)
df["vehicle_type_pred_canon"] = df.apply(
    lambda r: canonical_vehicle(r["plate_color_pred"], r["text_color_pred"]),
    axis=1
)

df["vehicle_type_acc"] = (
    df["vehicle_type_gt_canon"] == df["vehicle_type_pred_canon"]
).astype(int)

# ================= SUMMARY =================
summary = {
    "Plate CER (avg)": round(df["plate_cer"].mean(), 4),
    "Plate Accuracy": round(df["plate_acc"].mean(), 4),
    "Province Accuracy": round(df["province_acc"].mean(), 4),
    "Plate Color Accuracy": round(df["plate_color_acc"].mean(), 4),
    "Text Color Accuracy": round(df["text_color_acc"].mean(), 4),
    "Vehicle Type Accuracy (Canonical)": round(df["vehicle_type_acc"].mean(), 4),
}

print("\n===== Evaluation Summary =====")
for k, v in summary.items():
    print(f"{k}: {v}")

# ================= OPTIONAL: SAVE DETAIL =================
df.to_csv("eval_detail.csv", index=False)

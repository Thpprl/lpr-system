import csv
from pipeline.evaluation.cer import cer
from pipeline.evaluation.field_accuracy import field_accuracy
from pipeline.evaluation.normalizer import norm_color, norm_vehicle

FIELDS = ["plate_number", "province", "plate_color", "text_color", "vehicle_type"]

def load_csv(path):
    data = {}
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            data[row["image"]] = row
    return data

def evaluate_lpr(label_csv, pred_csv):
    labels = load_csv(label_csv)
    preds = load_csv(pred_csv)

    results = []

    for img, gt in labels.items():
        if img not in preds:
            continue

        pr = preds[img]

        # normalize
        gt["plate_color"] = norm_color(gt["plate_color"])
        pr["plate_color"] = norm_color(pr["plate_color"])
        gt["text_color"]  = norm_color(gt["text_color"])
        pr["text_color"]  = norm_color(pr["text_color"])
        gt["vehicle_type"] = norm_vehicle(gt["vehicle_type"])
        pr["vehicle_type"] = norm_vehicle(pr["vehicle_type"])

        cer_score = cer(gt["plate_number"], pr["plate_number"])
        field_acc = field_accuracy(gt, pr, FIELDS)

        results.append({
            "image": img,
            "cer": cer_score,
            "field_accuracy": field_acc
        })

    return results

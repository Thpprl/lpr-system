import json
import csv
from pathlib import Path
from datetime import datetime

OUTPUT_DIR = Path("output")
JSON_DIR = OUTPUT_DIR / "json"
CSV_DIR = OUTPUT_DIR / "csv"

JSON_DIR.mkdir(parents=True, exist_ok=True)
CSV_DIR.mkdir(parents=True, exist_ok=True)

CSV_FILE = CSV_DIR / "results.csv"


def save_json(result: dict):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    path = JSON_DIR / f"result_{timestamp}.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    return path


def save_csv(result: dict):
    is_new = not CSV_FILE.exists()

    with open(CSV_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "image",
                "plate_number",
                "province",
                "plate_color",
                "text_color",
                "vehicle_type",
            ],
        )

        if is_new:
            writer.writeheader()

        writer.writerow({
            "image": result.get("image"),
            "plate_number": result.get("plate_number"),
            "province": result.get("province"),
            "plate_color": result.get("plate_color"),
            "text_color": result.get("text_color"),
            "vehicle_type": result.get("vehicle_type"),
        })

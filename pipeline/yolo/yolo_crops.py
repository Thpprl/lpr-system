from ultralytics import YOLO
from pathlib import Path
import cv2

MODEL_PATH = "models/yolo/best.pt"
OUTPUT_DIR = Path("output/crops")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

model = YOLO(MODEL_PATH)

def crop_plate(image_path: str) -> list[str]:
    img = cv2.imread(image_path)
    results = model(img)

    saved_paths = []
    for i, box in enumerate(results[0].boxes.xyxy):
        x1, y1, x2, y2 = map(int, box)
        crop = img[y1:y2, x1:x2]

        out_path = OUTPUT_DIR / f"plate_{i}.jpg"
        cv2.imwrite(str(out_path), crop)
        saved_paths.append(str(out_path))

    return saved_paths

from pathlib import Path
from pipeline.pipeline import run_pipeline
from pipeline.utils.saver import save_json, save_csv

SUPPORTED_EXT = {".jpg", ".jpeg", ".png"}


def run_pipeline_batch(folder_path: str, save: bool = True):
    folder = Path(folder_path)

    if not folder.exists():
        raise FileNotFoundError(f"Folder not found: {folder_path}")

    results = []

    for img_path in sorted(folder.iterdir()):
        if img_path.suffix.lower() not in SUPPORTED_EXT:
            continue

        print(f"\n🖼️ Processing: {img_path.name}")

        try:
            result = run_pipeline(str(img_path))
            result["image"] = img_path.name

            if save:
                save_json(result)
                save_csv(result)

            results.append(result)

        except Exception as e:
            print(f"❌ Failed: {img_path.name} -> {e}")

    return results

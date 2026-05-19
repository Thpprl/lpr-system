import sys
from pipeline.pipeline import run_pipeline
from pipeline.batch import run_pipeline_batch
from pipeline.postprocess.formatter import format_lpr_result
from pipeline.utils.saver import save_json, save_csv


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage:")
        print("  python run.py single <image_path> [--save]")
        print("  python run.py batch <folder_path> [--save]")
        sys.exit(1)

    mode = sys.argv[1]
    path = sys.argv[2]
    save = "--save" in sys.argv  # 👈 เพิ่มแค่นี้

    # ======================
    # Single image
    # ======================
    if mode == "single":
        result = run_pipeline(path)

        print(format_lpr_result(result))

        if save:
            save_json(result)
            save_csv(result)

    # ======================
    # Batch mode
    # ======================
    elif mode == "batch":
        results = run_pipeline_batch(path)

        print("\n✅ Batch finished")

        for r in results:
            print(f"\n📂 Image: {r['image']}")
            print(format_lpr_result(r))

            if save:
                save_json(r)
                save_csv(r)

    else:
        print("❌ Unknown mode:", mode)

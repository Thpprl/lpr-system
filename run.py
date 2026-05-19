import sys
from pipeline.pipeline import run_pipeline
from pipeline.batch import run_pipeline_batch
from pipeline.postprocess.formatter import format_lpr_result
from pipeline.utils.saver import save_json, save_csv


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python run.py single <image_path> [--save]")
        print("  python run.py batch <folder_path> [--save]")
        print("  python run.py web [--port <port>]")
        sys.exit(1)

    mode = sys.argv[1]

    # ======================
    # Web server mode
    # ======================
    if mode == "web":
        import uvicorn
        port = 8000
        if "--port" in sys.argv:
            try:
                port_idx = sys.argv.index("--port") + 1
                port = int(sys.argv[port_idx])
            except (ValueError, IndexError):
                pass
        print(f"🚀 Starting Web UI server on http://127.0.0.1:{port} ...")
        uvicorn.run("web.app:app", host="127.0.0.1", port=port, reload=True)

    # ======================
    # Single image
    # ======================
    elif mode == "single":
        if len(sys.argv) < 3:
            print("Error: Missing image path")
            print("Usage: python run.py single <image_path> [--save]")
            sys.exit(1)
        path = sys.argv[2]
        save = "--save" in sys.argv
        result = run_pipeline(path)

        print(format_lpr_result(result))

        if save:
            save_json(result)
            save_csv(result)

    # ======================
    # Batch mode
    # ======================
    elif mode == "batch":
        if len(sys.argv) < 3:
            print("Error: Missing folder path")
            print("Usage: python run.py batch <folder_path> [--save]")
            sys.exit(1)
        path = sys.argv[2]
        save = "--save" in sys.argv
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


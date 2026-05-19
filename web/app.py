from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
import shutil
import os
import sys

# Add the project root to sys.path to allow imports from pipeline
sys.path.append(str(Path(__file__).parent.parent))

from pipeline.pipeline import run_pipeline

app = FastAPI(
    title="Thai License Plate Recognition (LPR) System",
    description="FastAPI Web Server for LPR pipeline",
    version="1.0.0"
)

# Base directories
BASE_DIR = Path(__file__).parent.parent
STATIC_DIR = BASE_DIR / "web" / "static"
TEMPLATES_DIR = BASE_DIR / "web" / "templates"
OUTPUT_DIR = BASE_DIR / "output"
TEMP_DIR = OUTPUT_DIR / "temp"

# Create directories if they don't exist
TEMP_DIR.mkdir(parents=True, exist_ok=True)

# Mount static files and output directories
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")
app.mount("/output", StaticFiles(directory=str(OUTPUT_DIR)), name="output")

@app.get("/")
async def get_index():
    index_path = TEMPLATES_DIR / "index.html"
    if not index_path.exists():
        raise HTTPException(status_code=404, detail="Index file not found")
    return FileResponse(index_path)

@app.post("/api/predict")
async def predict_license_plate(file: UploadFile = File(...)):
    # Validate file extension
    file_ext = Path(file.filename).suffix.lower()
    if file_ext not in [".jpg", ".jpeg", ".png"]:
        return JSONResponse(
            status_code=400,
            content={"error": "Unsupported file format. Please upload JPG, JPEG, or PNG."}
        )

    # Save uploaded file to temp location
    temp_file_path = TEMP_DIR / f"upload_{os.getpid()}{file_ext}"
    try:
        with open(temp_file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Run LPR pipeline
        result = run_pipeline(str(temp_file_path))
        
        # Check if crop plate exists
        crop_dir = OUTPUT_DIR / "crops"
        crops = sorted(crop_dir.glob("plate_*.jpg"))
        
        # Default crop URL
        crop_url = None
        if crops:
            # We use the first plate crop path relative to output
            crop_url = f"/output/crops/{crops[0].name}"

        # Add crop URL and success status to response
        response_data = {
            "success": True,
            "data": {
                "plate_number": result.get("plate_number"),
                "province": result.get("province"),
                "plate_color": result.get("plate_color"),
                "text_color": result.get("text_color"),
                "vehicle_type": result.get("vehicle_type"),
                "crop_url": crop_url
            }
        }
        return response_data

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"success": False, "error": str(e)}
        )
    finally:
        # Clean up temp file
        if temp_file_path.exists():
            try:
                os.remove(temp_file_path)
            except Exception:
                pass

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)

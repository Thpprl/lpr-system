from PIL import Image
from pipeline.yolo.yolo_crops import crop_plate
from pipeline.qwen.qwen_infer import infer_qwen
from pipeline.postprocess.vehicle_type import classify_vehicle_type


def run_pipeline(image_path: str):
    # 1. YOLO detect + crop
    crops = crop_plate(image_path)

    if not crops:
        raise RuntimeError("No license plate detected")

    crop_path = crops[0]  # ใช้ plate แรกก่อน
    image = Image.open(crop_path).convert("RGB")

    # 2. Qwen infer
    result = infer_qwen(image)
    # result ควรเป็น dict:
    # {
    #   plate_number,
    #   province,
    #   plate_color,
    #   text_color
    # }

    # 3. Post-process → vehicle type
    vehicle_type = classify_vehicle_type(
        result.get("plate_color"),
        result.get("text_color")
    )

    result["vehicle_type"] = vehicle_type

    return result

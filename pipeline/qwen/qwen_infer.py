import torch
from PIL import Image
from transformers import AutoProcessor, AutoModelForVision2Seq
from peft import PeftModel

# =========================
# Config
# =========================
DEVICE = "cuda"
BASE_MODEL = "Qwen/Qwen3-VL-2B-Instruct"
LORA_PATH = "models/qwen/checkpoint-400"

# =========================
# Load processor & model (โหลดครั้งเดียว)
# =========================
processor = AutoProcessor.from_pretrained(
    BASE_MODEL,
    trust_remote_code=True
)

base_model = AutoModelForVision2Seq.from_pretrained(
    BASE_MODEL,
    torch_dtype=torch.float16,
    device_map="auto",
    trust_remote_code=True
)

model = PeftModel.from_pretrained(
    base_model,
    LORA_PATH
)

model.eval()

# =========================
# Output parser
# =========================
def parse_qwen_output(text: str) -> dict:
    """
    แปลง output จาก Qwen (string) → dict
    """
    data = {
        "plate_number": None,
        "province": None,
        "plate_color": None,
        "text_color": None,
        "raw_text": text
    }

    for line in text.splitlines():
        line = line.strip()

        if line.startswith("เลขทะเบียน"):
            data["plate_number"] = line.split(":", 1)[-1].strip()

        elif line.startswith("จังหวัด"):
            data["province"] = line.split(":", 1)[-1].strip()

        elif line.startswith("สีป้ายทะเบียน"):
            data["plate_color"] = line.split(":", 1)[-1].strip()

        elif line.startswith("สีตัวอักษร"):
            data["text_color"] = line.split(":", 1)[-1].strip()

    return data


# =========================
# Inference
# =========================
def infer_qwen(image: Image.Image) -> dict:
    """
    รับ PIL.Image → ส่งกลับ dict
    """

    messages = [
        {
            "role": "user",
            "content": [
                {"type": "image"},
                {
                    "type": "text",
                    "text": (
                        "คุณเป็นระบบอ่านป้ายทะเบียนรถในประเทศไทยจากภาพถ่าย\n\n"
                        "หน้าที่:\n"
                        "อ่านข้อความที่มองเห็นได้จากป้ายทะเบียนรถในภาพเท่านั้น\n\n"
                        "กฎสำคัญ:\n"
                        "- ตอบเป็นภาษาไทยเท่านั้น\n"
                        "- ห้ามใช้ภาษาอังกฤษและภาษาจีน\n"
                        "- ห้ามเดาค่าที่ไม่เห็นชัด\n"
                        "- ให้ตอบเฉพาะข้อมูลที่มองเห็นชัดจากตัวอักษรและสีในภาพเท่านั้น\n"
                        "- หากข้อมูลใดอ่านไม่ได้หรือไม่ชัด ให้ตอบว่า \"ไม่สามารถระบุได้\"\n\n"
                        "กฎเกี่ยวกับสี:\n"
                        "- สีป้ายทะเบียนและสีตัวอักษรให้พิจารณาจากสีที่เห็นจริงในภาพเท่านั้น\n"
                        "- ห้ามอ้างอิงจากความรู้ทั่วไปหรือรูปแบบป้าย\n\n"
                        "รูปแบบคำตอบ (ต้องตรงตามนี้เท่านั้น):\n"
                        "เลขทะเบียน:\n"
                        "จังหวัด:\n"
                        "สีป้ายทะเบียน:\n"
                        "สีตัวอักษร:\n\n"
                        "คำศัพท์ที่อนุญาต:\n"
                        "- สีป้ายทะเบียน: ขาว, เหลือง, เขียว, แดง, ฟ้า\n"
                        "- สีตัวอักษร: ดำ, ขาว, แดง\n\n"
                        "ห้ามอธิบายเพิ่มเติม\n"
                        "ห้ามใส่ข้อความนอกเหนือจาก format"
                    )
                }
            ]
        }
    ]

    # 🔥 สำคัญมาก (แก้ error image tokens)
    prompt = processor.apply_chat_template(
        messages,
        add_generation_prompt=True
    )

    inputs = processor(
        text=prompt,
        images=image,
        return_tensors="pt"
    ).to(model.device)

    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=128,
            do_sample=False
        )

    decoded = processor.batch_decode(
        outputs,
        skip_special_tokens=True
    )[0]

    return parse_qwen_output(decoded)

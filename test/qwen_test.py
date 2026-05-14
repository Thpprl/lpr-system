from llamafactory.chat import ChatModel
from PIL import Image

# -----------------------------
# Load model (Base + LoRA)
# -----------------------------
model = ChatModel(
    "Qwen/Qwen3-VL-2B-Instruct",   # base model
    "models/qwen/checkpoint-400",  # LoRA path
    "qwen3_vl",                    # template
    "cuda"                         # device
)

# -----------------------------
# Load image
# -----------------------------
image = Image.open("test/img (80).jpg").convert("RGB")

# -----------------------------
# Prompt
# -----------------------------
messages = [
    {
        "role": "user",
        "content": [
            {"type": "image", "image": image},
            {
                "type": "text",
                "text": (
                    "อ่านข้อความจากป้ายทะเบียนรถ และตอบเฉพาะในรูปแบบนี้:\n"
                    "- เลขทะเบียน:\n"
                    "- จังหวัด:\n"
                    "- สีป้ายทะเบียน:\n"
                    "- สีตัวอักษร:\n\n"
                    "ตอบเป็นภาษาไทยเท่านั้น ถ้าไม่ชัดเจนให้ตอบว่า 'ไม่สามารถระบุได้'"
                )
            }
        ]
    }
]

# -----------------------------
# Inference
# -----------------------------
response = model.chat(
    messages,
    max_new_tokens=256,
    temperature=0.1
)

print("\n=== RESULT ===")
print(response)

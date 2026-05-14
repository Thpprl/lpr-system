from ultralytics import YOLO
import torch

print("CUDA:", torch.cuda.is_available())

model = YOLO("models/yolo/best.pt")  # แก้ path ตามของคุณ
results = model("test/img (80).jpg", device=0)

print("Done YOLO")

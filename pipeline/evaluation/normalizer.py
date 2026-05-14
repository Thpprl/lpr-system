# pipeline/evaluation/normalizer.py

COLOR_MAP = {
    "white": "ขาว",
    "black": "ดำ",
    "green": "เขียว",
    "yellow": "เหลือง",
    "red": "แดง",
    "blue": "ฟ้า",
    "ขาว": "ขาว",
    "ดำ": "ดำ",
    "เขียว": "เขียว",
    "เหลือง": "เหลือง",
    "แดง": "แดง",
    "ฟ้า": "ฟ้า",
}



def norm_color(x: str):
    if not x:
        return None
    return COLOR_MAP.get(x.strip().lower(), x)

def norm_vehicle(x: str):
    if not x:
        return None
    return VEHICLE_MAP.get(x.strip(), x)

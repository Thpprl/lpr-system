import re

def parse_qwen_output(text: str) -> dict:
    result = {
        "plate_number": None,
        "province": None,
        "plate_color": None,
        "text_color": None,
    }

    for line in text.splitlines():
        if "เลขทะเบียน" in line:
            result["plate_number"] = line.split(":")[-1].strip()
        elif "จังหวัด" in line:
            result["province"] = line.split(":")[-1].strip()
        elif "สีป้ายทะเบียน" in line:
            result["plate_color"] = line.split(":")[-1].strip()
        elif "สีตัวอักษร" in line:
            result["text_color"] = line.split(":")[-1].strip()

    return result

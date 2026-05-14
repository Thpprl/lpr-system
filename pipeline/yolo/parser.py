import re

def parse_plate(text: str) -> dict:
    def find(pattern):
        m = re.search(pattern, text)
        return m.group(1).strip() if m else "ไม่สามารถระบุได้"

    return {
        "plate": find(r"ทะเบียน[:：]?\s*(.+)"),
        "province": find(r"จังหวัด[:：]?\s*(.+)"),
        "plate_color": find(r"ป้ายสี[:：]?\s*(.+)"),
        "text_color": find(r"ตัวอักษรสี[:：]?\s*(.+)")
    }

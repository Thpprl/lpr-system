def format_lpr_result(result: dict) -> str:
    return f"""
🚗 ผลการอ่านป้ายทะเบียน
-------------------------
เลขทะเบียน      : {result.get("plate_number", "-")}
จังหวัด          : {result.get("province", "-")}
สีป้ายทะเบียน   : {result.get("plate_color", "-")}
สีตัวอักษร       : {result.get("text_color", "-")}
ประเภทรถ        : {result.get("vehicle_type", "-")}
""".strip()

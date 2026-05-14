def classify_vehicle_type(plate_color: str, text_color: str) -> str:
    plate_color = plate_color.lower()
    text_color = text_color.lower()

    if plate_color == "ขาว" and text_color == "ดำ":
        return "รถยนต์ส่วนบุคคล"

    elif plate_color == "ขาว" and text_color == "น้ำเงิน":
        return "รถยนต์นั่งส่วนบุคคลเกิน 7 คน"

    elif plate_color == "ขาว" and text_color == "เขียว":
        return "รถบรรทุกส่วนบุคคล"

    elif plate_color == "เหลือง" and text_color == "ดำ":
        return "รถรับจ้าง"

    elif plate_color == "เหลือง" and text_color == "แดง":
        return "รถรับจ้างระหว่างจังหวัด"

    elif plate_color == "เหลือง" and text_color == "น้ำเงิน":
        return "รถยนต์สาธารณะ"

    elif plate_color == "เหลือง" and text_color == "เขียว":
        return "รถสามล้อ"

    elif plate_color == "เขียว" and text_color == "ขาว":
        return "รถบริการ"

    elif plate_color == "แดง" and text_color == "ขาว":
        return "รถป้ายแดง"

    elif plate_color == "ดำ" and text_color == "ขาว":
        return "รถทูต"

    elif plate_color == "ฟ้า" and text_color == "ขาว":
        return "รถองค์การ / หน่วยงานรัฐ"

    else:
        return "ไม่สามารถระบุได้"

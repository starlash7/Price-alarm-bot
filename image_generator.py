# -*- coding: utf-8 -*-
from PIL import Image, ImageDraw, ImageFont
import os

# 종목별 템플릿 설정
TEMPLATES = {
    "005930": {"file": "template.png", "crop": (5, 0, -5, 0), "y_offset": 20, "x_offset": 0, "font_size": 90},      # 삼성
    "000660": {"file": "template_hynix.png", "crop": (0, 0, 0, 0), "y_offset": 20, "x_offset": 0, "font_size": 90}, # 하이닉스
    "KOSPI": {"file": "template_kospi.png", "crop": (5, 0, -5, 0), "y_offset": -60, "x_offset": 60, "font_size": 60},  # KOSPI
}

def create_price_image(stock_code, price, is_up, is_index=False):
    """
    종목별 템플릿 이미지에 가격 오버레이
    """
    # 템플릿 선택
    template_info = TEMPLATES.get(stock_code, {"file": "template.png", "crop": (0, 0, 0, 0), "y_offset": 20})
    template_path = os.path.join(os.path.dirname(__file__), template_info["file"])

    img = Image.open(template_path).convert("RGB")

    # 종목별 crop 적용 (left, top, right, bottom)
    crop = template_info["crop"]
    if crop != (0, 0, 0, 0):
        w, h = img.size
        left = crop[0]
        top = crop[1]
        right = w + crop[2] if crop[2] < 0 else w
        bottom = h + crop[3] if crop[3] < 0 else h
        img = img.crop((left, top, right, bottom))
    
    draw = ImageDraw.Draw(img)
    
    width, height = img.size
    print(f"Template: {template_info['file']}, Size: {width}x{height}")
    
    # 폰트 설정 (종목별 크기)
    font_size = template_info.get("font_size", 120)
    font_options = [
        # macOS 폰트
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
        "/System/Library/Fonts/AppleSDGothicNeo.ttc",
        "/Library/Fonts/Arial Bold.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
        # Windows 폰트
        "C:/Windows/Fonts/GOTHICB.TTF",
        "C:/Windows/Fonts/ariblk.ttf",
        "C:/Windows/Fonts/segoeuib.ttf",
    ]
    
    price_font = None
    for font_path in font_options:
        try:
            price_font = ImageFont.truetype(font_path, font_size)
            break
        except:
            continue
    
    if price_font is None:
        price_font = ImageFont.load_default()
    
    # 가격 텍스트 (지수는 소수점, 주식은 WON)
    if is_index:
        price_text = f"{price:,.2f}"
    else:
        price_text = format(int(price), ',') + " WON"
    
    # 텍스트 크기 계산
    price_bbox = draw.textbbox((0, 0), price_text, font=price_font)
    price_width = price_bbox[2] - price_bbox[0]
    price_height = price_bbox[3] - price_bbox[1]

    # 위치 계산 (x_offset, y_offset 적용)
    y_offset = template_info.get("y_offset", 20)
    x_offset = template_info.get("x_offset", 0)
    x = (width - price_width) // 2 + x_offset
    y = (height - price_height) // 2 + y_offset

    # 텍스트가 이미지 경계를 넘지 않도록 clamp
    x = max(0, min(x, width - price_width))
    y = max(0, min(y, height - price_height))

    # 그림자 효과
    draw.text((x + 2, y + 2), price_text, fill=(0, 0, 0), font=price_font)

    # 메인 텍스트 (흰색)
    draw.text((x, y), price_text, fill=(255, 255, 255), font=price_font)

    # 종목별 개별 파일로 저장 (동시 호출 시 덮어쓰기 방지)
    output_path = os.path.join(os.path.dirname(__file__), f"price_alert_{stock_code}.png")
    img.save(output_path, "PNG")
    
    print(f"Price image created: {output_path}")
    return output_path


if __name__ == "__main__":
    # 삼성전자 테스트
    create_price_image("005930", 165000, True)
    
    # SK하이닉스 테스트
    create_price_image("000660", 841000, True)

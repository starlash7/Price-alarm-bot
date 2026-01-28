# -*- coding: utf-8 -*-
from PIL import Image, ImageDraw, ImageFont
import os

# 종목별 템플릿 설정
TEMPLATES = {
    "005930": {"file": "template.png", "crop": (5, 0, -5, 0)},        # 삼성 (흰 테두리 있음)
    "000660": {"file": "template_hynix.png", "crop": (0, 0, 0, 0)},   # 하이닉스 (테두리 없음)
}

OUTPUT_PATH = "price_alert.png"


def create_price_image(stock_code, price, is_up):
    """
    종목별 템플릿 이미지에 가격 오버레이
    """
    # 템플릿 선택
    template_info = TEMPLATES.get(stock_code, {"file": "template.png", "crop": (0, 0, 0, 0)})
    template_path = os.path.join(os.path.dirname(__file__), template_info["file"])
    
    img = Image.open(template_path).convert("RGB")
    
    # 종목별 crop 적용
    crop = template_info["crop"]
    if crop != (0, 0, 0, 0):
        left = crop[0]
        right = img.size[0] + crop[2] if crop[2] < 0 else img.size[0]
        img = img.crop((left, 0, right, img.size[1]))
    
    draw = ImageDraw.Draw(img)
    
    width, height = img.size
    print(f"Template: {template_info['file']}, Size: {width}x{height}")
    
    # 폰트 설정
    font_options = [
        "C:/Windows/Fonts/GOTHICB.TTF",
        "C:/Windows/Fonts/ariblk.ttf",
        "C:/Windows/Fonts/segoeuib.ttf",
    ]
    
    price_font = None
    for font_path in font_options:
        try:
            price_font = ImageFont.truetype(font_path, 80)
            break
        except:
            continue
    
    if price_font is None:
        price_font = ImageFont.load_default()
    
    # 가격 텍스트
    price_text = format(price, ',') + " WON"
    
    # 텍스트 크기 계산
    price_bbox = draw.textbbox((0, 0), price_text, font=price_font)
    price_width = price_bbox[2] - price_bbox[0]
    price_height = price_bbox[3] - price_bbox[1]
    
    # 중앙 위치 계산
    x = (width - price_width) // 2
    y = (height - price_height) // 2 + 20
    
    # 그림자 효과
    draw.text((x + 2, y + 2), price_text, fill=(0, 0, 0), font=price_font)
    
    # 메인 텍스트 (흰색)
    draw.text((x, y), price_text, fill=(255, 255, 255), font=price_font)
    
    # 저장
    output_path = os.path.join(os.path.dirname(__file__), OUTPUT_PATH)
    img.save(output_path, "PNG")
    
    print(f"Price image created: {output_path}")
    return output_path


if __name__ == "__main__":
    # 삼성전자 테스트
    create_price_image("005930", 165000, True)
    
    # SK하이닉스 테스트
    create_price_image("000660", 841000, True)

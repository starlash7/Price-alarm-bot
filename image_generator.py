# -*- coding: utf-8 -*-
from PIL import Image, ImageDraw, ImageFont
import os

# 경로 설정
TEMPLATE_PATH = "template.png"
OUTPUT_PATH = "price_alert.png"


def create_price_image(stock_name, price, is_up):
    """
    템플릿 이미지에 가격만 오버레이
    """
    # 템플릿 이미지 열기
    template_path = os.path.join(os.path.dirname(__file__), TEMPLATE_PATH)
    img = Image.open(template_path).convert("RGB")
    
    # 흰색/연한 테두리 자르기 (더 많이)
    img = img.crop((5, 0, img.size[0] - 5, img.size[1]))
    
    draw = ImageDraw.Draw(img)
    
    width, height = img.size
    print(f"Template size (after crop): {width}x{height}")
    
    # 폰트 설정 (더 굵고 둥근 폰트)
    font_options = [
        "C:/Windows/Fonts/GOTHICB.TTF",    # Century Gothic Bold (굵고 둥근)
        "C:/Windows/Fonts/ariblk.ttf",     # Arial Black (매우 굵음)
        "C:/Windows/Fonts/segoeuib.ttf",   # Segoe UI Bold
    ]
    
    price_font = None
    for font_path in font_options:
        try:
            price_font = ImageFont.truetype(font_path, 80)
            print(f"Using font: {font_path}")
            break
        except Exception as e:
            print(f"Font not found: {font_path}")
            continue
    
    if price_font is None:
        price_font = ImageFont.load_default()
        print("Using default font")
    
    # 가격 텍스트
    price_text = format(price, ',') + " WON"
    
    # 텍스트 크기 계산
    price_bbox = draw.textbbox((0, 0), price_text, font=price_font)
    price_width = price_bbox[2] - price_bbox[0]
    price_height = price_bbox[3] - price_bbox[1]
    
    # 중앙 위치 계산
    x = (width - price_width) // 2
    y = (height - price_height) // 2 + 20  # 아래로 내림
    
    # 그림자 효과
    shadow_color = (0, 0, 0)
    draw.text((x + 2, y + 2), price_text, fill=shadow_color, font=price_font)
    
    # 메인 텍스트 (흰색)
    text_color = (255, 255, 255)
    draw.text((x, y), price_text, fill=text_color, font=price_font)
    
    # 저장
    output_path = os.path.join(os.path.dirname(__file__), OUTPUT_PATH)
    img.save(output_path, "PNG")
    
    print(f"Price image created: {output_path}")
    return output_path


if __name__ == "__main__":
    # 테스트
    path = create_price_image("Samsung", 165000, True)
    print(f"Test image: {path}")

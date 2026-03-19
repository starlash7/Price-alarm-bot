# -*- coding: utf-8 -*-
import os
from PIL import Image, ImageDraw, ImageFont

FONT_CANDIDATES = [
    "/System/Library/Fonts/Supplemental/Arial Black.ttf",
    "/System/Library/Fonts/Supplemental/Impact.ttf",
    "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
    "/System/Library/Fonts/Supplemental/Arial Rounded Bold.ttf",
    "/System/Library/Fonts/AppleSDGothicNeo.ttc",
    "/Library/Fonts/Arial Bold.ttf",
    "/System/Library/Fonts/Helvetica.ttc",
]

SYMBOL_FONT_CANDIDATES = [
    "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
    "/System/Library/Fonts/Supplemental/Arial Unicode.ttf",
    "/System/Library/Fonts/Supplemental/Arial.ttf",
    "/System/Library/Fonts/AppleSDGothicNeo.ttc",
    "/Library/Fonts/Arial Unicode.ttf",
]

DEFAULT_TEMPLATE = {
    "file": "templates/samsung.png",
    "price_style": "krw",
    "decimals": 0,
    "x_offset": 0,
    "y_offset": 0,
    "font_size": 108,
    "max_width_ratio": 0.48,
    "text_fill": (0, 0, 0),
    "stroke_fill": (0, 0, 0),
    "stroke_width": 0,
    "shadow_fill": (90, 90, 90),
    "shadow_offset": (4, 4),
    "bold_offsets": ((1, 0), (0, 1), (1, 1), (-1, 0), (0, -1), (-1, -1), (-1, 1), (1, -1)),
    "symbol_scale": 0.94,
    "symbol_gap": 10,
    "symbol_y_offset": 0,
}

TEMPLATES = {
    "005930": {"file": "templates/samsung.png", "price_style": "krw", "font_size": 88, "max_width_ratio": 0.40, "symbol_scale": 0.92, "symbol_gap": 3, "symbol_y_offset": 12},
    "000660": {"file": "templates/hynix.png", "price_style": "krw", "font_size": 84, "max_width_ratio": 0.40, "symbol_scale": 1.00, "symbol_gap": 2, "symbol_y_offset": 10},
    "035420": {"file": "templates/naver.png", "price_style": "krw", "font_size": 88, "max_width_ratio": 0.40, "symbol_scale": 0.92, "symbol_gap": 3, "symbol_y_offset": 12},
    "005380": {"file": "templates/hyundai.png", "price_style": "krw", "font_size": 88, "max_width_ratio": 0.40, "symbol_scale": 0.92, "symbol_gap": 3, "symbol_y_offset": 12},
    "KOSPI": {"file": "templates/kospi.png", "price_style": "index", "decimals": 2, "font_size": 96, "max_width_ratio": 0.44},
    "KOSDAQ": {"file": "templates/kosdaq.png", "price_style": "index", "decimals": 2, "font_size": 96, "max_width_ratio": 0.44},
    "SOL": {"file": "templates/sol.png", "price_style": "usd", "decimals": 2},
    "BNB": {"file": "templates/bnb.png", "price_style": "usd", "decimals": 2},
    "HYPE": {"file": "templates/hype.png", "price_style": "usd", "decimals": 2},
    "XRP": {"file": "templates/xrp.png", "price_style": "usd", "decimals": 2},
    "DOGE": {"file": "templates/doge.png", "price_style": "usd", "decimals": 4},
    "NASDAQ": {"file": "templates/nasdaq.png", "price_style": "index", "decimals": 2, "font_size": 92, "max_width_ratio": 0.42},
    "TSLA": {"file": "templates/tsla.png", "price_style": "usd", "decimals": 2},
    "NVDA": {"file": "templates/nvda.png", "price_style": "usd", "decimals": 2},
    "AAPL": {"file": "templates/aapl.png", "price_style": "usd", "decimals": 2},
}


def _load_font(size):
    for font_path in FONT_CANDIDATES:
        try:
            return ImageFont.truetype(font_path, size)
        except OSError:
            continue
    return ImageFont.load_default()


def _load_symbol_font(size):
    for font_path in SYMBOL_FONT_CANDIDATES:
        try:
            return ImageFont.truetype(font_path, size)
        except OSError:
            continue
    return _load_font(size)


def _fit_font(draw, text, start_size, max_width, stroke_width):
    size = start_size
    while size > 24:
        font = _load_font(size)
        bbox = draw.textbbox((0, 0), text, font=font, stroke_width=stroke_width)
        if (bbox[2] - bbox[0]) <= max_width:
            return font, bbox
        size -= 2

    font = _load_font(24)
    return font, draw.textbbox((0, 0), text, font=font, stroke_width=stroke_width)


def _fit_krw_fonts(draw, symbol_text, body_text, start_size, max_width, symbol_scale, symbol_gap):
    size = start_size
    while size > 24:
        body_font = _load_font(size)
        symbol_font = _load_symbol_font(max(24, int(size * symbol_scale)))
        symbol_bbox = draw.textbbox((0, 0), symbol_text, font=symbol_font)
        body_bbox = draw.textbbox((0, 0), body_text, font=body_font)
        symbol_width = symbol_bbox[2] - symbol_bbox[0]
        body_width = body_bbox[2] - body_bbox[0]
        total_width = symbol_width + symbol_gap + body_width
        if total_width <= max_width:
            return body_font, body_bbox, symbol_font, symbol_bbox, total_width
        size -= 2

    body_font = _load_font(24)
    symbol_font = _load_symbol_font(24)
    body_bbox = draw.textbbox((0, 0), body_text, font=body_font)
    symbol_bbox = draw.textbbox((0, 0), symbol_text, font=symbol_font)
    total_width = (symbol_bbox[2] - symbol_bbox[0]) + symbol_gap + (body_bbox[2] - body_bbox[0])
    return body_font, body_bbox, symbol_font, symbol_bbox, total_width


def _format_price(price, template_info, is_index=False):
    style = template_info.get("price_style", "krw")
    decimals = template_info.get("decimals", 2)

    if style == "index" or is_index:
        return {"prefix": "", "body": f"{price:,.{decimals}f}"}
    if style == "usd":
        return {"prefix": "", "body": f"${price:,.{decimals}f}"}
    return {"prefix": "\u20A9", "body": f"{int(price):,}"}


def create_price_image(stock_code, price, is_up, is_index=False):
    template_info = DEFAULT_TEMPLATE.copy()
    template_info.update(TEMPLATES.get(stock_code, {}))

    template_path = os.path.join(os.path.dirname(__file__), template_info["file"])
    img = Image.open(template_path).convert("RGB")
    draw = ImageDraw.Draw(img)

    width, height = img.size
    price_text = _format_price(price, template_info, is_index=is_index)
    max_width = int(width * template_info["max_width_ratio"])
    stroke_width = template_info.get("stroke_width", 0)
    if price_text["prefix"]:
        symbol_scale = template_info.get("symbol_scale", DEFAULT_TEMPLATE["symbol_scale"])
        symbol_gap = template_info.get("symbol_gap", DEFAULT_TEMPLATE["symbol_gap"])
        font, bbox, symbol_font, symbol_bbox, text_width = _fit_krw_fonts(
            draw,
            price_text["prefix"],
            price_text["body"],
            template_info["font_size"],
            max_width,
            symbol_scale,
            symbol_gap,
        )
        body_height = bbox[3] - bbox[1]
        symbol_height = symbol_bbox[3] - symbol_bbox[1]
        text_height = max(body_height, symbol_height)
    else:
        font, bbox = _fit_font(draw, price_text["body"], template_info["font_size"], max_width, stroke_width)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        symbol_font = None
        symbol_bbox = None

    x = (width - text_width) // 2 + template_info.get("x_offset", 0)
    y = (height - text_height) // 2 + template_info.get("y_offset", 0)

    x = max(0, min(x, width - text_width))
    y = max(0, min(y, height - text_height))

    shadow_offset = template_info.get("shadow_offset", (0, 0))
    bold_offsets = template_info.get("bold_offsets", ())
    if price_text["prefix"]:
        symbol_width = symbol_bbox[2] - symbol_bbox[0]
        symbol_gap = template_info.get("symbol_gap", DEFAULT_TEMPLATE["symbol_gap"])
        symbol_y_offset = template_info.get("symbol_y_offset", DEFAULT_TEMPLATE["symbol_y_offset"])
        body_height = bbox[3] - bbox[1]
        symbol_height = symbol_bbox[3] - symbol_bbox[1]
        symbol_y = y + max(0, (text_height - symbol_height) // 2) + symbol_y_offset
        body_x = x + symbol_width + symbol_gap
        body_y = y + max(0, (text_height - body_height) // 2)

        if shadow_offset != (0, 0):
            draw.text(
                (x + shadow_offset[0], symbol_y + shadow_offset[1]),
                price_text["prefix"],
                fill=template_info.get("shadow_fill", (90, 90, 90)),
                font=symbol_font,
            )
            draw.text(
                (body_x + shadow_offset[0], body_y + shadow_offset[1]),
                price_text["body"],
                fill=template_info.get("shadow_fill", (90, 90, 90)),
                font=font,
            )

        for offset_x, offset_y in bold_offsets:
            draw.text((x + offset_x, symbol_y + offset_y), price_text["prefix"], fill=template_info["text_fill"], font=symbol_font)
            draw.text((body_x + offset_x, body_y + offset_y), price_text["body"], fill=template_info["text_fill"], font=font)

        draw.text((x, symbol_y), price_text["prefix"], fill=template_info["text_fill"], font=symbol_font)
        draw.text((body_x, body_y), price_text["body"], fill=template_info["text_fill"], font=font)
    else:
        if shadow_offset != (0, 0):
            draw.text(
                (x + shadow_offset[0], y + shadow_offset[1]),
                price_text["body"],
                fill=template_info.get("shadow_fill", (90, 90, 90)),
                font=font,
                stroke_width=0,
            )

        for offset_x, offset_y in bold_offsets:
            draw.text((x + offset_x, y + offset_y), price_text["body"], fill=template_info["text_fill"], font=font, stroke_width=0)

        draw.text((x, y), price_text["body"], fill=template_info["text_fill"], font=font, stroke_width=stroke_width)

    output_path = os.path.join(os.path.dirname(__file__), f"price_alert_{stock_code}.png")
    img.save(output_path, "PNG")

    print(f"Price image created: {output_path}")
    return output_path


if __name__ == "__main__":
    create_price_image("005930", 208750, True)
    create_price_image("KOSPI", 5931.03, True, is_index=True)
    create_price_image("SOL", 181.52, True)
    create_price_image("AAPL", 246.37, True)

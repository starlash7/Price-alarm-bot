# -*- coding: utf-8 -*-
import asyncio
from telegram import Bot
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHANNEL_ID
from image_generator import create_price_image


async def send_photo_async(image_path, caption):
    try:
        bot = Bot(token=TELEGRAM_BOT_TOKEN)
        with open(image_path, 'rb') as photo:
            await bot.send_photo(chat_id=TELEGRAM_CHANNEL_ID, photo=photo, caption=caption)
        print("Image sent", flush=True)
        return True
    except Exception as e:
        print(f"Image failed: {e}", flush=True)
        return False


def send_photo(image_path, caption):
    return asyncio.run(send_photo_async(image_path, caption))


def send_price_alert(stock_code, korean_name, price, is_up, is_index=False):
    # 이모지: 📈 = \U0001F4C8, 📉 = \U0001F4C9
    if is_up:
        emoji = "\U0001F4C8"
    else:
        emoji = "\U0001F4C9"
    
    # 지수는 소수점, 주식은 WON
    if is_index:
        price_text = f"{price:,.2f}"
    else:
        price_text = format(int(price), ',') + " WON"
    
    caption = emoji + " " + korean_name + " " + price_text + " @cryptoPixy"
    
    # 종목별 이미지 생성
    image_path = create_price_image(stock_code, price, is_up, is_index=is_index)
    
    return send_photo(image_path, caption)


if __name__ == "__main__":
    # 삼성전자 테스트
    send_price_alert("005930", "\uc0bc\uc131\uc804\uc790", 165000, True)
    
    # SK하이닉스 테스트
    send_price_alert("000660", "SK \ud558\uc774\ub2c9\uc2a4", 845000, True)
    
    # KOSPI 테스트
    send_price_alert("KOSPI", "\ucf54\uc2a4\ud53c", 5221.25, True, is_index=True)

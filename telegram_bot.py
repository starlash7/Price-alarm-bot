# -*- coding: utf-8 -*-
import asyncio
from telegram import Bot
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHANNEL_ID
from image_generator import create_price_image


async def send_message_async(message):
    try:
        bot = Bot(token=TELEGRAM_BOT_TOKEN)
        await bot.send_message(chat_id=TELEGRAM_CHANNEL_ID, text=message)
        print("Message sent", flush=True)
        return True
    except Exception as e:
        print(f"Message failed: {e}", flush=True)
        return False


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


def send_message(message):
    return asyncio.run(send_message_async(message))


def send_photo(image_path, caption):
    return asyncio.run(send_photo_async(image_path, caption))


def send_price_alert(stock_name, price, is_up):
    # 이모지: 📈 = \U0001F4C8, 📉 = \U0001F4C9
    # 한글: 삼성전자 = \uc0bc\uc131\uc804\uc790
    if is_up:
        emoji = "\U0001F4C8"
    else:
        emoji = "\U0001F4C9"
    
    korean_name = "\uc0bc\uc131\uc804\uc790"  # 삼성전자
    caption = emoji + " " + korean_name + " " + format(price, ',') + " WON @cryptoPixy"
    
    image_path = create_price_image(stock_name, price, is_up)
    return send_photo(image_path, caption)


if __name__ == "__main__":
    send_price_alert("Samsung", 165000, True)

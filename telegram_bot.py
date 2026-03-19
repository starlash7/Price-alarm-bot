# -*- coding: utf-8 -*-
import asyncio
import html
from telegram import Bot
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHANNEL_ID
from image_generator import create_price_image


async def get_chat_info_async(chat_id):
    try:
        bot = Bot(token=TELEGRAM_BOT_TOKEN)
        chat = await bot.get_chat(chat_id)
        return {
            "ok": True,
            "chat_id": chat.id,
            "title": chat.title,
        }
    except Exception as e:
        return {
            "ok": False,
            "error_type": type(e).__name__,
            "error": str(e),
        }


def get_chat_info(chat_id):
    return asyncio.run(get_chat_info_async(chat_id))


async def send_photo_async(image_path, caption, chat_id=None):
    try:
        bot = Bot(token=TELEGRAM_BOT_TOKEN)
        target_chat_id = chat_id or TELEGRAM_CHANNEL_ID
        with open(image_path, 'rb') as photo:
            await bot.send_photo(chat_id=target_chat_id, photo=photo, caption=caption, parse_mode="HTML")
        print(f"Image sent to {target_chat_id}", flush=True)
        return True
    except Exception as e:
        print(f"Image failed: {e}", flush=True)
        return False


def send_photo(image_path, caption, chat_id=None):
    return asyncio.run(send_photo_async(image_path, caption, chat_id=chat_id))


def _format_caption_price(asset, price):
    if asset.get("price_style") == "usd":
        decimals = 4 if asset["code"] == "DOGE" else 2
        return f"${price:,.{decimals}f}"
    if asset.get("is_index"):
        return f"{price:,.2f}"
    return "\u20A9" + format(int(price), ",")


def send_price_caption(asset, price, is_up):
    """캡션만 생성 (이미지 생성 없음)"""
    emoji = "\U0001F4C8" if is_up else "\U0001F4C9"
    price_text = html.escape(_format_caption_price(asset, price))
    channel_text = html.escape(asset["telegram_channel"])
    return f"{emoji} <b>{price_text}</b> {channel_text}"


def send_close_caption(asset, price, is_up):
    emoji = "\U0001F4C8" if is_up else "\U0001F4C9"
    price_text = html.escape(_format_caption_price(asset, price))
    channel_text = html.escape(asset["telegram_channel"])
    return f"[CLOSE] {emoji} <b>{price_text}</b> {channel_text}"


def send_price_alert(asset, price, is_up, chat_id=None):
    """이미지 생성 + 전송 (단독 사용 시)"""
    caption = send_price_caption(asset, price, is_up)
    image_path = create_price_image(asset["code"], price, is_up, is_index=asset.get("is_index", False))
    return send_photo(image_path, caption, chat_id=chat_id)


if __name__ == "__main__":
    from config import ASSETS

    samples = {asset["code"]: asset for asset in ASSETS}
    send_price_alert(samples["005930"], 165000, True)
    send_price_alert(samples["000660"], 845000, True)
    send_price_alert(samples["KOSPI"], 5221.25, True)

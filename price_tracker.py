import time
from datetime import datetime
from stock_fetcher import get_current_price
from image_generator import create_price_image
from telegram_bot import send_photo, send_price_caption
from threads_bot import send_threads_with_image
from config import STOCKS

# 중복 호출 방지 간격 (초)
DEDUP_INTERVAL = 60


class PriceTracker:
    def __init__(self):
        # 종목별 마지막 가격 저장 (비교용)
        self.last_prices = {}
        # 종목별 마지막 알림 시간 (중복 방지)
        self.last_sent = {}

    def send_scheduled_alert(self, stock):
        """정해진 시간에 알림 전송"""
        # 주말(토=5, 일=6) 송출 안 함
        if datetime.now().weekday() >= 5:
            print(f"[{stock['name']}] Skipping weekend", flush=True)
            return

        code = stock["code"]
        name = stock["name"]
        korean_name = stock["korean_name"]
        is_index = stock.get("is_index", False)

        # 중복 호출 방지: 같은 종목이 짧은 시간 내에 다시 호출되면 무시
        now = time.time()
        last = self.last_sent.get(code, 0)
        if now - last < DEDUP_INTERVAL:
            print(f"[{name}] Skipping duplicate call (last sent {int(now - last)}s ago)", flush=True)
            return

        result = get_current_price(code, is_index=is_index)

        if result is None:
            print(f"[{name}] Price fetch failed", flush=True)
            return

        price = result["price"]
        change = result["change"]
        change_ratio = result["change_ratio"]
        is_up = result["is_up"]

        if is_index:
            print(f"[{name}] Price: {price:,.2f} ({'+' if is_up else '-'}{change_ratio}%)", flush=True)
        else:
            print(f"[{name}] Price: {price:,} ({'+' if is_up else '-'}{change_ratio}%)", flush=True)

        # 이미지 1회 생성
        image_path = create_price_image(code, price, is_up, is_index=is_index)

        # 텔레그램 전송
        caption = send_price_caption(code, korean_name, price, is_up, is_index=is_index)
        send_photo(image_path, caption)

        # Threads 전송
        send_threads_with_image(image_path, korean_name, price, is_up, is_index=is_index,
                                change=change, change_ratio=change_ratio)

        # 가격 및 전송 시간 저장
        self.last_prices[code] = price
        self.last_sent[code] = now


if __name__ == "__main__":
    from config import STOCKS
    tracker = PriceTracker()
    for stock in STOCKS:
        tracker.send_scheduled_alert(stock)

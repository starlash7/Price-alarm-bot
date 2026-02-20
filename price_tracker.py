import time
from stock_fetcher import get_current_price
from telegram_bot import send_price_alert
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

        current_price = get_current_price(code, is_index=is_index)

        if current_price is None:
            print(f"[{name}] Price fetch failed", flush=True)
            return

        if is_index:
            print(f"[{name}] Price: {current_price:,.2f}", flush=True)
        else:
            print(f"[{name}] Price: {current_price:,}", flush=True)

        # 이전 가격과 비교해서 상승/하락 결정
        last_price = self.last_prices.get(code)

        if last_price is None:
            is_up = True  # 첫 알림은 상승으로
        else:
            is_up = current_price >= last_price

        # 알림 전송
        send_price_alert(code, korean_name, current_price, is_up, is_index=is_index)

        # 가격 및 전송 시간 저장
        self.last_prices[code] = current_price
        self.last_sent[code] = now


if __name__ == "__main__":
    from config import STOCKS
    tracker = PriceTracker()
    for stock in STOCKS:
        tracker.send_scheduled_alert(stock)

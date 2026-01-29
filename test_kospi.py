# -*- coding: utf-8 -*-
"""
KOSPI 오늘가 테스트 전송 - IDE에서 Run으로 실행하면 됨
"""
import os

# 프록시 환경변수 제거 (API/텔레그램 직접 연결)
for key in ("HTTP_PROXY", "HTTPS_PROXY", "http_proxy", "https_proxy"):
    os.environ.pop(key, None)

from config import STOCKS
from stock_fetcher import get_current_price
from telegram_bot import send_price_alert


def main():
    kospi = STOCKS[0]  # KOSPI
    code = kospi["code"]
    name = kospi["name"]
    korean_name = kospi["korean_name"]

    price = get_current_price(code, is_index=True)

    if price is None:
        price = 5221.25  # API 실패 시 예시 가격
        print(f"[{name}] API failed, using sample: {price:,.2f}", flush=True)
    else:
        print(f"[{name}] Price: {price:,.2f}", flush=True)

    send_price_alert(code, korean_name, price, True, is_index=True)
    print("Done", flush=True)


if __name__ == "__main__":
    main()

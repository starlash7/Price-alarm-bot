import schedule
import time
from price_tracker import PriceTracker
from config import CHECK_INTERVAL, STOCK_NAME, PRICE_UNIT


def main():
    print(f"=== {STOCK_NAME} 가격 알림 봇 시작 ===", flush=True)
    print(f"알림 단위: {PRICE_UNIT:,}원", flush=True)
    print(f"체크 주기: {CHECK_INTERVAL}초", flush=True)
    print("=" * 35, flush=True)
    
    tracker = PriceTracker()
    
    # 시작 시 한 번 체크
    tracker.check_and_alert()
    
    # 주기적으로 체크
    schedule.every(CHECK_INTERVAL).seconds.do(tracker.check_and_alert)
    
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    main()

import schedule
import time
from price_tracker import PriceTracker
from config import CHECK_INTERVAL, STOCKS


def main():
    print("=== Price Alert Bot Started ===", flush=True)
    print(f"Stocks: {', '.join([s['name'] for s in STOCKS])}", flush=True)
    print(f"Check interval: {CHECK_INTERVAL}s", flush=True)
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

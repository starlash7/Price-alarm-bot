import schedule
import time
from price_tracker import PriceTracker
from config import STOCKS


def main():
    print("=== Price Alert Bot Started ===", flush=True)
    print("=" * 35, flush=True)
    
    tracker = PriceTracker()
    
    # 종목별 스케줄 등록
    for stock in STOCKS:
        name = stock["name"]
        code = stock["code"]
        times = stock["alert_times"]
        
        print(f"[{name}] Alert times: {', '.join(times)}", flush=True)
        
        for alert_time in times:
            schedule.every().day.at(alert_time).do(tracker.send_scheduled_alert, stock)
    
    print("=" * 35, flush=True)
    print("Waiting for scheduled times...", flush=True)
    
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    main()

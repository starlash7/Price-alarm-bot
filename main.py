import schedule
import time
import os
import sys
import signal
from price_tracker import PriceTracker
from config import STOCKS

LOCK_FILE = os.path.join(os.path.dirname(__file__), "bot.lock")


def _is_process_running(pid):
    """PID가 실제로 살아있는지 확인"""
    try:
        os.kill(pid, 0)
        return True
    except (OSError, ProcessLookupError):
        return False


def _acquire_lock():
    """단일 인스턴스 보장 (lock file)"""
    if os.path.exists(LOCK_FILE):
        with open(LOCK_FILE, "r") as f:
            old_pid = f.read().strip()
        if old_pid and old_pid.isdigit() and _is_process_running(int(old_pid)):
            print(f"Bot already running (PID {old_pid}). Exiting.", flush=True)
            sys.exit(1)
        else:
            print(f"Stale lock file found (PID {old_pid}). Removing.", flush=True)

    with open(LOCK_FILE, "w") as f:
        f.write(str(os.getpid()))


def _release_lock(*args):
    """종료 시 lock file 제거"""
    if os.path.exists(LOCK_FILE):
        os.remove(LOCK_FILE)
    sys.exit(0)


def main():
    _acquire_lock()
    signal.signal(signal.SIGTERM, _release_lock)
    signal.signal(signal.SIGINT, _release_lock)

    print("=== Price Alert Bot Started ===", flush=True)
    print(f"PID: {os.getpid()}", flush=True)
    print("=" * 35, flush=True)

    # 기존 스케줄 초기화 (재시작 시 중복 방지)
    schedule.clear()

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

    try:
        while True:
            schedule.run_pending()
            time.sleep(1)
    finally:
        _release_lock()


if __name__ == "__main__":
    main()

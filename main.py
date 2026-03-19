import os
import signal
import sys
import time

from config import ASSETS, CHECK_INTERVAL_SECONDS
from price_tracker import PriceTracker
from telegram_bot import get_chat_info

LOCK_FILE = os.path.join(os.path.dirname(__file__), "bot.lock")


def _is_process_running(pid):
    try:
        os.kill(pid, 0)
        return True
    except (OSError, ProcessLookupError):
        return False


def _acquire_lock():
    if os.path.exists(LOCK_FILE):
        with open(LOCK_FILE, "r") as handle:
            old_pid = handle.read().strip()
        if old_pid and old_pid.isdigit() and _is_process_running(int(old_pid)):
            print(f"Bot already running (PID {old_pid}). Exiting.", flush=True)
            sys.exit(1)
        print(f"Stale lock file found (PID {old_pid}). Removing.", flush=True)

    with open(LOCK_FILE, "w") as handle:
        handle.write(str(os.getpid()))


def _release_lock(*_args):
    if os.path.exists(LOCK_FILE):
        os.remove(LOCK_FILE)
    sys.exit(0)


def _filter_accessible_assets(assets):
    chat_checks = {}
    active_assets = []

    for asset in assets:
        chat_id = asset["telegram_channel"]
        if chat_id not in chat_checks:
            info = get_chat_info(chat_id)
            chat_checks[chat_id] = info
            if info["ok"]:
                print(f"[Channel OK] {chat_id} -> {info['title']} ({info['chat_id']})", flush=True)
            else:
                print(
                    f"[Channel ERR] {chat_id} -> {info['error_type']}: {info['error']}",
                    flush=True,
                )

        if chat_checks[chat_id]["ok"]:
            active_assets.append(asset)
        else:
            print(f"[{asset['name']}] Disabled due to inaccessible channel {chat_id}", flush=True)

    return active_assets


def main():
    _acquire_lock()
    signal.signal(signal.SIGTERM, _release_lock)
    signal.signal(signal.SIGINT, _release_lock)

    print("=== Price Alert Bot Started ===", flush=True)
    print(f"PID: {os.getpid()}", flush=True)
    print(f"Polling every {CHECK_INTERVAL_SECONDS}s", flush=True)
    print("=" * 35, flush=True)

    active_assets = _filter_accessible_assets(ASSETS)
    if not active_assets:
        print("No accessible Telegram channels. Exiting.", flush=True)
        return

    print("=" * 35, flush=True)

    for asset in active_assets:
        print(
            f"[{asset['name']}] Market: {asset['market']} | Step: {asset['alert_step']} | Channel: {asset['telegram_channel']}",
            flush=True,
        )

    print("=" * 35, flush=True)

    tracker = PriceTracker()

    try:
        while True:
            tracker.poll_assets(active_assets)
            time.sleep(CHECK_INTERVAL_SECONDS)
    finally:
        _release_lock()


if __name__ == "__main__":
    main()

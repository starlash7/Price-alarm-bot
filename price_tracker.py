import json
import os
import time
from datetime import datetime, time as dt_time
from decimal import Decimal
from zoneinfo import ZoneInfo

from image_generator import create_price_image
from stock_fetcher import get_current_price, get_crypto_prices
from telegram_bot import send_close_caption, send_photo, send_price_caption
from threads_bot import send_threads_with_image
from config import ASSETS, ENABLE_THREADS, THREADS_ACCESS_TOKEN

SEOUL_TZ = ZoneInfo("Asia/Seoul")
NEW_YORK_TZ = ZoneInfo("America/New_York")
CLOSE_ALERT_STATE_FILE = os.path.join(os.path.dirname(__file__), ".context", "close_alert_state.json")


class PriceTracker:
    def __init__(self):
        self.last_ranges = {}
        self.last_prices = {}
        self.close_alert_dates = self._load_close_alert_dates()

    def _load_close_alert_dates(self):
        try:
            with open(CLOSE_ALERT_STATE_FILE, "r") as handle:
                return json.load(handle)
        except FileNotFoundError:
            return {}
        except Exception as exc:
            print(f"[CLOSE] State load error: {exc}", flush=True)
            return {}

    def _save_close_alert_dates(self):
        try:
            os.makedirs(os.path.dirname(CLOSE_ALERT_STATE_FILE), exist_ok=True)
            with open(CLOSE_ALERT_STATE_FILE, "w") as handle:
                json.dump(self.close_alert_dates, handle)
        except Exception as exc:
            print(f"[CLOSE] State save error: {exc}", flush=True)

    def _is_market_open(self, asset, now_utc=None):
        market = asset["market"]
        if market == "CRYPTO":
            return True

        now_utc = now_utc or datetime.now(ZoneInfo("UTC"))

        if market == "KR":
            local_now = now_utc.astimezone(SEOUL_TZ)
            if local_now.weekday() >= 5:
                return False
            return dt_time(9, 0) <= local_now.time() <= dt_time(15, 30)

        if market == "US":
            local_now = now_utc.astimezone(NEW_YORK_TZ)
            if local_now.weekday() >= 5:
                return False
            return dt_time(9, 30) <= local_now.time() <= dt_time(16, 0)

        return False

    def _range_key(self, asset, price):
        return int(Decimal(str(price)) // Decimal(str(asset["alert_step"])))

    def _market_clock(self, asset, now_utc=None):
        now_utc = now_utc or datetime.now(ZoneInfo("UTC"))

        if asset["market"] == "KR":
            return now_utc.astimezone(SEOUL_TZ), dt_time(15, 30)
        if asset["market"] == "US":
            return now_utc.astimezone(NEW_YORK_TZ), dt_time(16, 0)
        return None, None

    def _send_alert(self, asset, result):
        price = result["price"]
        is_up = result["is_up"]
        image_path = create_price_image(asset["code"], price, is_up, is_index=asset.get("is_index", False))
        caption = send_price_caption(asset, price, is_up)
        sent = send_photo(image_path, caption, chat_id=asset["telegram_channel"])
        if not sent:
            print(f"[{asset['name']}] Telegram send failed for {asset['telegram_channel']}", flush=True)
            return False

        print(f"[{asset['name']}] Sent to {asset['telegram_channel']}", flush=True)

        if ENABLE_THREADS and THREADS_ACCESS_TOKEN:
            send_threads_with_image(
                image_path,
                asset["korean_name"],
                price,
                is_up,
                is_index=asset.get("is_index", False),
                change=result["change"],
                change_ratio=result["change_ratio"],
            )
        else:
            print(f"[{asset['name']}] Threads disabled", flush=True)

        return True

    def _send_close_alert(self, asset, result):
        price = result["price"]
        is_up = result["is_up"]
        image_path = create_price_image(asset["code"], price, is_up, is_index=asset.get("is_index", False))
        caption = send_close_caption(asset, price, is_up)
        sent = send_photo(image_path, caption, chat_id=asset["telegram_channel"])
        if not sent:
            print(f"[{asset['name']}] Close alert send failed for {asset['telegram_channel']}", flush=True)
            return False

        print(f"[{asset['name']}] Close sent to {asset['telegram_channel']}", flush=True)
        return True

    def _process_close_alert(self, asset, now_utc=None):
        if asset["market"] not in ("KR", "US"):
            return

        local_now, close_time = self._market_clock(asset, now_utc=now_utc)
        if local_now is None or local_now.weekday() >= 5 or local_now.time() <= close_time:
            return

        trading_date = local_now.date().isoformat()
        if self.close_alert_dates.get(asset["code"]) == trading_date:
            return

        result = get_current_price(asset)
        if result is None:
            print(f"[{asset['name']}] Close price fetch failed", flush=True)
            return

        if self._send_close_alert(asset, result):
            self.close_alert_dates[asset["code"]] = trading_date
            self._save_close_alert_dates()

    def _process_asset(self, asset, crypto_cache=None):
        if not self._is_market_open(asset):
            return

        result = get_current_price(asset, crypto_cache=crypto_cache)
        if result is None:
            print(f"[{asset['name']}] Price fetch failed", flush=True)
            return

        price = result["price"]
        range_key = self._range_key(asset, price)
        previous_range = self.last_ranges.get(asset["code"])

        if previous_range is None:
            self.last_ranges[asset["code"]] = range_key
            self.last_prices[asset["code"]] = price
            print(f"[{asset['name']}] Baseline set at {price}", flush=True)
            return

        self.last_prices[asset["code"]] = price

        if range_key == previous_range:
            return

        if self._send_alert(asset, result):
            self.last_ranges[asset["code"]] = range_key

    def poll_assets(self, assets):
        crypto_assets = [asset for asset in assets if asset["market"] == "CRYPTO"]
        crypto_cache = {}
        if crypto_assets:
            try:
                crypto_cache = get_crypto_prices(crypto_assets)
            except Exception as exc:
                print(f"[CRYPTO] Batch fetch error: {exc}", flush=True)

        for asset in assets:
            try:
                self._process_asset(asset, crypto_cache=crypto_cache)
            except Exception as exc:
                print(f"[{asset['name']}] Processing error: {exc}", flush=True)

        for asset in assets:
            try:
                self._process_close_alert(asset)
            except Exception as exc:
                print(f"[{asset['name']}] Close processing error: {exc}", flush=True)


if __name__ == "__main__":
    tracker = PriceTracker()
    tracker.poll_assets(ASSETS)

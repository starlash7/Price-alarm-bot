# -*- coding: utf-8 -*-
import csv
import io
import requests

NAVER_STOCK_URL = "https://polling.finance.naver.com/api/realtime/domestic/stock/{symbol}"
NAVER_INDEX_URL = "https://polling.finance.naver.com/api/realtime/domestic/index/{symbol}"
STOOQ_QUOTE_URL = "https://stooq.com/q/l/"
COINGECKO_SIMPLE_PRICE_URL = "https://api.coingecko.com/api/v3/simple/price"

DEFAULT_HEADERS = {
    "User-Agent": "Mozilla/5.0",
}


def _parse_naver_response(data, is_index):
    if not data.get("datas"):
        return None

    item = data["datas"][0]
    price_str = item.get("closePrice", "0")
    change_ratio = float(item.get("fluctuationsRatioRaw", item.get("fluctuationsRatio", "0")))
    change_str = item.get("compareToPreviousClosePrice", "0")
    direction = item.get("compareToPreviousPrice", {}).get("name", "")

    if is_index:
        price = float(price_str.replace(",", ""))
        change = float(change_str.replace(",", ""))
    else:
        price = int(price_str.replace(",", ""))
        change = int(change_str.replace(",", ""))

    return {
        "price": price,
        "change": change,
        "change_ratio": change_ratio,
        "is_up": direction != "FALLING",
    }


def _fetch_kr_price(asset):
    url_template = NAVER_INDEX_URL if asset.get("is_index") else NAVER_STOCK_URL
    response = requests.get(
        url_template.format(symbol=asset["source_symbol"]),
        headers=DEFAULT_HEADERS,
        timeout=10,
        proxies={"http": None, "https": None},
    )
    response.raise_for_status()
    return _parse_naver_response(response.json(), asset.get("is_index", False))


def _fetch_stooq_price(asset):
    response = requests.get(
        STOOQ_QUOTE_URL,
        params={"s": asset["source_symbol"].lower(), "i": "d"},
        headers=DEFAULT_HEADERS,
        timeout=10,
    )
    response.raise_for_status()

    rows = list(csv.reader(io.StringIO(response.text.strip())))
    if not rows:
        return None

    row = rows[0]
    if len(row) < 7 or row[3] == "N/D" or row[6] == "N/D":
        return None

    open_price = float(row[3])
    close_price = float(row[6])
    change = close_price - open_price
    change_ratio = (change / open_price * 100) if open_price else 0.0

    return {
        "price": close_price,
        "change": change,
        "change_ratio": change_ratio,
        "is_up": change >= 0,
    }


def get_crypto_prices(assets):
    ids = ",".join(asset["source_symbol"] for asset in assets)
    response = requests.get(
        COINGECKO_SIMPLE_PRICE_URL,
        params={"ids": ids, "vs_currencies": "usd", "include_24hr_change": "true"},
        headers=DEFAULT_HEADERS,
        timeout=10,
    )
    response.raise_for_status()
    data = response.json()

    result = {}
    for asset in assets:
        coin_data = data.get(asset["source_symbol"])
        if not coin_data:
            continue

        price = float(coin_data["usd"])
        change_ratio = float(coin_data.get("usd_24h_change", 0.0))
        previous_price = price / (1 + (change_ratio / 100)) if change_ratio != -100 else price
        change = price - previous_price

        result[asset["code"]] = {
            "price": price,
            "change": change,
            "change_ratio": change_ratio,
            "is_up": change >= 0,
        }

    return result


def get_current_price(asset, crypto_cache=None):
    try:
        market = asset["market"]
        if market == "KR":
            return _fetch_kr_price(asset)
        if market == "US":
            return _fetch_stooq_price(asset)
        if market == "CRYPTO":
            if crypto_cache is None:
                crypto_cache = get_crypto_prices([asset])
            return crypto_cache.get(asset["code"])
        raise ValueError(f"Unsupported market: {market}")
    except Exception as exc:
        print(f"[{asset['name']}] Price fetch error: {exc}", flush=True)
        return None


if __name__ == "__main__":
    from config import ASSETS

    crypto_assets = [asset for asset in ASSETS if asset["market"] == "CRYPTO"]
    crypto_cache = get_crypto_prices(crypto_assets)
    for asset in ASSETS:
        print(asset["code"], get_current_price(asset, crypto_cache=crypto_cache))

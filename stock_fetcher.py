# -*- coding: utf-8 -*-
import requests


def get_current_price(stock_code, is_index=False):
    """
    네이버 금융 실시간 API에서 주식/지수 가격 조회
    Returns: dict with price, change, change_ratio, is_up (or None on failure)
    """
    try:
        if is_index:
            url = f"https://polling.finance.naver.com/api/realtime/domestic/index/{stock_code}"
        else:
            url = f"https://polling.finance.naver.com/api/realtime/domestic/stock/{stock_code}"

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        # 프록시 미사용 (직접 연결)
        proxies = {"http": None, "https": None}

        response = requests.get(url, headers=headers, timeout=10, proxies=proxies)
        response.raise_for_status()

        data = response.json()

        if data.get("datas") and len(data["datas"]) > 0:
            item = data["datas"][0]
            price_str = item.get("closePrice", "0")
            change_ratio = float(item.get("fluctuationsRatioRaw", item.get("fluctuationsRatio", "0")))
            change_str = item.get("compareToPreviousClosePrice", "0")
            price_direction = item.get("compareToPreviousPrice", {}).get("name", "")

            if is_index:
                price = float(price_str.replace(",", ""))
                change = float(change_str.replace(",", ""))
            else:
                price = int(price_str.replace(",", ""))
                change = int(change_str.replace(",", ""))

            is_up = price_direction != "FALLING"

            return {
                "price": price,
                "change": change,
                "change_ratio": change_ratio,
                "is_up": is_up,
            }

        return None

    except Exception as e:
        print(f"Price fetch error: {e}", flush=True)
        return None


if __name__ == "__main__":
    # 테스트
    samsung = get_current_price("005930")
    hynix = get_current_price("000660")
    kospi = get_current_price("KOSPI", is_index=True)

    if samsung:
        s = samsung
        print(f"Samsung: {s['price']:,} WON ({'+' if s['is_up'] else '-'}{s['change_ratio']}%)")
    if hynix:
        h = hynix
        print(f"SK Hynix: {h['price']:,} WON ({'+' if h['is_up'] else '-'}{h['change_ratio']}%)")
    if kospi:
        k = kospi
        print(f"KOSPI: {k['price']:,.2f} ({'+' if k['is_up'] else '-'}{k['change_ratio']}%)")

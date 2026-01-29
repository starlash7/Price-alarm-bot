# -*- coding: utf-8 -*-
import requests


def get_current_price(stock_code):
    """
    네이버 금융 실시간 API에서 주식 가격 조회
    """
    try:
        url = f"https://polling.finance.naver.com/api/realtime/domestic/stock/{stock_code}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        if data.get("datas") and len(data["datas"]) > 0:
            price_str = data["datas"][0].get("closePrice", "0")
            price = int(price_str.replace(",", ""))
            return price
        
        return None
        
    except Exception as e:
        print(f"Price fetch error: {e}", flush=True)
        return None


def get_price_unit(price, unit):
    """
    가격이 속한 단위 구간 반환
    예: 54,300원, 5000원 단위 -> 50,000원
    """
    return (price // unit) * unit


if __name__ == "__main__":
    # 테스트
    samsung = get_current_price("005930")
    hynix = get_current_price("000660")
    
    print(f"Samsung: {samsung:,} WON" if samsung else "Samsung: Failed")
    print(f"SK Hynix: {hynix:,} WON" if hynix else "SK Hynix: Failed")

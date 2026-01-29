# -*- coding: utf-8 -*-
import requests


def get_current_price(stock_code, is_index=False):
    """
    네이버 금융 실시간 API에서 주식/지수 가격 조회
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
            price_str = data["datas"][0].get("closePrice", "0")
            
            if is_index:
                # 지수는 소수점 포함
                price = float(price_str.replace(",", ""))
            else:
                # 주식은 정수
                price = int(price_str.replace(",", ""))
            
            return price
        
        return None
        
    except Exception as e:
        print(f"Price fetch error: {e}", flush=True)
        return None


if __name__ == "__main__":
    # 테스트
    samsung = get_current_price("005930")
    hynix = get_current_price("000660")
    kospi = get_current_price("KOSPI", is_index=True)
    
    print(f"Samsung: {samsung:,} WON" if samsung else "Samsung: Failed")
    print(f"SK Hynix: {hynix:,} WON" if hynix else "SK Hynix: Failed")
    print(f"KOSPI: {kospi:,.2f}" if kospi else "KOSPI: Failed")

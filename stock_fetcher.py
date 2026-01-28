from pykrx import stock
from datetime import datetime, timedelta


def get_current_price(stock_code: str) -> int | None:
    """
    주식 현재가 조회
    장 운영 시간이 아닐 경우 최근 종가 반환
    """
    try:
        today = datetime.now().strftime("%Y%m%d")
        
        # 오늘 날짜로 시도
        df = stock.get_market_ohlcv(today, today, stock_code)
        
        if not df.empty:
            return int(df.iloc[-1]["종가"])
        
        # 오늘 데이터 없으면 최근 5일 중 마지막 거래일 조회
        start_date = (datetime.now() - timedelta(days=5)).strftime("%Y%m%d")
        df = stock.get_market_ohlcv(start_date, today, stock_code)
        
        if not df.empty:
            return int(df.iloc[-1]["종가"])
        
        return None
        
    except Exception as e:
        print(f"주식 가격 조회 실패: {e}")
        return None


def get_price_unit(price: int, unit: int) -> int:
    """
    가격이 속한 단위 구간 반환
    예: 54,300원, 5000원 단위 -> 50,000원
    """
    return (price // unit) * unit


if __name__ == "__main__":
    # 테스트
    price = get_current_price("005930")
    print(f"삼성전자 현재가: {price:,}원")
    print(f"5000원 단위: {get_price_unit(price, 5000):,}원")

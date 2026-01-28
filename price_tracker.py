from stock_fetcher import get_current_price, get_price_unit
from telegram_bot import send_price_alert
from config import STOCKS


class PriceTracker:
    def __init__(self):
        # 종목별 마지막 가격 단위 저장
        self.last_price_units = {}
    
    def check_and_alert(self):
        """모든 종목 가격 체크 후 단위 변경 시 알림"""
        for stock in STOCKS:
            self._check_stock(stock)
    
    def _check_stock(self, stock):
        """개별 종목 체크"""
        code = stock["code"]
        name = stock["name"]
        korean_name = stock["korean_name"]
        price_unit = stock["price_unit"]
        
        current_price = get_current_price(code)
        
        if current_price is None:
            print(f"[{name}] Price fetch failed", flush=True)
            return
        
        current_unit = get_price_unit(current_price, price_unit)
        
        print(f"[{name}] Price: {current_price:,} (Unit: {current_unit:,})", flush=True)
        
        # 첫 실행 시 초기화만
        if code not in self.last_price_units:
            self.last_price_units[code] = current_unit
            print(f"[{name}] Initialized at {current_unit:,} unit", flush=True)
            return
        
        last_unit = self.last_price_units[code]
        
        # 단위가 변경되었는지 확인
        if current_unit != last_unit:
            is_up = current_unit > last_unit
            
            # 알림 전송
            alert_price = current_unit if is_up else last_unit
            send_price_alert(code, korean_name, alert_price, is_up)
            
            self.last_price_units[code] = current_unit


if __name__ == "__main__":
    tracker = PriceTracker()
    tracker.check_and_alert()

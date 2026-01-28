from stock_fetcher import get_current_price, get_price_unit
from telegram_bot import send_price_alert
from config import STOCK_CODE, STOCK_NAME, PRICE_UNIT


class PriceTracker:
    def __init__(self):
        self.last_price_unit = None
    
    def check_and_alert(self) -> None:
        """가격 체크 후 단위 변경 시 알림"""
        current_price = get_current_price(STOCK_CODE)
        
        if current_price is None:
            print("가격 조회 실패", flush=True)
            return
        
        current_unit = get_price_unit(current_price, PRICE_UNIT)
        
        print(f"현재가: {current_price:,}원 (단위: {current_unit:,}원)", flush=True)
        
        # 첫 실행 시 초기화만
        if self.last_price_unit is None:
            self.last_price_unit = current_unit
            print(f"초기화 완료: {current_unit:,}원 단위에서 시작", flush=True)
            return
        
        # 단위가 변경되었는지 확인
        if current_unit != self.last_price_unit:
            is_up = current_unit > self.last_price_unit
            
            # 알림 전송
            alert_price = current_unit if is_up else self.last_price_unit
            send_price_alert(STOCK_NAME, alert_price, is_up)
            
            self.last_price_unit = current_unit


if __name__ == "__main__":
    # 테스트
    tracker = PriceTracker()
    tracker.check_and_alert()

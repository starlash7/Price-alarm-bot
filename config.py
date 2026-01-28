import os
from dotenv import load_dotenv

load_dotenv()

# 텔레그램 설정
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHANNEL_ID = os.getenv("TELEGRAM_CHANNEL_ID")

# 주식 설정 (여러 종목)
STOCKS = [
    {
        "code": "005930",
        "name": "Samsung",
        "korean_name": "\uc0bc\uc131\uc804\uc790",  # 삼성전자
        "price_unit": 5000,
    },
    {
        "code": "000660",
        "name": "SK Hynix",
        "korean_name": "SK \ud558\uc774\ub2c9\uc2a4",  # SK 하이닉스
        "price_unit": 5000,
    },
]

# 체크 주기 (초)
CHECK_INTERVAL = 60  # 1분마다 체크

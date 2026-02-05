import os
from dotenv import load_dotenv

load_dotenv()

# 텔레그램 설정
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHANNEL_ID = os.getenv("TELEGRAM_CHANNEL_ID")

# 주식 설정 (여러 종목)
STOCKS = [
    {
        "code": "KOSPI",
        "name": "KOSPI",
        "korean_name": "\ucf54\uc2a4\ud53c",  # 코스피
        "alert_times": ["09:00"],  # 오전 9시
        "is_index": True,
    },
    {
        "code": "005930",
        "name": "Samsung",
        "korean_name": "\uc0bc\uc131\uc804\uc790",  # 삼성전자
        "alert_times": ["12:00"],  # 오후 12시
        "is_index": False,
    },
    {
        "code": "000660",
        "name": "SK Hynix",
        "korean_name": "SK \ud558\uc774\ub2c9\uc2a4",  # SK 하이닉스
        "alert_times": ["15:00"],  # 오후 3시
        "is_index": False,
    },
]

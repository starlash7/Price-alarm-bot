import os
from dotenv import load_dotenv

load_dotenv()

# 텔레그램 설정
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHANNEL_ID = os.getenv("TELEGRAM_CHANNEL_ID")

# 주식 설정
STOCK_CODE = "005930"  # 삼성전자
STOCK_NAME = "삼성전자"

# 알림 설정
PRICE_UNIT = 5000  # 5,000원 단위로 알림

# 체크 주기 (초)
CHECK_INTERVAL = 60  # 1분마다 체크

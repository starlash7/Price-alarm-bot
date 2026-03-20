import os
from dotenv import load_dotenv

load_dotenv()

# Telegram settings
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHANNEL_ID = os.getenv("TELEGRAM_CHANNEL_ID")

# Threads settings
THREADS_ACCESS_TOKEN = os.getenv("THREADS_ACCESS_TOKEN")
ENABLE_THREADS = os.getenv("ENABLE_THREADS", "true").strip().lower() in ("1", "true", "yes", "on")

# Runtime settings
CHECK_INTERVAL_SECONDS = int(os.getenv("CHECK_INTERVAL_SECONDS", "60"))

CHANNELS = {
    "SAMSUNG": "@samsung_elec_price",
    "XRP": "@xrp_price_feed",
    "KRX": "@krx_price",
    "HYPE": "@hype_price",
    "DOGE": "@doge_price_feed",
    "SK_HYNIX": "@skhynix_price",
    "NASDAQ": "@nasdaq_price_feed",
    "TSLA": "@tsla_price",
    "NVDA": "@nvda_price",
    "AAPL": "@appl_price",
    "NAVER": "@naver_price",
    "HYUNDAI": "@hyundai_price_feed",
    "SOL": "@sol_price_feed",
    "BNB": "@bnb_price_feed",
}

ASSETS = [
    {
        "code": "KOSPI",
        "source_symbol": "KOSPI",
        "name": "KOSPI",
        "korean_name": "코스피",
        "market": "KR",
        "is_index": True,
        "alert_step": 100,
        "telegram_channel": CHANNELS["KRX"],
    },
    {
        "code": "KOSDAQ",
        "source_symbol": "KOSDAQ",
        "name": "KOSDAQ",
        "korean_name": "코스닥",
        "market": "KR",
        "is_index": True,
        "alert_step": 100,
        "telegram_channel": CHANNELS["KRX"],
    },
    {
        "code": "005930",
        "source_symbol": "005930",
        "name": "Samsung",
        "korean_name": "삼성전자",
        "market": "KR",
        "is_index": False,
        "alert_step": 5000,
        "telegram_channel": CHANNELS["SAMSUNG"],
    },
    {
        "code": "000660",
        "source_symbol": "000660",
        "name": "SK Hynix",
        "korean_name": "SK 하이닉스",
        "market": "KR",
        "is_index": False,
        "alert_step": 10000,
        "telegram_channel": CHANNELS["SK_HYNIX"],
    },
    {
        "code": "035420",
        "source_symbol": "035420",
        "name": "NAVER",
        "korean_name": "NAVER",
        "market": "KR",
        "is_index": False,
        "alert_step": 5000,
        "telegram_channel": CHANNELS["NAVER"],
    },
    {
        "code": "005380",
        "source_symbol": "005380",
        "name": "HYUNDAI",
        "korean_name": "현대차",
        "market": "KR",
        "is_index": False,
        "alert_step": 10000,
        "telegram_channel": CHANNELS["HYUNDAI"],
    },
    {
        "code": "NASDAQ",
        "source_symbol": "^NDQ",
        "name": "NASDAQ",
        "korean_name": "NASDAQ",
        "market": "US",
        "is_index": True,
        "alert_step": 500,
        "telegram_channel": CHANNELS["NASDAQ"],
        "price_style": "index",
    },
    {
        "code": "TSLA",
        "source_symbol": "TSLA.US",
        "name": "TSLA",
        "korean_name": "TSLA",
        "market": "US",
        "is_index": False,
        "alert_step": 10,
        "telegram_channel": CHANNELS["TSLA"],
        "price_style": "usd",
    },
    {
        "code": "NVDA",
        "source_symbol": "NVDA.US",
        "name": "NVDA",
        "korean_name": "NVDA",
        "market": "US",
        "is_index": False,
        "alert_step": 5,
        "telegram_channel": CHANNELS["NVDA"],
        "price_style": "usd",
    },
    {
        "code": "AAPL",
        "source_symbol": "AAPL.US",
        "name": "AAPL",
        "korean_name": "AAPL",
        "market": "US",
        "is_index": False,
        "alert_step": 5,
        "telegram_channel": CHANNELS["AAPL"],
        "price_style": "usd",
    },
    {
        "code": "SOL",
        "source_symbol": "solana",
        "name": "SOL",
        "korean_name": "SOL",
        "market": "CRYPTO",
        "is_index": False,
        "alert_step": 1,
        "telegram_channel": CHANNELS["SOL"],
        "price_style": "usd",
    },
    {
        "code": "BNB",
        "source_symbol": "binancecoin",
        "name": "BNB",
        "korean_name": "BNB",
        "market": "CRYPTO",
        "is_index": False,
        "alert_step": 25,
        "telegram_channel": CHANNELS["BNB"],
        "price_style": "usd",
    },
    {
        "code": "HYPE",
        "source_symbol": "hyperliquid",
        "name": "HYPE",
        "korean_name": "HYPE",
        "market": "CRYPTO",
        "is_index": False,
        "alert_step": 0.5,
        "telegram_channel": CHANNELS["HYPE"],
        "price_style": "usd",
    },
    {
        "code": "XRP",
        "source_symbol": "ripple",
        "name": "XRP",
        "korean_name": "XRP",
        "market": "CRYPTO",
        "is_index": False,
        "alert_step": 0.10,
        "telegram_channel": CHANNELS["XRP"],
        "price_style": "usd",
    },
    {
        "code": "DOGE",
        "source_symbol": "dogecoin",
        "name": "DOGE",
        "korean_name": "DOGE",
        "market": "CRYPTO",
        "is_index": False,
        "alert_step": 0.01,
        "telegram_channel": CHANNELS["DOGE"],
        "price_style": "usd",
    },
]

# Backward compatible alias
STOCKS = ASSETS

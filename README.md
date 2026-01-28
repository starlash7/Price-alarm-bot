# 삼성전자 주식 가격 알림 봇 📈

삼성전자 주식 가격이 5,000원 단위를 돌파/이탈할 때 텔레그램으로 알림을 보내는 봇입니다.

## 알림 예시

```
📈 삼성전자 55,000원 돌파
📉 삼성전자 50,000원 이탈
```

## 설치 방법

### 1. 의존성 설치

```bash
pip install -r requirements.txt
```

### 2. 텔레그램 봇 설정

1. [@BotFather](https://t.me/BotFather)에서 새 봇 생성
2. 봇 토큰 복사
3. 알림받을 채널 생성 후 봇을 관리자로 추가

### 3. 환경변수 설정

`.env.example`을 `.env`로 복사 후 값 입력:

```bash
cp .env.example .env
```

```
TELEGRAM_BOT_TOKEN=your_bot_token_here
TELEGRAM_CHANNEL_ID=@your_channel_name
```

### 4. 실행

```bash
python main.py
```

## 설정 변경

`config.py`에서 수정 가능:

- `STOCK_CODE`: 종목 코드 (기본: 005930 삼성전자)
- `PRICE_UNIT`: 알림 단위 (기본: 5000원)
- `CHECK_INTERVAL`: 체크 주기 (기본: 60초)

## 파일 구조

```
├── main.py           # 메인 실행 파일
├── config.py         # 설정
├── stock_fetcher.py  # 주식 가격 조회
├── telegram_bot.py   # 텔레그램 전송
├── price_tracker.py  # 가격 변동 감지
├── requirements.txt  # 의존성
└── .env              # 환경변수 (직접 생성)
```

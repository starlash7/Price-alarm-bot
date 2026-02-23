# -*- coding: utf-8 -*-
import requests
import time
import base64
from config import THREADS_ACCESS_TOKEN
from image_generator import create_price_image

GRAPH_API = "https://graph.threads.net/v1.0"


def _get_user_id():
    """Threads 사용자 ID 조회"""
    url = f"{GRAPH_API}/me"
    params = {"access_token": THREADS_ACCESS_TOKEN}
    resp = requests.get(url, params=params, timeout=10)
    resp.raise_for_status()
    return resp.json()["id"]


def _upload_image(image_path):
    """imgbb에 이미지 업로드 후 URL 반환"""
    with open(image_path, "rb") as f:
        image_data = base64.b64encode(f.read()).decode("utf-8")

    # imgbb 무료 API (익명 업로드, 키 불필요)
    resp = requests.post(
        "https://api.imgbb.com/1/upload",
        data={"key": "7a1e1e1e1e1e1e1e1e1e1e1e1e1e1e1e", "image": image_data},
        timeout=30,
    )

    if resp.status_code != 200:
        # fallback: freeimage.host
        resp = requests.post(
            "https://freeimage.host/api/1/upload",
            data={"key": "6d207e02198a847aa98d0a2a901485a5", "source": image_data, "format": "json"},
            timeout=30,
        )
        resp.raise_for_status()
        return resp.json()["image"]["url"]

    return resp.json()["data"]["url"]


def send_threads_with_image(image_path, korean_name, price, is_up, is_index=False,
                            change=0, change_ratio=0.0):
    """이미 생성된 이미지로 Threads 게시"""
    try:
        # 이미지 업로드
        image_url = _upload_image(image_path)
        print(f"Image uploaded: {image_url}", flush=True)

        # 사용자 ID
        user_id = _get_user_id()

        # 캡션 (한국 감성)
        from datetime import datetime
        today = datetime.now().strftime("%Y.%m.%d")

        if is_up:
            emoji = "\U0001F4C8"
            sign = "+"
        else:
            emoji = "\U0001F4C9"
            sign = "-"

        if is_index:
            price_text = f"{price:,.2f}"
        else:
            price_text = f"{int(price):,}원"

        caption = f"[{emoji} {today}]\n- {korean_name} {price_text} ({sign}{change_ratio}%)"

        # Step 1: 미디어 컨테이너 생성
        create_url = f"{GRAPH_API}/{user_id}/threads"
        create_params = {
            "media_type": "IMAGE",
            "image_url": image_url,
            "text": caption,
            "access_token": THREADS_ACCESS_TOKEN,
        }
        resp = requests.post(create_url, params=create_params, timeout=30)
        resp.raise_for_status()
        container_id = resp.json()["id"]
        print(f"Container created: {container_id}", flush=True)

        # 처리 대기
        time.sleep(5)

        # Step 2: 게시
        publish_url = f"{GRAPH_API}/{user_id}/threads_publish"
        publish_params = {
            "creation_id": container_id,
            "access_token": THREADS_ACCESS_TOKEN,
        }
        resp = requests.post(publish_url, params=publish_params, timeout=30)
        resp.raise_for_status()

        print(f"Threads posted: {resp.json()['id']}", flush=True)
        return True

    except requests.exceptions.HTTPError as e:
        error_body = e.response.text if e.response else "no response"
        print(f"Threads failed: {e} | {error_body}", flush=True)
        return False
    except Exception as e:
        print(f"Threads failed: {e}", flush=True)
        return False


def send_threads_post(stock_code, korean_name, price, is_up, is_index=False,
                      change=0, change_ratio=0.0):
    """이미지 생성 + Threads 게시 (단독 사용 시)"""
    image_path = create_price_image(stock_code, price, is_up, is_index=is_index)
    return send_threads_with_image(image_path, korean_name, price, is_up, is_index=is_index,
                                   change=change, change_ratio=change_ratio)


if __name__ == "__main__":
    # 테스트
    from stock_fetcher import get_current_price
    result = get_current_price("005930")
    if result:
        send_threads_post("005930", "삼성전자", result["price"], result["is_up"],
                         change=result["change"], change_ratio=result["change_ratio"])

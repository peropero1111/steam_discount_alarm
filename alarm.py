import json
import re
import time
from datetime import date, datetime
from pathlib import Path
from tkinter import Tk, messagebox
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

COUNTRY_CODE = "KR"
LANGUAGE = "koreana"
RUN_ONCE_PER_DAY = True
REQUEST_TIMEOUT_SECONDS = 15
REQUEST_RETRIES = 3
RETRY_DELAY_SECONDS = 10
POPUP_MODE = "always"

WATCHED_PRODUCTS = [
    {
        "name": "게임_이름",
        "url": "스팀_주소"
    },
]


BASE_DIR = Path(__file__).resolve().parent
LOG_FILE = BASE_DIR / "steam_sale_checker.log"
LAST_RUN_FILE = BASE_DIR / "last_run_date.txt"


def write_log(text: str) -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with LOG_FILE.open("a", encoding="utf-8") as f:
        f.write(f"[{now}]\n{text}\n\n")


def already_ran_today() -> bool:
    if not RUN_ONCE_PER_DAY:
        return False

    if not LAST_RUN_FILE.exists():
        return False

    last_run_date = LAST_RUN_FILE.read_text(encoding="utf-8").strip()
    return last_run_date == date.today().isoformat()


def mark_ran_today() -> None:
    if RUN_ONCE_PER_DAY:
        LAST_RUN_FILE.write_text(date.today().isoformat(), encoding="utf-8")


def extract_store_item_id(product: dict) -> dict:

    if "appid" in product:
        return {"appid": to_int(product["appid"], -1)}

    if "bundleid" in product:
        return {"bundleid": to_int(product["bundleid"], -1)}

    if "packageid" in product:
        return {"packageid": to_int(product["packageid"], -1)}

    url = str(product.get("url", "")).strip()

    patterns = [
        ("appid", r"/app/(\d+)"),
        ("bundleid", r"/bundle/(\d+)"),
        ("packageid", r"/sub/(\d+)"),
    ]

    for key, pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return {key: to_int(match.group(1), -1)}

    raise ValueError("appid, bundleid, packageid 또는 Steam URL이 필요합니다.")


def fetch_store_item(store_item_id: dict) -> dict | None:

    input_json = json.dumps(
        {
            "ids": [store_item_id],
            "context": {
                "country_code": COUNTRY_CODE,
                "language": LANGUAGE,
                "steam_realm": 1,
            },
            "data_request": {
                "include_basic_info": True,
                "include_all_purchase_options": True,
            },
        },
        separators=(",", ":"),
    )

    params = urlencode({"input_json": input_json})

    url = f"https://api.steampowered.com/IStoreBrowseService/GetItems/v1/?{params}"

    request = Request(
        url,
        headers={
            "User-Agent": "personal-steam-sale-checker/1.0"
        }
    )

    for attempt in range(1, REQUEST_RETRIES + 1):
        try:
            with urlopen(request, timeout=REQUEST_TIMEOUT_SECONDS) as response:
                raw_data = response.read().decode("utf-8")
            break

        except HTTPError:
            raise

        except URLError:
            if attempt == REQUEST_RETRIES:
                raise

            time.sleep(RETRY_DELAY_SECONDS)

    data = json.loads(raw_data)
    store_items = data.get("response", {}).get("store_items", [])

    if not store_items:
        return None

    store_item = store_items[0]

    if not store_item.get("success"):
        return None

    return store_item


def get_purchase_option(store_item: dict | None) -> dict | None:
    if not store_item:
        return None

    best_option = store_item.get("best_purchase_option")

    if best_option:
        return best_option

    purchase_options = store_item.get("purchase_options") or []

    if purchase_options:
        return purchase_options[0]

    return None


def to_int(value, default: int = 0) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def is_on_sale(purchase_option: dict | None) -> bool:
    if not purchase_option:
        return False

    discount_percent = to_int(purchase_option.get("discount_pct"))
    user_discount_percent = to_int(purchase_option.get("user_discount_pct"))

    if discount_percent > 0 or user_discount_percent > 0:
        return True

    if purchase_option.get("active_discounts") or purchase_option.get("user_active_discounts"):
        return True

    original_price = to_int(purchase_option.get("original_price_in_cents"))
    final_price = to_int(purchase_option.get("final_price_in_cents"))

    if original_price > final_price > 0:
        return True

    return False


def get_current_price_text(purchase_option: dict | None) -> str:
    if not purchase_option:
        return "가격 정보 없음"

    if purchase_option.get("formatted_final_price"):
        return str(purchase_option["formatted_final_price"])

    final_price = purchase_option.get("final_price_in_cents")

    if final_price is None:
        return "가격 정보 없음"

    return str(final_price)


def show_popup(title: str, message: str) -> None:
    root = Tk()
    root.withdraw()
    root.attributes("-topmost", True)

    messagebox.showinfo(title, message)

    root.destroy()


def main() -> None:
    if already_ran_today():
        write_log("오늘 이미 실행해서 종료합니다.")
        return

    sale_messages = []
    normal_messages = []
    error_messages = []

    for product in WATCHED_PRODUCTS:
        name = product.get("name", "이름 없는 Steam 제품")

        try:
            store_item_id = extract_store_item_id(product)
            store_item = fetch_store_item(store_item_id)
            purchase_option = get_purchase_option(store_item)
            current_price = get_current_price_text(purchase_option)

            if is_on_sale(purchase_option):
                sale_messages.append(f"{name}\n현재 할인 중입니다.\n현재가: {current_price}")
            else:
                normal_messages.append(f"{name}\n현재 할인 중이 아닙니다.\n현재가: {current_price}")

        except HTTPError as e:
            error_messages.append(f"{name}\nHTTP 오류: {e.code}")

        except URLError as e:
            error_messages.append(f"{name}\n네트워크 오류: {e.reason}")

        except Exception as e:
            error_messages.append(f"{name}\n오류: {e}")

    report_parts = []

    if sale_messages:
        report_parts.append("[할인 중]")
        report_parts.extend(sale_messages)

    if normal_messages:
        report_parts.append("[할인 아님]")
        report_parts.extend(normal_messages)

    if error_messages:
        report_parts.append("[오류]")
        report_parts.extend(error_messages)

    report = "\n\n".join(report_parts) if report_parts else "확인할 제품이 없습니다."
    write_log(report)

    if sale_messages or normal_messages:
        mark_ran_today()

    if sale_messages:
        popup_message = "\n\n".join(sale_messages)

        if error_messages:
            popup_message += "\n\n일부 제품 확인 중 오류가 있었습니다. 로그 파일을 확인하세요."

        show_popup("Steam 할인 알림", popup_message)

    elif POPUP_MODE == "always":
        popup_message = "현재 할인 중인 제품이 없습니다."

        if error_messages:
            popup_message += "\n\n일부 제품 확인 중 오류가 있었습니다. 로그 파일을 확인하세요."

        show_popup("Steam 할인 체크 결과", popup_message)


if __name__ == "__main__":
    main()


import json
import requests
from bs4 import BeautifulSoup

# 1. 讀取商品設定檔
def load_products():
    with open("products.json", "r", encoding="utf-8") as file:
        data = json.load(file)

    return data["products"]


# 2. 檢查單一商品網頁
def check_product(product):
    name = product["name"]
    url = product["url"]

    print(f"\n正在檢查：{name}")

    try:
        response = requests.get(
            url,
            headers={
                "User-Agent": "Mozilla/5.0"
            },
            timeout=15
        )

        print("HTTP 狀態碼：", response.status_code)

        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        title = soup.title.string if soup.title else "找不到網頁標題"

        print("網頁標題：", title.strip())
        print("網頁讀取成功！")

    except requests.RequestException as error:
        print("網頁讀取失敗：", error)


# 3. 主程式
def main():
    products = load_products()

    for product in products:
        if product.get("enabled", False):
            check_product(product)


# 4. 程式執行入口
if __name__ == "__main__":
    main()

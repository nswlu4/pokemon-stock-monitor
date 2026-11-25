import json
import os
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
    print(f"網址：{url}")

    try:
        response = requests.get(
            url,
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            },
            timeout=15
        )
        print("HTTP 狀態碼：", response.status_code)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        title = soup.title.string if soup.title else "找不到網頁標題"
        print("網頁標題：", title.strip())
        print("網頁讀取成功！")

        # 把整個網頁文字拿出來判斷
        page_text = soup.get_text()

        # PChome 常見的關鍵字
        in_stock_keywords = ["加入購物車", "立即購買", "加入購物車"]
        out_of_stock_keywords = ["已售完", "售完", "缺貨", "補貨中", "已售罄", "無庫存"]

        has_in_stock = any(k in page_text for k in in_stock_keywords)
        has_out_of_stock = any(k in page_text for k in out_of_stock_keywords)

        print(f"找到「有貨關鍵字」: {has_in_stock}")
        print(f"找到「缺貨關鍵字」: {has_out_of_stock}")

        if has_in_stock and not has_out_of_stock:
            status = "有貨 ✅"
        elif has_out_of_stock:
            status = "缺貨 ❌"
        else:
            status = "無法判斷 ⚠️ 找不到庫存關鍵字"

        print(f"判斷結果：{name} - {status}")
        return status

    except requests.RequestException as error:
        print("網頁讀取失敗：", error)
        return "讀取失敗"

# 3. 主程式
def main():
    products = load_products()
    for product in products:
        if product.get("enabled", False):
            status = check_product(product)
            # 有貨才發通知
            if "有貨" in status:
                print(f"🚨 補貨了！{product['name']} - {product['url']}")
                # 這裡之後接通知，見下面說明
            else:
                print("不發通知，繼續監控...")

# 4. 程式執行入口
if __name__ == "__main__":
    main()

import pip._vendor.requests 
import re

# ビットコイン価格をCoingeckoから取得する関数
def get_bitcoin_price_in_jpy():
    response = pip._vendor.requests.get("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=jpy")
    data = response.json()
    return data["bitcoin"]["jpy"]

# 特定のカフェチェーンのコーヒー価格を取得する関数
def get_coffee_price(url, regex_pattern):
    response = pip._vendor.requests.get(url)
    page_content = response.text
    price_match = re.search(regex_pattern, page_content)
    if price_match:
        return int(price_match.group(1))
    else:
        raise ValueError("価格が見つかりませんでした。")

# 特定のURLからコーヒー価格の平均をスクレイピング + 正規表現パターン
coffee_price_url = "https://jpmarket-conditions.com/2162/"
regex_pattern = r"\b(\d+)円\b"

# コーヒー価格を取得
coffee_price_jpy = get_coffee_price(coffee_price_url, regex_pattern)

# ビットコインの現在価格を取得してsats換算
bitcoin_price_jpy = get_bitcoin_price_in_jpy()
price_in_btc = coffee_price_jpy / bitcoin_price_jpy
price_in_sats = price_in_btc * 100000000
print(f"取得した価格: {price_in_sats}sats")

# HTMLファイルを更新
with open("index.html", "r+") as file:
    html_content = file.read()
    new_content = re.sub(r"Pay (\d+) sats", f"Pay {price_in_sats:.0f} sats", html_content)
    file.seek(0)
    file.write(new_content)
    file.truncate()

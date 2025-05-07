import requests

def get_top_tokens_with_scores():
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency": "usd",
        "order": "market_cap_desc",
        "per_page": 50,
        "page": 1,
        "sparkline": "false"
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        coins = response.json()
    except Exception as e:
        print("Ошибка при запросе CoinGecko:", e)
        return []

    tokens = []
    for coin in coins:
        try:
            name = coin["name"]
            symbol = coin["symbol"].upper()
            price = coin["current_price"]
            volume = coin["total_volume"]
            market_cap = coin["market_cap"]
            price_change = coin["price_change_percentage_24h"] or 0

            # вычисление "score"
            score = round((price_change * 1.5) + (volume / market_cap * 100), 2)
            token = {
                "name": name,
                "symbol": symbol,
                "price": price,
                "score": score,
                "change": price_change,
                "volume": volume,
                "market_cap": market_cap
            }

            if score >= 70:
                tokens.append(token)

        except Exception as e:
            print(f"Ошибка токена {coin.get('symbol', '?')}: {e}")

    return tokens

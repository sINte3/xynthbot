# xynth_scoring.py

import requests

LUNAR_API = "haef4br11i6lfgm49ewblvftcemacaulo7b2ynraq"

TOKENS = [
    {"symbol": "LDO"},
    {"symbol": "OP"},
    {"symbol": "ARB"},
    {"symbol": "PYTH"},
    {"symbol": "SUSHI"}
]

def get_top_tokens_with_scores():
    results = []
    for token in TOKENS:
        try:
            symbol = token['symbol']
            sentiment = get_sentiment_score(symbol)
            onchain = get_onchain_score(symbol)      # заглушка
            finance = get_finance_score(symbol)      # заглушка
            dev = get_dev_score(symbol)              # заглушка

            total_score = round(sentiment*0.5 + onchain*0.2 + finance*0.15 + dev*0.15, 1)

            results.append({
                "symbol": symbol,
                "score": total_score,
                "sentiment": sentiment,
                "onchain": onchain,
                "finance": finance,
                "dev": dev
            })
        except Exception as e:
            print(f"Ошибка для {symbol}: {e}")
    return sorted(results, key=lambda x: x['score'], reverse=True)

def get_sentiment_score(symbol):
    url = f"https://api.lunarcrush.com/v2?data=assets&symbol={symbol}&key={LUNAR_API}"
    response = requests.get(url)
    data = response.json()

    # Проверка, что API вернул данные
    if "data" in data and len(data["data"]) > 0:
        alt_rank = data["data"][0]["alt_rank"]
        galaxy_score = data["data"][0]["galaxy_score"]
        score = max(100 - alt_rank, 0) * 0.4 + galaxy_score * 0.6  # Взвешенная формула
        return round(score, 1)
    else:
        return 50  # если нет данных — нейтральный балл

# заглушки:
def get_onchain_score(symbol): return 60 + hash(symbol[::-1]) % 30
def get_finance_score(symbol): return 55 + len(symbol) % 25
def get_dev_score(symbol): return 65 + sum(ord(c) for c in symbol) % 15

if __name__ == "__main__":
    tokens = get_top_tokens_with_scores()
    for token in tokens:
        print(token)


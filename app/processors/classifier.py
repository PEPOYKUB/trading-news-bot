from app.schemas import NewsItem
def classify(item: NewsItem) -> NewsItem:
    text = f"{item.title} {item.raw_text}".lower()
    markets = []
    groups = {"Forex": ["fed", "ecb", "boj", "forex", "usd", "eur", "gbp", "jpy"], "Crypto": ["bitcoin", "btc", "ethereum", "crypto", "etf", "exchange"], "Gold": ["gold", "xau"], "Commodities": ["oil", "opec", "gas", "commodity", "supply"], "Stocks": ["stock", "earnings", "guidance", "m&a", "shares"], "Indices": ["nasdaq", "s&p", "dow", "index"], "Macro": ["cpi", "ppi", "nfp", "gdp", "pmi", "inflation", "employment"], "Central Bank": ["fed", "fomc", "ecb", "boj", "interest rate"], "Geopolitics": ["war", "geopolitical", "sanction"]}
    for market, words in groups.items():
        if any(w in text for w in words): markets.append(market)
    item.market = markets or ["Macro"]
    return item

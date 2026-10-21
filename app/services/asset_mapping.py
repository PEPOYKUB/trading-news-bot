MAPPING = {
    "fed": ["USD", "XAUUSD", "US Indices"], "fomc": ["USD", "XAUUSD", "SPX500", "NAS100"],
    "ecb": ["EUR", "European Indices"], "boj": ["JPY", "USDJPY"], "opec": ["USOIL", "CAD", "Inflation"],
    "bitcoin etf": ["BTCUSD"], "bitcoin": ["BTCUSD"], "btc": ["BTCUSD"], "ethereum": ["ETHUSD"],
    "cpi": ["USD", "XAUUSD", "SPX500", "NAS100"], "nfp": ["USD", "XAUUSD", "US Indices"],
    "oil": ["USOIL", "CAD"], "gold": ["XAUUSD"], "nasdaq": ["NAS100"], "s&p": ["SPX500"],
}
def detect_assets(text: str) -> list[str]:
    lowered = text.lower(); found = []
    for key, assets in MAPPING.items():
        if key in lowered:
            for asset in assets:
                if asset not in found: found.append(asset)
    return found

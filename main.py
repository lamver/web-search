import random
import time
from fastapi import FastAPI, Query
from duckduckgo_search import DDGS

app = FastAPI(title="SaaS Search API")

# Список прокси прямо в коде
# Формат: http://user:pass@host:port или http://host:port
PROXIES = [
    "socks5://C1La2C:C6QAtH@213.139.223.115:9875",
]

@app.get("/search")
def search_internet(q: str, limit: int = 5):
    # Копируем список, чтобы можно было удалять плохие прокси из попыток
    available_proxies = PROXIES.copy()
    max_retries = len(available_proxies) if available_proxies else 1
    
    for attempt in range(max_retries):
        # Выбираем случайный прокси
        proxy = random.choice(available_proxies) if available_proxies else None
        
        try:
            with DDGS(proxy=proxy, timeout=15) as ddgs:
                results = list(ddgs.text(q, max_results=limit))
                if results:
                    return {"status": "success", "proxy": proxy, "results": results}
                
                # Если пустой список — возможно, тоже бан или капча
                raise Exception("Empty results (possible soft ban)")

        except Exception as e:
            print(f"Attempt {attempt+1} failed with proxy {proxy}: {e}")
            # Удаляем плохой прокси из списка попыток для этого запроса
            if proxy in available_proxies:
                available_proxies.remove(proxy)
            # Небольшая пауза перед следующей попыткой
            time.sleep(1)
            continue

    return {"status": "error", "message": "All proxies failed or blocked"}
import random
from fastapi import FastAPI, Query
from duckduckgo_search import DDGS

app = FastAPI(title="SaaS Search API")

# Список прокси прямо в коде
# Формат: http://user:pass@host:port или http://host:port
PROXIES = [
    "socks5://C1La2C:C6QAtH@213.139.223.115:9875",
]

@app.get("/search")
def search_internet(
    q: str = Query(..., description="Запрос"),
    limit: int = Query(5, description="Лимит результатов")
):
    # Выбираем случайный прокси, если список не пуст
    proxy = random.choice(PROXIES) if PROXIES else None
    
    results = []
    try:
        # Передаем прокси в DDGS
        with DDGS(proxy=proxy, timeout=20) as ddgs:
            search_results = ddgs.text(q, max_results=limit, region='wt-wt')
            for r in search_results:
                results.append({
                    "title": r['title'],
                    "url": r['href'],
                    "snippet": r['body']
                })
        
        return {
            "status": "success",
            "proxy_used": proxy, 
            "count": len(results),
            "results": results
        }
        
    except Exception as e:
        # Если прокси отвалился, вернем ошибку, чтобы знать какой именно
        return {"status": "error", "proxy_attempted": proxy, "message": str(e)}
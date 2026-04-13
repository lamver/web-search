from fastapi import FastAPI, Query
from duckduckgo_search import DDGS
import trafilatura

app = FastAPI(title="SaaS Search Engine API")

@app.get("/search")
def search_internet(q: str = Query(..., description="Поисковый запрос")):
    results = []
    
    # 1. Ищем ссылки через DuckDuckGo (бесплатно)
    with DDGS() as ddgs:
        search_results = ddgs.text(q, max_results=3)
        for r in search_results:
            results.append({
                "title": r['title'],
                "url": r['href'],
                "snippet": r['body']
            })
    
    return {"query": q, "results": results}

@app.get("/extract")
def extract_text(url: str = Query(..., description="URL статьи")):
    # 2. Извлекаем чистый текст из статьи (без рекламы и меню)
    downloaded = trafilatura.fetch_url(url)
    content = trafilatura.extract(downloaded)
    
    return {"url": url, "content": content[:2000]} # Возвращаем первые 2000 символов

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

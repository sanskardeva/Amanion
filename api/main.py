from fastapi import FastAPI
from scraper.scraper import scrape_macs_newegg

app = FastAPI()

@app.get("/newegg-macs")
def get_newegg(limit: int = 5):
    try:
        products = scrape_macs_newegg(limit=limit)
        return {"count": len(products), "results": products}
    except Exception as e:
        return {"count": 0, "results": [{"error": str(e)}]}

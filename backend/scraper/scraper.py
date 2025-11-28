# scraper.py
import asyncio
import json
from crawl4ai import AsyncWebCrawler
from crawl4ai.extraction_strategy import JsonCssExtractionStrategy
from crawl4ai.async_configs import CrawlerRunConfig

SEARCH_SCHEMA = {
    "name": "AmazonSearch",
    "baseSelector": ".s-main-slot [data-component-type='s-search-result']",
    "fields": [
        {
            "name": "link",
            "selector": ".a-link-normal.s-no-outline",
            "type": "attribute",
            "attribute": "href",
            "multiple": False,
        }
    ],
}

PRODUCT_SCHEMA = {
    "name": "AmazonProduct",
    "baseSelector": "body",
    "fields": [
        {"name": "title", "selector": "#productTitle", "type": "text"},
        {"name": "price", "selector": ".a-price .a-offscreen", "type": "text"},
        {"name": "brand", "selector": "tr.po-brand .po-break-word", "type": "text"},
        {"name": "screen_size", "selector": "tr.po-display\\.size .po-break-word", "type": "text"},
        {"name": "ram_memory_installed_size", "selector": "tr.po-ram_memory\\.installed_size .po-break-word", "type": "text"},
        # add more fields as you like
    ],
}

BASE_URL = "https://www.amazon.com"

async def scrape_amazon(search_term: str, max_products: int = 10) -> list[dict]:
    """Return a list of product dicts for an Amazon search term."""
    async with AsyncWebCrawler() as crawler:
        # 1) search page → get product links
        search_strategy = JsonCssExtractionStrategy(schema=SEARCH_SCHEMA)
        search_config = CrawlerRunConfig(extraction_strategy=search_strategy)

        search_q = search_term.replace(" ", "+")
        search_result = await crawler.arun(
            url=f"{BASE_URL}/s?k={search_q}",
            config=search_config,
        )

        search_data = json.loads(search_result.extracted_content)
        links = [item["link"] for item in search_data][:max_products]

        # 2) product pages → get details
        product_strategy = JsonCssExtractionStrategy(schema=PRODUCT_SCHEMA)
        product_config = CrawlerRunConfig(extraction_strategy=product_strategy)

        products: list[dict] = []
        for link in links:
            result = await crawler.arun(
                url=f"{BASE_URL}{link}",
                config=product_config,
            )
            data = json.loads(result.extracted_content)
            # extraction may return a list; normalize to list of dicts
            if isinstance(data, list):
                products.extend(data)
            else:
                products.append(data)

        return products

# optional manual test:
if __name__ == "__main__":
    products = asyncio.run(scrape_amazon("dell laptop", max_products=5))
    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(products, f, indent=2, ensure_ascii=False)

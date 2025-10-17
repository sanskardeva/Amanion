import asyncio
from crawl4ai import AsyncWebCrawler
from crawl4ai.extraction_strategy import JsonCssExtractionStrategy
from crawl4ai.async_configs import CrawlerRunConfig
import json

async def main():
    schema = {
        "name": "AmazonProduct",
        "baseSelector": "body",
        "fields": [
            {"name": "title", "selector": "#productTitle", "type": "text"},
            {"name": "brand", "selector": "#tr.po-brand", "type": "text"},
        ],
    }

    extraction = JsonCssExtractionStrategy(schema=schema)
    config = CrawlerRunConfig(extraction_strategy=extraction)

    # Create an instance of AsyncWebCrawler
    async with AsyncWebCrawler() as crawler:
        # Run the crawler on a URL
        result = await crawler.arun(url="https://www.amazon.com/Apple-2024-MacBook-Laptop-10%E2%80%91core/dp/B0DLHBYRPS", config=config)

        data = json.loads(result.extracted_content)

        # Print the extracted content
        with open("product_data.json", "w") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

# Run the async main function
asyncio.run(main())

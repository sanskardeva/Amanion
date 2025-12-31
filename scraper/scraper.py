import asyncio
from crawl4ai import AsyncWebCrawler
from crawl4ai.extraction_strategy import JsonCssExtractionStrategy
from crawl4ai.async_configs import CrawlerRunConfig
import json

async def main():
    schema = {
        "name": "AmazonProduct",
        "baseSelector": ".s-main-slot [data-component-type='s-search-result']",
        "fields": [
            {"name": "link", "selector": ".s-search-results .a-link-normal.s-no-outline", "type": "attribute", "attribute": "href", "multiple": True},
            # {"name": "title", "selector": "#productTitle", "type": "text"},
            # {"name": "reviews", "selector": "#acrPopover .a-icon-alt", "type": "text"},
            # {"name": "price", "selector": ".aok-offscreen", "type": "text"},
            # {"name": "brand", "selector": "tr.po-brand .po-break-word", "type": "text"},
            # {"name": "model_name", "selector": "tr.po-model_name .po-break-word", "type": "text"},
            # {"name": "screen_size", "selector": "tr.po-display\\.size .po-break-word", "type": "text"},
            # {"name": "color", "selector": "tr.po-color .po-break-word", "type": "text"},
            # {"name": "hard_disk_size", "selector": "tr.po-hard_disk\\.size .po-break-word", "type": "text"},
            # {"name": "cpu_model", "selector": "tr.po-cpu_model\\.family .po-break-word", "type": "text"},
            # {"name": "ram_memory_installed_size", "selector": "tr.po-ram_memory\\.installed_size .po-break-word", "type": "text"},
            # {"name": "operating_system", "selector": "tr.po-operating_system .po-break-word", "type": "text"},
            # {"name": "special_feature", "selector": "tr.po-special_feature .po-break-word", "type": "text"},
            # {"name": "graphics_card_description", "selector": "tr.po-graphics_description .po-break-word", "type": "text"},
        ],
    }

    base_url = "https://www.amazon.com"

    product_schema = {
        "name": "AmazonProduct",
        "baseSelector": "html",
        "fields": [
            {"name": "url", "selector": "link[rel='canonical']", "type": "attribute", "attribute": "href"},
            {"name": "image_url", "selector": "#landingImage", "type": "attribute", "attribute": "src"},
            {"name": "title", "selector": "#productTitle", "type": "text"},
            {"name": "reviews", "selector": "#acrPopover .a-icon-alt", "type": "text"},
            {"name": "price", "selector": ".a-price .a-offscreen", "type": "text"},
            {"name": "brand", "selector": "tr.po-brand .po-break-word", "type": "text"},
            {"name": "model_name", "selector": "tr.po-model_name .po-break-word", "type": "text"},
            {"name": "screen_size", "selector": "tr.po-display\\.size .po-break-word", "type": "text"},
            {"name": "color", "selector": "tr.po-color .po-break-word", "type": "text"},
            {"name": "hard_disk_size", "selector": "tr.po-hard_disk\\.size .po-break-word", "type": "text"},
            {"name": "cpu_model", "selector": "tr.po-cpu_model\\.family .po-break-word", "type": "text"},
            {"name": "ram_memory_installed_size", "selector": "tr.po-ram_memory\\.installed_size .po-break-word", "type": "text"},
            {"name": "operating_system", "selector": "tr.po-operating_system .po-break-word", "type": "text"},
            {"name": "special_feature", "selector": "tr.po-special_feature .po-break-word", "type": "text"},
            {"name": "graphics_card_description", "selector": "tr.po-graphics_description .po-break-word", "type": "text"},
        ],
    }


    # Create an instance of AsyncWebCrawler
    async with AsyncWebCrawler() as crawler:
        # Run the crawler on a URL
        search_term = "kitchen blenders"
        search_tern = search_term.replace(" ", "+")

        extraction = JsonCssExtractionStrategy(schema=schema)
        config = CrawlerRunConfig(extraction_strategy=extraction)

        result = await crawler.arun(url=f"https://www.amazon.com/s?k={search_term}", config=config)
        data = json.loads(result.extracted_content)
        with open("product_data.json", "w") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        with open("product_data.json", "r") as f:
            link_data = json.load(f)

        links = [item["link"] for item in link_data]

        products = []

        p_extraction = JsonCssExtractionStrategy(schema=product_schema)
        p_config = CrawlerRunConfig(extraction_strategy=p_extraction)

        for link in links:
            result = await crawler.arun(url=f"{base_url}{link}", config=p_config)
            p_data = json.loads(result.extracted_content)

            
            products.extend(p_data)
            # elif isinstance(p_data, list):
            #     for item in p_data:
            #         if isinstance(item, list):  # flatten nested lists
            #             products.extend(item)
            #         else:
            #             products.append(item)

        # write all products once
        with open("data.json", "w") as f:
            json.dump(products, f, indent=2, ensure_ascii=False)
                

# Run the async main function
asyncio.run(main())

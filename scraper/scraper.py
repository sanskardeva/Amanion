from playwright.sync_api import sync_playwright

def scrape_macs_newegg(limit=5):
    url = "https://www.newegg.com/p/pl?d=macbook"
    entries = []
    results = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # headless=False if you want to see the browser
        page = browser.new_page()
        page.goto(url)
        page.wait_for_selector(".item-cell")  # wait until products load

        items = page.query_selector_all(".item-cell")
        for item in items[:limit]:
            title = item.query_selector(".item-title").inner_text().strip()
            price = item.query_selector(".price-current").inner_text().strip()
            features = item.query_selector(".item-features").inner_text().strip()
            link = item.query_selector(".item-title").get_attribute("href")
            results.append({"title": title, "price": price, "features": features, "link": link})

        browser.close()
    return results

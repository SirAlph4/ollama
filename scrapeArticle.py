from playwright.async_api import async_playwright
import random
import asyncio
from playwright_stealth import stealth_async
import os
from xata.client import XataClient
from dotenv import load_dotenv
load_dotenv()

user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:95.0) Gecko/20100101 Firefox/95.0',
        'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:90.0) Gecko/20100101 Firefox/90.0',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:98.0) Gecko/20100101 Firefox/98.0',
        'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:100.0) Gecko/20100101 Firefox/100.0',
        'Mozilla/5.0 (X11; Linux x86_64; rv:93.0) Gecko/20100101 Firefox/93.0',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:96.0) Gecko/20100101 Firefox/96.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:94.0) Gecko/20100101 Firefox/94.0',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:99.0) Gecko/20100101 Firefox/99.0',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:101.0) Gecko/20100101 Firefox/101.0',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:103.0) Gecko/20100101 Firefox/103.0',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:104.0) Gecko/20100101 Firefox/104.0',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:105.0) Gecko/20100101 Firefox/105.0',

    ]

async def start_scraping(i):
    print(i)
    client = XataClient(db_url=os.environ.get('REDACTED_DB_URL'), api_key=os.environ.get('XATA_API_KEY'))
    async with async_playwright() as p:
        query_params = {
                "filter": {
                    "ID": i
                }
            }

        result = client.data().query("Urls", query_params)
        url = result["records"][0]["url"]
        browser = await p.firefox.launch(headless=True)
        context = await browser.new_context(
            viewport={'width': 600, 'height': 480}, 
            user_agent=random.choice(user_agents)
        )

        page = await context.new_page()
        await stealth_async(page)
        # Start scraping the main page
        await scrape_pages(page, url, i)
        await browser.close()
    


async def scrape_pages(page, url, i):
    await page.goto(url)  # Set timeout to 30 seconds
    await random_sleep(1, 3)

    headline = await page.text_content('h1.page-title')
    categories = await page.locator('li.meta-categories a').all_text_contents()
    timestamp = await page.get_attribute('li.meta-date time', 'datetime')
    author_name = await page.text_content('li.meta-author span[itemprop="name"]')

    # Extract article body, excluding unwanted sections
    text_body = page.locator('div.ct-container').nth(2)
    paragraphs = await text_body.locator('p').all_text_contents()
    article_text = ' '.join(paragraphs[:-2])  # Removing the last 2 paragraphs if necessary
    if "Sign up for our weekly email to stay on top of the latest news and insights! " in article_text[:100]:
        article_text = article_text[77:]
    client = XataClient(db_url=os.environ.get('REDACTED_DB_URL'), api_key=os.environ.get('XATA_API_KEY'))

    client.records().insert("Articles",{
                    "article_text": article_text,
                    "author_name": author_name,
                    "categories": categories,
                    "headline": headline,
                    "timestamp": timestamp, 
                    "url": url,
                    "ID": i,
                })


async def random_sleep( min_seconds, max_seconds):
    await asyncio.sleep(random.uniform(min_seconds, max_seconds))

if __name__ == "__main__":
    for i in range(1000000, 1005971):
        asyncio.run(start_scraping(i))

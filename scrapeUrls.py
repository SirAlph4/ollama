from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeoutError
import random
import asyncio
import json
from playwright_stealth import stealth_async
from pageUrls import pageUrls
import pandas as pd

class TheBrakeReportScraper:
    def __init__(self):
        self.user_agents = [
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
    async def start_scraping(self):
        url = "https://asia.nikkei.com/Business/Tech"
        try:
            df = pd.read_json('nikkei.json')
        except FileNotFoundError:
            df = pd.DataFrame()
        except Exception as e:
            df = pd.DataFrame()
            print(e)   
        async with async_playwright() as p:
            browser = await p.firefox.launch(headless=False)
            context = await browser.new_context(
                viewport={'width': 600, 'height': 480}, 
                user_agent=random.choice(self.user_agents)
            )

            page = await context.new_page()
            await stealth_async(page)
            # Start scraping the main page
            await self.scrape_pages(page, url ,df)
            print(url)
            await browser.close()
        


    async def scrape_pages(self, page, url, df):
        await page.goto(url)  # Set timeout to 30 seconds
        await self.random_sleep(5, 30)

        article_urls = []  # List to hold all article URLs
        while True:
            # Extract article URLs
            urls = await page.evaluate('''
                () => {
                    const articles = document.querySelectorAll('div.entries article');
                    return Array.from(articles).map(article => {
                        const link = article.querySelector('a');
                        return link ? link.href : null;
                    }).filter(url => url !== null);
                }
            ''')

            article_urls.extend(urls)  # Add extracted URLs to the list
            
            break  # Exit the loop if there's no next page

        # Update the DataFrame with new data
        df[url] = [article_urls]

        # Save the updated DataFrame to JSON
        df.to_json('article_urls.json', orient='index', indent=4)
        


    async def random_sleep(self, min_seconds, max_seconds):
        await asyncio.sleep(random.uniform(min_seconds, max_seconds))

if __name__ == "__main__":
    scraper = TheBrakeReportScraper()
    asyncio.run(scraper.start_scraping())

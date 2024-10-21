from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeoutError
import random
import asyncio
import json
from playwright_stealth import stealth_async
from thebrakereport import TheBrakeReport

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


    async def check_for_captcha(self, page):
        try:
            captcha_visible = await page.locator("#cf-challenge-running").is_visible(timeout=5000)
            if captcha_visible:
                print("CAPTCHA detected. Please solve it manually.")
                input("Press Enter to continue after solving the CAPTCHA...")
        except PlaywrightTimeoutError:
            pass

    async def start_scraping(self):
        async with async_playwright() as p:
            browser = await p.firefox.launch(headless=True)
            context = await browser.new_context(
                viewport={'width': 1920, 'height': 1080},
                user_agent=random.choice(self.user_agents)
            )
            
            page = await context.new_page()
            await stealth_async(page)

            await self.emulate_human_behavior(page)

            
            await self.scrape_pages(page, 'https://thebrakereport.com/ford-edge-brake-hose-investigation/')

            await browser.close()

    async def emulate_human_behavior(self, page):
        """Simulate human-like interactions."""
        await page.mouse.move(random.randint(0, 500), random.randint(0, 500))
        await page.mouse.down()
        await page.mouse.up()
        await self.random_sleep(2, 5)  # Pause after mouse interactions

    async def scrape_pages(self, page, url):
        await page.goto(url, wait_until="domcontentloaded", timeout=30000)  # Set timeout to 20 seconds
        await self.check_for_captcha(page)
        await self.random_sleep(5, 30)

        articles = []
        while True:
            article_urls = await page.evaluate('''
                () => {
                    const articles = document.querySelectorAll('div.entries article');
                    return Array.from(articles).map(article => {
                        const link = article.querySelector('a');
                        return link ? link.href : null;
                    }).filter(url => url !== null);
                }
            ''')
            next_page = await page.query_selector('a.next.page-numbers')
            next_page_url = await next_page.get_attribute('href') if next_page else None
            print(next_page_url)
 
            for article_url in article_urls:
                try:
                    article_data = await self.scrape_article(page, article_url)
                    articles.append(article_data)
                except Exception as e:
                    print(f"Error scraping article {article_url}: {e}")

            print(next_page_url)
            if next_page_url:
                await page.goto(next_page_url, wait_until="domcontentloaded", timeout=20000)

            if next_page_url == "https://thebrakereport.com/page/20/":
                break
            await page.goto(next_page_url, wait_until="domcontentloaded")
            await self.check_for_captcha(page)

            await page.wait_for_load_state("domcontentloaded")
            await self.random_sleep(5, 10)


    async def scrape_article(self, page, url):
        print(f"Scraping: {url}")
        await page.goto(url, wait_until="domcontentloaded")
        await self.check_for_captcha(page)
        await self.random_sleep(3, 5)

        article_data = await page.evaluate('''
            () => {
                const headline = document.querySelector('h1.page-title')?.innerText;
                const categories = Array.from(document.querySelectorAll('li.meta-categories a')).map(a => a.innerText);
                const timestamp = document.querySelector('li.meta-date time')?.getAttribute('datetime');
                const author_name = document.querySelector('li.meta-author span[itemprop="name"]')?.innerText;
                const text_body = document.querySelectorAll('div.ct-container')[2];
                const paragraphs = text_body ? Array.from(text_body.querySelectorAll('p')).slice(0, -2) : [];
                const article_text = paragraphs.map(p => p.innerText).join(' ');

                return {
                    headline,
                    url: window.location.href,
                    categories,
                    timestamp,
                    author_name,
                    article_text
                };
            }
        ''')

        return article_data

    async def random_sleep(self, min_seconds, max_seconds):
        await asyncio.sleep(random.uniform(min_seconds, max_seconds))

if __name__ == "__main__":
    scraper = TheBrakeReportScraper()
    asyncio.run(scraper.start_scraping())
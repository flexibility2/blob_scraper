import requests
from bs4 import BeautifulSoup
import sqlite3
from datetime import datetime
import schedule
import time
import logging
import random

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_random_user_agent():
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Safari/605.1.15',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0'
    ]
    return random.choice(user_agents)

def scrape_blog(url, blog_name):
    try:
        headers = {
            'User-Agent': get_random_user_agent(),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Referer': 'https://www.google.com/',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        logger.info(f"Successfully fetched {url}")
        logger.info(f"Page title: {soup.title.string if soup.title else 'No title found'}")
        
        results = []
        
        if blog_name == "Protocol Labs":
            posts = soup.find_all('article', class_='card-post')
            logger.info(f"Found {len(posts)} potential posts for Protocol Labs")
            for post in posts:
                title = post.find('h1', class_='type-h5')
                content = post.find('p', class_='type-p1-serif')
                date = post.find('time')
                
                if title and content and date:
                    results.append({
                        'title': title.text.strip(),
                        'content': content.text.strip(),
                        'date': date['datetime'],
                        'blog_name': blog_name
                    })
        
        elif blog_name == "Ethereum":
            posts = soup.find_all('div', class_='css-1g7quxy')
            logger.info(f"Found {len(posts)} potential posts for Ethereum")
            for post in posts:
                title = post.find('a', class_='chakra-link')
                content = post.find('p', class_='chakra-text css-jxubeb')
                date = post.find('div', class_='css-1y8927a')
                
                if title and content:
                    results.append({
                        'title': title.text.strip(),
                        'content': content.text.strip(),
                        'date': date.text.strip() if date else 'Unknown',
                        'blog_name': blog_name
                    })
        
        logger.info(f"Found {len(results)} posts for {blog_name}")
        return results
    except Exception as e:
        logger.error(f"Error scraping {blog_name}: {str(e)}")
        return []

# 移除 summarize_text 函數

def store_in_database(posts):
    conn = sqlite3.connect('blogdb.sqlite')
    cur = conn.cursor()
    
    cur.execute('''CREATE TABLE IF NOT EXISTS blog_posts
                   (id INTEGER PRIMARY KEY, title TEXT, content TEXT, date TEXT, blog_name TEXT)''')
    
    for post in posts:
        cur.execute(
            "INSERT INTO blog_posts (title, content, date, blog_name) VALUES (?, ?, ?, ?)",
            (post['title'], post['content'], post['date'], post['blog_name'])
        )
    
    conn.commit()
    cur.close()
    conn.close()

def main():
    blogs = [
        ("https://protocol.ai/blog/", "Protocol Labs"),
        ("https://blog.ethereum.org/", "Ethereum"),
        # 暫時註釋掉 Coinbase
        # ("https://www.coinbase.com/blog", "Coinbase")
    ]
    
    for url, name in blogs:
        logger.info(f"Scraping {name}...")
        posts = scrape_blog(url, name)
        if posts:
            store_in_database(posts)
        else:
            logger.warning(f"No posts found for {name}")
        time.sleep(random.uniform(1, 3))  # 添加隨機延遲
    logger.info(f"Scraping completed at {datetime.now()}")

if __name__ == "__main__":
    logger.info("Starting the scraper...")
    main()  # Run once immediately
    logger.info("Initial scraping completed. Setting up schedule...")
    schedule.every().day.at("00:00").do(main)
    while True:
        schedule.run_pending()
        time.sleep(60)
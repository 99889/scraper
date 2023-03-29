import requests
from bs4 import BeautifulSoup
import sqlite3
import csv
import datetime

class VergeScraper:
    
    def __init__(self, url):
        self.url = url
        self.articles = []
    
    def scrape(self):
        response = requests.get(self.url)
        soup = BeautifulSoup(response.text, 'html.parser')
        article_elements = soup.find_all('article', class_='c-compact-river__entry')
        
        for element in article_elements:
            try:
                title = element.find('h2', class_='c-entry-box--compact__title').text.strip()
                url = element.find('a', class_='c-entry-box--compact__image-wrapper')['href']
                author = element.find('span', class_='c-byline__item').text.strip()
                date = element.find('time')['datetime'][:10]
                self.articles.append({'title': title, 'url': url, 'author': author, 'date': date})
            except:
                pass
    
    def save_to_csv(self):
        today = datetime.datetime.today().strftime('%d%m%Y')
        with open(f'{today}_verge.csv', mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=['id', 'url', 'headline', 'author', 'date'])
            writer.writeheader()
            for i, article in enumerate(self.articles):
                writer.writerow({'id': i, 'url': article['url'], 'headline': article['title'], 'author': article['author'], 'date': article['date']})
    
    def save_to_sqlite(self):
        conn = sqlite3.connect('theverge.db')
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS articles
                        (id INTEGER PRIMARY KEY, url TEXT, headline TEXT, author TEXT, date TEXT)''')
        for i, article in enumerate(self.articles):
            cursor.execute(f"INSERT OR IGNORE INTO articles VALUES (?, ?, ?, ?, ?)", (i, article['url'], article['title'], article['author'], article['date']))
        conn.commit()
        conn.close()
    
if __name__ == '__main__':
    scraper = VergeScraper('https://www.theverge.com/')
    scraper.scrape()
    scraper.save_to_csv()
    scraper.save_to_sqlite()

from bs4 import BeautifulSoup
import requests
import csv,sqlite3
import pandas as pd
from datetime import datetime

response = requests.get('https://www.theverge.com/')

soup = BeautifulSoup(response.content, 'lxml')

articles = soup.find_all("li", class_="duet--content-cards--content-card")

data = []

for i,article in enumerate(articles):
    headline = article.find('h2',class_="font-polysans").text
    url = 'https://theverge.com/'+article.find('a').get('href')
    author = article.find('a',class_="text-gray-31").text
    date_response = requests.get(url)
    soup = BeautifulSoup(date_response.content,'lxml')
    time = soup.find('time').get('datetime')
    date = pd.to_datetime(time).date()
    data = [i,headline,url,author,date]

file = datetime.now().strftime("%d%m%Y_verge.csv")
with open(file,'w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['id','headline','url','author','date'])
    for i, data_ in enumerate(data):
        writer.writerow([i+1, data_])

conn = sqlite3.connect('verge.db')
c = conn.cursor()
c.execute("CREATE TABLE article (id INTEGER PRIMARY KEY, URL TEXT, headline TEXT, author TEXT, date TEXT)")
c.executemany("INSERT INTO article (id, URL, headline, author, date) VALUES (?, ?, ?, ?, ?)", data)
conn.commit()
conn.close()

from bs4 import BeautifulSoup
from datetime import datetime   
import os
import requests
import pandas as pd

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}


def get_articles_with_content(article_list):
    valid_articles = []
    for article in article_list:
        if 'published' in article and 'content' in article:
            valid_articles.append(article)
    return valid_articles


def get_article_list_from_dawn(url):
    response = requests.get(url,headers =headers)
    if response.status_code != 200:
        print('Failed to retrieve articles')
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    arts = soup.find_all('article', class_='story')

    article_list = []
    for art in arts:
        title_tag = art.find('h2', class_='story__title')
        if not title_tag:
            continue
        link = title_tag.find('a')['href']
        title = title_tag.get_text(strip=True)
        article_list.append({
            'title': title,
            'url': link,
        })

    return article_list


def get_article_content_from_dawn(url):
    response =  requests.get(url,headers= headers)
    if response.status_code != 200:
#         print('Failed to retrieve articles')
        return '',''

    soup = BeautifulSoup(response.text, 'html.parser')
    content_div = soup.find('div', class_='story__content')
    time_tag = soup.find('span', class_='timestamp--time')
    if time_tag and 'title' in time_tag.attrs:
        date_time_str = time_tag['title']
        date_time_obj = datetime.strptime(date_time_str, '%Y-%m-%dT%H:%M:%S%z').date()
    else:
        date_time_obj = datetime.now().date() 

              
    if content_div:
        return date_time_obj,' '.join(paragraph.get_text(strip=True) for paragraph in content_div.find_all('p'))
    else:
        return '',''
    
    
    
def get_article_list_from_ary(url):
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
#         print('Failed to retrieve articles')
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    arts = soup.find_all('div', class_='td-module-container')

    article_list = []
    for art in arts:
        title_tag = art.find('h3', class_='entry-title')
        if not title_tag:
            continue
        link = title_tag.find('a')['href']
        title = title_tag.get_text(strip=True)
        article_list.append({
            'title': title,
            'url': link,
        })

    return article_list


def get_article_content_from_ary(url):
    response = requests.get(url,headers= headers)
    if response.status_code != 200:
#         print('Failed to retrieve articles')
        return '',''

    soup = BeautifulSoup(response.text, 'html.parser')
    content_div = soup.find('div', class_='td-post-content')
#     print(content_div)
    time_tag = soup.find('time', class_='entry-date')
    if time_tag and 'datetime' in time_tag.attrs:
        date_time_str = time_tag['datetime']
        date_time_obj = datetime.strptime(date_time_str, '%Y-%m-%dT%H:%M:%S%z').date()
    else:
        date_time_obj = datetime.now().date()
              
    if content_div:
        return date_time_obj,' '.join(paragraph.get_text(strip=True) for paragraph in content_div.find_all('p'))
    else:
        return '',''
    



def web_scrape_articles():
    print("web scarping .....")
    dawn_article_list_url = 'https://www.dawn.com/pakistan'
    articles = get_article_list_from_dawn(dawn_article_list_url)

    for article in articles:
        date , content = get_article_content_from_dawn(article['url'])
        if date and content:
            article['published'] = date
            article['content'] = content

    dawn_articles = get_articles_with_content(articles)
    print(dawn_articles)
    
    
    ary_article_list_url = 'https://arynews.tv/category/pakistan/'
    articles = get_article_list_from_ary(ary_article_list_url)

    for article in articles:
        date , content = get_article_content_from_ary(article['url'])
        if date and content:
            article['published'] = date
            article['content'] = content

    ary_articles = get_articles_with_content(articles)
    print(ary_articles)
    
    dawn_articles.extend(ary_articles)
    articles = pd.DataFrame(dawn_articles)
    
    return articles
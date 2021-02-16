import requests
from bs4 import BeautifulSoup
import pymongo
import pandas as pd
markup4 = requests.get(f'https://blog.digimind.com/fr/tendances/covid-30-fake-news-les-plus-repandues-sur-medias-sociaux#top5').text
soup4 = BeautifulSoup(markup4, 'html.parser')
markup3 = requests.get(f'https://www.rtbf.be/info/dossier/epidemie-de-coronavirus/detail_coronavirus-le-vrai-et-le-faux-des-rumeurs-et-idees-recues-sur-le-covid-19?id=10441926').text
soup3 = BeautifulSoup(markup3, 'html.parser')

markup1 = requests.get(f'https://www.who.int/fr/health-topics/coronavirus/coronavirus#tab=tab_1').text
soup1 = BeautifulSoup(markup1, 'html.parser')
markup = requests.get(f'https://www.inserm.fr/information-en-sante/dossiers-information/coronavirus-sars-cov-et-mers-cov').text
soup = BeautifulSoup(markup, 'html.parser')
markup2 = requests.get(f'https://www.topsante.com/medecine/maladies-infectieuses/zoonoses/vaccin-anti-covid-640575').text
soup2 = BeautifulSoup(markup2, 'html.parser')

item2 = soup2.find('div',class_='article-content')
item1 = soup1.find('div',class_='sf_colsOut tabContent')
item = item1.find('div',class_='sf_colsIn')
fake_news = []
real_news = []
item3 = soup3.find('div',class_='rtbf-article-text')
item4= item3.ul
for data in soup.find_all('div',class_='col-12'):
    news = {} 
    for text in data.find_all('p'):
        news = {}
        if text.find('a') is not None :
            continue
        elif text.find('h4') is not None :
            continue
        else:
            
            news['text'] =text.text
            news['source'] = 'inserm.fr'
            
            real_news.append(news)

for data in item.find_all('p'):
    news = {}
    news['text'] = data.text
    news['source'] = 'Organization mondiale de la santé'
    real_news.append(news)
    print(news)


for data in item2.find_all('p'):
    news = {}
    if data.find('a') is not None :
        continue
    elif data.find('strong') is not None :
        continue
    else:
        news['text'] = data.text
        news['source'] = 'topsante.com'
        real_news.append(news)


for data in item4.find_all('li'):
    news = {}
    if('FAUX') in data.strong.text:
        news['text'] = data.text
        news['source'] = 'rtbf.be'
        fake_news.append(news) 
    if('IMPRÉCIS') in data.strong.text:
        news['text'] = data.text
        news['source'] = 'rtbf.be'
        fake_news.append(news) 
    elif('VRAI') in data.strong.text:  
        news['text'] = data.text
        news['source'] = 'rtbf.be'
        real_news.append(news)


for data in soup4.find_all('tr'):
    news = {}
    td=data.find_all('td')
    news['text'] = td[1].span.text 
    news['source'] = 'blog.digimind.com'
    fake_news.append(news)

print(f'inserted {len(fake_news)} articles')
print(f'inserted {len(real_news)} articles')
dffake =  pd.DataFrame(fake_news)
print(dffake.head())
#dffake.to_csv('fake_news.csv', index=False, encoding='utf-8')
dfreal =  pd.DataFrame(real_news)
print(dfreal.head())
#dfreal.to_csv('real_news.csv', index=False, encoding='utf-8')

import pandas as pd
import requests
from bs4 import BeautifulSoup
import pymongo
# make a request to the site and get it as a string
markup =  requests.get(f'https://www.inserm.fr/information-en-sante/dossiers-information/coronavirus-sars-cov-et-mers-cov').text
markup1 = requests.get(f'https://www.who.int/fr/health-topics/coronavirus/coronavirus#tab=tab_1').text
markup2 = requests.get(f'https://www.topsante.com/medecine/maladies-infectieuses/zoonoses/vaccin-anti-covid-640575').text
markup3 = requests.get(f'https://www.rtbf.be/info/dossier/epidemie-de-coronavirus/detail_coronavirus-le-vrai-et-le-faux-des-rumeurs-et-idees-recues-sur-le-covid-19?id=10441926').text
markup4 = requests.get(f'https://blog.digimind.com/fr/tendances/covid-30-fake-news-les-plus-repandues-sur-medias-sociaux#top5').text
markup5 = requests.get(f'https://www.strategies.fr/actualites/medias/4043674W/les-10-fake-news-les-plus-repandues-sur-le-covid-19.html').text
markup6 = requests.get(f'https://www.rtl.fr/actu/bien-etre/coronavirus-cinq-fake-news-qui-circulent-sur-la-covid-19-7800676001').text
markup7 = requests.get(f'https://www.who.int/fr/emergencies/diseases/novel-coronavirus-2019/question-and-answers-hub/q-a-detail/coronavirus-disease-covid-19#:~:text=symptomes').text

# pass the string to a BeautifulSoup object
soup =  BeautifulSoup(markup, 'html.parser')
soup1 = BeautifulSoup(markup1, 'html.parser')
soup2 = BeautifulSoup(markup2, 'html.parser')
soup3 = BeautifulSoup(markup3, 'html.parser')
soup4 = BeautifulSoup(markup4, 'html.parser')
soup5 = BeautifulSoup(markup5, 'html.parser')
soup6 = BeautifulSoup(markup6, 'html.parser')
soup7 = BeautifulSoup(markup7, 'html.parser')


item2 = soup2.find('div',class_='article-content')
item1 = soup1.find('div',class_='sf_colsOut tabContent')
div = item1.find('div',class_='sf_colsIn')
item3 = soup3.find('div',class_='rtbf-article-text')
item4= item3.ul
fake_news = []
real_news = []
# now we can select elements
for item in soup5.find_all('ul'):
    news = {}
    news['text'] = item.select_one('li').get_text()
    news['source'] = 'strategies journal'
    fake_news.append(news)
    
for item in soup6.find_all('h3',class_='article-title mdl'):    
    news = {}
    news['text'] = item.get_text()
    news['source'] = "RTL journal"
    fake_news.append(news)

# now we can select elements
for item in soup7.select('.sf-accordion__content'):
    news = {}
    news['text'] = item.select_one('p').get_text()
    news['source'] = 'Organisation mondiale de la santé'
    real_news.append(news)


for data in div.find_all('p'):
    news = {}
    news['text'] = data.text
    news['source'] = 'Organization mondiale de la santé'
    real_news.append(news)
    print(news)

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


dffake = pd.DataFrame(fake_news)
dffake.to_csv('fake_news.csv', index=False, encoding='utf-8')

dfreal = pd.DataFrame(real_news)
dfreal.to_csv('real_news.csv', index=False, encoding='utf-8')


import urllib
from bs4 import BeautifulSoup
from http.cookiejar import CookieJar
import warnings
warnings.filterwarnings("ignore",category=UserWarning,module="bs4")
import random
import time
import csv
import json
import math
import os.path
import chardet
import datetime
from time import strptime
# print(datetime.datetime.now().strftime ("%d-%m-%Y"))
# print("5 days ago")
# print((datetime.datetime.now()-datetime.timedelta(days=5)).strftime ("%d-%m-%Y"))
# print("1 weeks ago")
# print((datetime.datetime.now()-datetime.timedelta(weeks=1)).strftime ("%d-%m-%Y"))


headers=[
        ('Host', "tripadvisor.in"),
        ('Accept', "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8"),
        ('Accept-Language', "en-GB,en-US;q=0.9,en;q=0.8"),
        ('Referer', "url"),
        ('Connection', "keep-alive"),
        ('User-Agent', "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"),  #Keep this as last because of pop used
]

userAgents=[
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"
        "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
]

cookieJar=CookieJar()
opener=urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookieJar))

opener.addheaders=headers

query = input('Enter place name : ')
limit = input('Enter no of places to scrape reviews from : ')
query = urllib.parse.quote_plus(query)
url='https://www.tripadvisor.in/TypeAheadJson?action=API&types=attr&urlList=false&query=' + query + '&max=' + limit +'&uiOrigin=trip_search_Attractions&source=trip_search_Attractions'

response=opener.open(url)

content=response.read()

#data = json.loads(content)
data = json.loads(content.decode(chardet.detect(content)["encoding"]))


for result in data['results']:
    url = 'https://www.tripadvisor.in' + result['url']
    page_url = url
    filename = result['name'].split(',')[0] + '.csv'
    page_offset = 0
    headers.pop()
    headers.append(('User-Agent',random.SystemRandom().choice(userAgents)))
    cookieJar=CookieJar()
    opener=urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookieJar))
    opener.addheaders=headers
    response=opener.open(page_url)
    content=response.read()
    soup=BeautifulSoup(content)

    pages = math.ceil(int(soup.find('span',{'class':'reviews_header_count'}).text.strip('()').replace(',',''))/10)
    print('No of pages for ' + page_url + ' : ', pages)
    pages = input('Enter no of pages you want to scrape: ')
    reviews=[]
    review_count = 0
    for i in range(int(pages)):
        print("page no: ",i + 1)
        print("page url : ",page_url)        
        headers.pop()
        headers.append(('User-Agent',random.SystemRandom().choice(userAgents)))
        cookieJar=CookieJar()
        opener=urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookieJar))
        opener.addheaders=headers
        response=opener.open(page_url)
        content=response.read()
        soup=BeautifulSoup(content)
        review_container = soup.findAll('div',{'class':'review-container'})
        print('No of reviews: ',len(review_container))
        if(len(review_container) == 0):
            print(content)
        
        count = 0
        for review_div in review_container:
            review = {}
            review_count+=1
            review['id'] = review_count
            try:
                review['title'] = review_div.find('span',{'class':'noQuotes'}).text
            except:
                review['title'] = 'Not-found'
            try:
                review['review'] = review_div.find('p',{'class':'partial_entry'}).text
            except: 
                review['review'] = 'Not-found'
            try:
                review['rating'] = int(review_div.find('div',{'class':'ratingInfo'}).span['class'][1].split('_')[1])/10
            except:
                review['rating'] = 'Not-found'
            try:
                date_string = review_div.find('div',{'class':'ratingInfo'}).find('span',{'class':'ratingDate'}).text.strip()
                date_type='days'
                month_number = 0
                no=None
                if date_string.find('ago') != -1:
                    no = date_string.split(' ')[1]
                    if date_string.find('day') != -1:
                        date_type='days'
                    elif date_string.find('week') != -1:
                        date_type='weeks'
                                            
                elif date_string.find('yesterday'):
                    date_type = 'days'
                    no = 1

                if no is not None:
                    if date_type == 'days':
                        print('DAYS')
                        review['date'] = (datetime.datetime.now()-datetime.timedelta(days=int(no))).strftime ("%d-%m-%Y")
                        print(review['date'])

                    else:
                        print('WEEKS')
                        review['date'] = (datetime.datetime.now()-datetime.timedelta(weeks=int(no))).strftime ("%d-%m-%Y")
                        print(review['date'])
                else:
                    month_number = strptime(date_string.split(' ')[2],'%B').tm_mon
                    date_string = date_string.split(' ')[1] +  ' ' + month_number + ' ' + date_string.split(' ')[3]
                    review['date'] = datetime.datetime.strptime(date_string, '%d %m %Y').strftime ("%d-%m-%Y")
            except:
                review['date'] = 'Not-found'
            try:
                review['user_name'] = review_div.find('div',{'class':'userInfo'}).find('span').text.strip()
            except:
                review['user_name'] = 'Not-found'
            
            try:
                review['review_likes'] = review_div.find('span',{'class':'numHelp'}).text.strip()
            except:
                review['review_likes'] = 'Not-found'

            if review['review_likes'] == '':
                review['review_likes'] = 0

            reviews.append(review)
            
        page_offset += 10
        url_splitted = url.split('-Reviews-')
        page_url = url_splitted[0] + '-Reviews-or' + str(page_offset) + '-' + url_splitted[1]


    writeHeader=True
    if((os.path.exists(filename))):
        writeHeader=False
        
    with open(filename, 'a') as f:
        writer = csv.DictWriter(f, reviews[0].keys())
        if writeHeader:
            writer.writeheader()
        for review in reviews:
            writer.writerow(review)
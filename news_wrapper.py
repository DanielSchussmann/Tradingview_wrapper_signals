import requests
from bs4 import BeautifulSoup
import json
from Selenium_class import *
import time


def SELENIUM_NEWS_ALGO(symbols):
    x = DRIVER()
    x.set_standard_options()
    x.start()
    for symbol in symbols:
        time.sleep(2)

        x.driver.get(f'https://www.tradingview.com/symbols/{symbol["TV_indicators"]["symbol"]}/news/')
        wrapper = x.driver.find_elements(By.CSS_SELECTOR,'.card-rY32JioV')

        for w in wrapper[0:30]:
            try:
                headline = w.find_element(By.CSS_SELECTOR,'.title-rY32JioV').text
                link =  w.get_attribute('href')
                date = w.find_element(By.CSS_SELECTOR,'.breadcrumbs-rY32JioV').find_elements(By.CSS_SELECTOR,'*')[0].get_attribute('title')

            except:
                print('EXCEPTED')
                continue


            print([headline,link,date])
"""
        x.driver.get(f'https://www.investing.com/currencies/{symbol["daily-fx"]}-news/')
        wrapper = x.driver.find_elements(By.CSS_SELECTOR, '.inv-link.text-secondary.font-bold.text-sm.whitespace-normal')
        for w in wrapper[0:30]:
            headline = w.find_element(By.CSS_SELECTOR, ".news-analysis_content__vBoNw.text-xs").text

            link = w.find_element(By.CSS_SELECTOR, ".news-analysis_content__vBoNw.text-xs").get_attribute('href')
            date = w.find_element(By.CSS_SELECTOR, '.ml-1.shrink-0').text



            print([headline, link, date])"""



#SELENIUM_NEWS_ALGO([EUR_USD,GBP_USD,NZD_USD])




def TV_news(symbol):
    symb = symbol['TV_news']
    link = 'https://www.tradingview.com/symbols/{}/news/'.format(symb)
    print(link)
    response = requests.get(link, timeout=(2000,2000))
    soup = BeautifulSoup(response.text, "html.parser")
    #print(soup)
    headlines = []
    for headline in soup.select(".tv-widget-news-item__title"):
        headlines.append(headline.text.strip())

    return headlines


#print(TV_news(IBM))



def DAILY_FX_NEWS(symbol_list):
    try:
        with open('DAILY_FX_NEWS.json') as file:
            data = json.load(file)

        for symbol in symbol_list:
            url = f"https://www.dailyfx.com/{symbol['daily-fx']}/news-and-analysis"
            response = requests.get(url)
            soup = BeautifulSoup(response.content, "html.parser")

            wrappers = soup.select(".dfx-articleListItem.jsdfx-articleListItem.d-flex.mb-3")

            #ts = str(datetime.datetime.now())

            #data[symbol['this']][ts] = []
            for w in wrappers:
                headline = \
                w.select(".dfx-articleListItem__title.jsdfx-articleListItem__title.font-weight-bold.align-middle")[
                    0].decode_contents()
                date = w.select(".jsdfx-articleListItem__date.text-nowrap")[0].decode_contents()
                link = w['href']

                data[symbol['this']]['DAILY_FX'].insert(0,{'date': date, 'headline': headline, 'link': link})

        with open('DAILY_FX_NEWS.json', 'w') as file:
            json.dump(data, file)

        return True

    except:
        return False


# MAIN FILE



#D_FX = DAILY_FX_NEWS(FX_symbols)

# print(D_FX)



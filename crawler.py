import time
import random
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
browser = webdriver.Chrome("C:\Program Files\Google\chromedriver.exe")

user_agents = ['Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20130406 Firefox/23.0', \
      'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:18.0) Gecko/20100101 Firefox/18.0', \
      'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/533+ \
      (KHTML, like Gecko) Element Browser 5.0', \
      'IBM WebExplorer /v0.94', 'Galaxy/1.0 [en] (Mac OS X 10.5.6; U; en)', \
      'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)', \
      'Opera/9.80 (Windows NT 6.0) Presto/2.12.388 Version/12.14', \
      'Mozilla/5.0 (iPad; CPU OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) \
       Version/6.0 Mobile/10A5355d Safari/8536.25', \
      'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) \
       Chrome/28.0.1468.0 Safari/537.36', \
      'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0; TheWorld)']

block_site = ['youtube', 'twitter', 'facebook', 'kkbox', 'instagram', 'twitch', 'weibo']
results = {}
def google_search(search_list, num_page = 1):
    global results
    for x in search_list:
        if x not in results:
            results[x] = {}
            for page in range(num_page):
                url = 'http://www.google.com.tw/search?q=' + x + '&start=' + str(page*10)
                time.sleep(3)
                try:
                    while True:
                        time.sleep(1)
                        index = random.randint(0, 9)
                        headers = {'User-Agent': user_agents[index]}
                        browser.get(url)
                        soup = BeautifulSoup(browser.page_source, "html.parser")
                        search_block = soup.find_all("div", class_="g")
                        if (search_block): #if crawler's working fine
                            for i in search_block:
                                if sum([k in i.find("a").get('href') for k in block_site]) == 0:
                                    if "title" not in results[x].keys():
                                        results[x]["title"] = [i.find("h3").text]
                                    else:
                                        results[x]["title"].extend([i.find("h3").text])
                                    if "snippet" not in results[x].keys():
                                        results[x]["snippet"] = [i.find("span", class_='st').text]
                                    else:
                                        results[x]["snippet"].extend([i.find("span", class_='st').text])
                                else:
                                    continue
                            # results count
                            count_text = soup.find("div", id="resultStats").text.split(" ")
                            if count_text[1] != "項結果":
                                search_counts = int(count_text[1].replace(",",""))
                            else:
                                search_counts = int(count_text[0].replace(",",""))
                            results[x]["count"] = search_counts
                            break
                        else: #crawler being blocked
                            print("faild to crawl anything, retrying...")
                            time.sleep(20)
                            continue
                except Exception as e:
                    print(e)
        else:
            continue
    return results

import time
import random
import requests
from bs4 import BeautifulSoup

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

# get free proxy from free-proxy-list.net
proxy_site = 'https://free-proxy-list.net/'
res = requests.get(url=proxy_site)
soup = BeautifulSoup(res.text, "html.parser")
rows = soup.select("tr > td")
proxies_pool = []
for i in range(0, 100, 8):
    full_proxy = "http://" + rows[i].string + ":" + rows[i+1].string
    proxies_pool.append(full_proxy)

def google_search(search_list, num_page = 1):
    results = {}
    for x in search_list:
        results[x] = {}
        for page in range(num_page):
            url = 'https://www.google.com.tw/search?q=' + x + "&start=" + str(page*10)
            time.sleep(3)
            while True:
                index = random.randint(0, 9)
                proxies = {"http": proxies_pool[index]}
                headers = {'User-Agent': user_agents[index]}
                res = requests.get(url=url, headers=headers, proxies=proxies)
                soup = BeautifulSoup(res.text, "html.parser")
                search_title = soup.find_all("h3", class_="LC20lb")
                search_content = soup.find_all("span", class_="st")
                if (search_title):
                    if "title" not in results[x].keys():
                        results[x]["title"] = [search_title[i].text for i in range(len(search_title))]
                    else:
                        results[x]["title"].extend([search_title[i].text for i in range(len(search_title))])
                    if "snippet" not in results[x].keys():
                        results[x]["snippet"] = [search_content[i].text for i in range(len(search_content))]
                    else:
                        results[x]["snippet"].extend([search_content[i].text for i in range(len(search_content))])
                    search_counts = int(soup.find("div", id="resultStats").text.split(" ")[1].replace(",",""))
                    print(search_counts)
                    break
                else:
                    print("faild to crawled anything, retrying...")
                    continue
    return results

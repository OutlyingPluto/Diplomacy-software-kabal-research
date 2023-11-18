from urllib.request import urlopen
from urllib.parse import urlparse

import pickle

from bs4 import BeautifulSoup

urlMAIN = "https://www.theguardian.com/world"
# CNA = "https://www.channelnewsasia.com/latest-news"
# TOI = "https://timesofindia.indiatimes.com/"
# CNN = "https://edition.cnn.com/"
# Guardian = "https://www.theguardian.com/world"
# Yahoo = "https://news.yahoo.com/world/"
# NYT = "https://www.nytimes.com/"
# The Hindu = "https://www.thehindu.com/"
# Bloomberg = "https://www.bloomberg.com/asia"
# WSJ = "https://www.wsj.com/"
# Forbes = "https://www.forbes.com/news"


def CleanPage(page): # this function is still dysfunctional
    listed = page.splitlines()
    for line in listed:
        if len(line.split(" ")) < 5:
            listed.remove(line)
    return '\n'.join(listed)


def ScrapePage(url):
    try:
        page = urlopen(url)
    except ValueError:
        url = urlparse(urlMAIN).scheme + "://" + urlparse(urlMAIN).netloc + url
        page = urlopen(url)

    html_bytes = page.read()
    html = html_bytes.decode("utf-8")

    # one-liner cuz y not
    # html = urlopen(url).read().decode("utf-8")

    title_index = html.find("<title")

    i = 0

    while True:
        i += 1 
        if html[title_index + i] == ">":
            start_index = title_index + i + 1
            break

    end_index = html.find("</title>")
    title = html[start_index:end_index]

    soup = BeautifulSoup(html, "html.parser")

    raw_paras = []

    if "https://www.channelnewsasia.com" in url:
        filter = lambda tag: tag.name == "p" and not tag.has_attr("class")
        raw_data = soup.find_all(filter)
        for data in raw_data:
            raw_paras.append(data)

        paras = [para.get_text() for para in raw_paras[:-4]]
    elif "https://www.theguardian.com" in url:
        filter = lambda tag: tag.name == "p" and tag.has_attr("class") #tag.get("class") == "dcr-1kas69x"
        raw_data = soup.find_all(filter)
        for data in raw_data:
            raw_paras.append(data)

        paras = [para.get_text() for para in raw_paras]

    for para in paras:
        print(para)

    lines = (line.strip() for line in paras)

    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))

    text = '\n'.join(chunk for chunk in chunks if chunk)

    print(text)

    return(text)


def ScrapeDir(url):

    page = urlopen(url)

    html_bytes = page.read()
    html = html_bytes.decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")
    # one-liner cuz y not
    # soup = BeautifulSoup(urlopen(url).read().decode("utf-8"), "html.parser")

    match url:
        case "https://www.channelnewsasia.com/latest-news": # working
            titles = soup.find_all('h6')
            LinksTable = {} # Format of {title: link}
            root = urlparse(url).scheme + "://" + urlparse(url).netloc

            for i in titles:
                try:
                    LinksTable[i.get_text()] = root + i.find('a')['href']
                except TypeError:
                    pass

            return(LinksTable)
        
        case "https://timesofindia.indiatimes.com/": # working
            titles = soup.find_all('a', class_="Hn2z7 undefined")
            LinksTable = {} # Format of {title: link}

            for i in titles:
                try:
                    LinksTable[i.get_text()] = i['href']
                except TypeError:
                    pass

            return(LinksTable)
            
        case "https://www.theguardian.com/world": # working
            titles = soup.find_all(lambda tag: tag.name == "a" and len(tag.get_text().split()) > 7)
            LinksTable = {} # Format of {title: link}

            for i in titles:
                try:
                    LinksTable[i.get_text()] = i['href']
                except TypeError:
                    pass

            return(LinksTable)

        case "https://news.yahoo.com/world/": # working
            titles = soup.find_all('h3')
            LinksTable = {} # Format of {title: link}
            root = urlparse(url).scheme + "://" + urlparse(url).netloc
            # root = ""

            for i in titles:
                try:
                    LinksTable[i.get_text()] = root + i.find('a')['href']
                except TypeError:
                    pass

            return(LinksTable)
        
        case "https://www.nytimes.com/": # not working (anti-scraper technique)
            titles = soup.find_all('script')
            return titles
        
        # case "https://www.thehindu.com/": # 403 forbidden
        #     titles = soup.find_all(lambda tag: tag.name == "a" and not tag.has_attr("class"))
        # case "https://www.bloomberg.com/asia": # not working (captcha-blocked)
        #     titles = soup.find_all(lambda tag: tag.name == "a" and not tag.has_attr("class"))
        # case "https://www.wsj.com/": # 403 forbidden
        #    titles = soup.find_all('span', class_=".WSJTheme--headlineText--He1ANr9C")
        
        case "https://www.forbes.com/news": # working
            titles = soup.find_all('h3')
            LinksTable = {} # Format of {title: link}
            root = urlparse(url).scheme + "://" + urlparse(url).netloc
            # root = ""

            for i in titles:
                try:
                    LinksTable[i.get_text()] = root + i.find('a')['href']
                except TypeError:
                    pass

            return(LinksTable)
        
        case _:
            return None

links = ScrapeDir(urlMAIN)

articles = {}

for key, value in links.items():
    articles[key] = ScrapePage(value)

with open("Articles.bin", "rb") as f:
    try:
        ExistingData = pickle.load(f)
        articles.update(ExistingData)
    except EOFError:
        pass

with open("Articles.bin", "wb") as f:
    pickle.dump(articles, f)


# ScrapePage("https://www.theguardian.com/world/2023/nov/18/apec-summit-ends-with-unity-on-wto-reform-but-not-gaza-or-ukraine")

"""
# Use this wherever you're calling these scraper functions

urls = [CNA, Guardian, TOI, CNN, Fox...]
scraped = []
for url in urls:
    links = ScrapeDir(url)
    scraped.append(ScrapePage(list(links.values())[3]))
"""
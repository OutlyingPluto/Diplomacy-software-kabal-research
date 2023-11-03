from urllib.request import urlopen
from urllib.parse import urlparse

from bs4 import BeautifulSoup

url = "https://www.theguardian.com/world"
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
    page = urlopen(url)

    html_bytes = page.read()
    html = html_bytes.decode("utf-8")

    title_index = html.find("<title")

    i = 0

    while True:
        i += 1 
        if html[title_index + i] == ">":
            start_index = title_index + i + 1
            break

    end_index = html.find("</title>")
    title = html[start_index:end_index]

    print(title)

    soup = BeautifulSoup(html, "html.parser")
    text = soup.get_text()

    lines = (line.strip() for line in text.splitlines())

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

                    if i['href'][0:5] != "https":
                        root = urlparse(url).scheme + "://" + urlparse(url).netloc
                        LinksTable[i.get_text()] = root + i['href']

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
        
def ParseTitles(titles):

    import spacy
    import os

    dir = os.getcwd()
    # dir = dir[:len(dir) - dir[::-1].find("\\")] # Move down a level

    nlp_textcat = spacy.load(dir + "\\textcat_output\\model-last")

    classification = {}

    for title in titles:
        docPred = nlp_textcat(title)
        res = docPred.cats
        classification[title] = max(res, key=res.get)

    return classification

links = ScrapeDir(url)

# titles = links.keys()
# results = ParseTitles(titles)

# print(results)

ScrapePage(list(links.values())[9])

"""
# Use this wherever you're calling these scraper functions

urls = [CNA, Guardian, TOI, CNN, Fox...]
scraped = []
for url in urls:
    links = ScrapeDir(url)
    scraped.append(ScrapePage(list(links.values())[3]))
"""
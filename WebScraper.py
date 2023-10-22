from urllib.request import urlopen
from urllib.parse import urlparse

from bs4 import BeautifulSoup

url = "https://www.channelnewsasia.com/latest-news"

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

    titles = soup.findAll('h6') # This is a line that needs to be changed for every web page you are going to examine

    # Times Of india: soup.findAll('div', class_="col_l_6")

    LinksTable = {} # Format of {title: link}

    root = urlparse(url).scheme + "://" + urlparse(url).netloc # This also needs to be change for every web page you are going to examine (either there or not there)
    # root = ""

    for i in titles:
        try:
            LinksTable[i.get_text()] = root + i.find('a')['href']
        except TypeError:
            pass

    # print(LinksTable)

    return(LinksTable)

links = ScrapeDir(url)

ScrapePage(list(links.values())[3])
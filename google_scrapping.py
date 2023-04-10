from bs4 import BeautifulSoup
import requests
from urllib.parse import quote

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'}

def scrape_search(query: str, page=1):
    url = f"https://www.google.com/search?hl=en&q={quote(query)}" + (f"&start={10*(page-1)}" if page > 1 else "")
    html = requests.get(url, headers=headers)

    soup = BeautifulSoup(html.text, 'html.parser')
    allData = soup.find_all('div', {'class':'g'})

    if len(allData) == 0:
        return 'Гугл отказался вам отвечать'

    g = 0
    Data = []
    l = {}

    for i in range(0, len(allData)):
        link = allData[i].find('a').get('href')

        if (link is not None):
            if (link.find('https') != -1) and (link.find('http') == 0) and (link.find('aclk') == -1):
                g += 1
                l['link'] = link

                try:
                    l['description'] = allData[i].find('div', {'class':'VwiC3b'}).text
                except:
                    l['description'] = None

                Data.append(l)
                l = {}

            else:
                continue

        else:
            continue

    result = extract_discription(Data)
    return result


def extract_discription(Data):
    response = str
    for i in range(len(Data)):
        if Data[i]['description'] is not None:
            response = Data[i]['description']
            break
    return response


import requests
import bs4
import json
import pandas as pd
import lxml
from io import StringIO


class Scraper:
    params = {
        'q': '',
        'hl': 'cs'
    }

    header = {
        ##'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        ##'accept-encoding': 'gzip, deflate, br',
        ##'accept-language' : 'cs-CZ,cs;q=0.9,cs;q=0.8',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36'
    }

    url = 'https://www.google.com/search'

    results = []

    def request(self, query):
        self.params['q'] = query
        request = requests.get(self.url, params=self.params, headers=self.header).text
        soup = bs4.BeautifulSoup(request, "lxml")
        for result in soup.select('.tF2Cxc'):
            self.results.append({
                'title': result.find('h3').text,
                'link': result.select_one('.yuRUbf').a['href'],
                'desc': result.find('div', {'class': 'VwiC3b yXK7lf MUxGbd yDYNvb lyLwlc lEBKkf'}).text
            })

    def to_json(self):
        j = StringIO(json.dumps(self.results, indent=2))
        return j

    def to_pandas(self):
        df = pd.read_json(self.to_json())
        return df

    def to_csv(self):
        csv = self.to_pandas().to_csv('out.csv')
        print(csv)

    def run(self):
        self.request('osobní automobil')
        self.to_pandas()
        print(self.to_pandas())
        self.to_csv()


scraper = Scraper()
scraper.run()

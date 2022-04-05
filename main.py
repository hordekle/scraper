from flask import Flask, render_template, request, redirect, url_for, session, send_file
from io import StringIO
import requests
import bs4
import json
import pandas as pd
import os
import lxml


app = Flask(__name__)
app.secret_key = 'key'

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

RESULTS = []

class Scraper:

    url = 'https://www.google.com/search'


    def request(self):
        req = requests.get(self.url, params=params, headers=header).text
        soup = bs4.BeautifulSoup(req, "lxml")
        for result in soup.select('.tF2Cxc'):
                RESULTS.append({
                'title': result.find('h3').text,
                'link': result.select_one('.yuRUbf').a['href'],
                'desc': result.find('div', {'class': 'VwiC3b yXK7lf MUxGbd yDYNvb lyLwlc lEBKkf'}).text
            })

    def to_json(self):
        j = StringIO(json.dumps(RESULTS, indent=2))
        return j

    def to_pandas(self):
        df = pd.read_json(self.to_json())
        return df

    def to_csv(self):
        csv = self.to_pandas().to_csv('out.csv')
        print(csv)

    def del_file(self, results=RESULTS):
        os.remove('out.csv')
        results.clear()

    def run(self):
        self.request()
        self.to_pandas()
        print(self.to_pandas())
        self.to_csv()

scraper = Scraper()

@app.route('/', methods=["GET", "POST"])
def home():
    if request.method == "POST":
        if request.form['submit_button'] == 'submit':
            search = request.form['search']
            params['q'] = search
            scraper.run()
            path = "out.csv"
            return send_file(path, as_attachment=True)
        if request.form['submit_button'] == 'new search':
            scraper.del_file()

            return redirect(url_for('home'))
    return render_template('index.html')

@app.route('/download')
def download():
    if 'search' in session:
        scraper.run()
        path = "out.csv"
        return send_file(path, as_attachment=True)
    else:
        return redirect(url_for('home'))

@app.route('/clear')
def clear():
    scraper.del_file()
    session.clear()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run()


from threading import Thread

from flask import Flask

from crawler import TJCrawler, KYCrawler
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/task/crawl/TJ')
def crawl_tj():
    TJCrawler()
    return "OK"


@app.route('/task/crawl/KY')
def crawl_ky():
    KYCrawler()
    return "OK"


@app.route('/status')
def status():
    return "OK"

if __name__ == '__main__':
    app.run()

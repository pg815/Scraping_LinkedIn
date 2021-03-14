from flask import Flask,jsonify
from scraper import Scraper

app = Flask("__LinkedInScraper__")

@app.route("/query/<query>", methods = ['GET'])
def scrape(query):
    data = Scraper()
    return jsonify(data.get_data(query))

app.run(debug=True)
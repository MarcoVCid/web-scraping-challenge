from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

@app.route("/")
def index():
    data = mongo.db.data.find_one()
    return render_template("index.html", mars_data = data)

@app.route("/scrape")
def scraper():
    data = mongo.db.data
    mars_dictionary = scrape_mars.scrape()
    data.update({}, mars_dictionary, upsert=True)
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
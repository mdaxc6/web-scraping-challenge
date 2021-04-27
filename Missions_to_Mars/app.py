from flask import Flask, render_template
import pymongo

app = Flask(__name__)

# setup mongo connection
conn = "mongodb://localhost:27017"
client = pymongo.MongoClient(conn)

# connect to mongo db and collection
db = client.planets
db.mars.drop()
mars = db.mars

@app.route("/scrape")
def scrape():
    from scrape_mars import scrape
    data = scrape()
    mars.insert_one(data)
    return render_template("index.html", mars_data=data)

@app.route("/")
def index():
    mars_data = mars.find()
    print(mars_data)
    return render_template("index.html", mars_data=mars_data)


if __name__ == "__main__":
    app.run(debug=True)
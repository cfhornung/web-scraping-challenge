# Dependencies
# https://pypi.org/project/pymongo/
# https://pypi.org/project/Flask-PyMongo/
# https://docs.mongodb.com/manual/tutorial/install-mongodb-on-os-x-tarball/
# https://stackoverflow.com/questions/13312358/mongo-couldnt-connect-to-server-127-0-0-127017
# starting mongo
# mongod --dbpath /usr/local/var/mongodb/data/db --logpath /usr/local/var/log/mongodb/mongo.log --fork
# mongo
#https://www.mongodb.com/try/download/compass

from flask import Flask, render_template, redirect, request, url_for, session
from flask_pymongo import PyMongo
import scrape_mars

# Flask
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri = "mongodb://127.0.0.1:27017/mars_app")

# Route to render index.html template using data from Mongo
@app.route("/")
def index():

    # Find one record of data from the mongo database
    latest_data = mongo.db.collection.find_one()

    print(latest_data)

    # Return template and data
    return render_template("index.html", data = latest_data)

# Route to import scrape_mars.py
@app.route('/scrape')
def scrape():

    # Call scrape
    mars_data = scrape_mars.scrape()
    mongo.db.collection.update({}, mars_data, upsert = True)
    return redirect("/")

# Run
if __name__ == "__main__":
    app.run(debug = True)
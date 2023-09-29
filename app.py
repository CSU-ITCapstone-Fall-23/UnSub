from flask import Flask, render_template, request           # import flask framework
app = Flask(__name__)                                       # create an app instance

import urllib.request, json

@app.route("/")                                             # use the home url
def hello():                                                # method called hello 
    # We need to add the URL we will be using to fetch information from.
    # Sometimes this means also sending some data like a key, but not for this one
    url = "https://xkcd.com/info.0.json"
    response = urllib.request.urlopen(url)
    # Once we have the response we need to extract the data we want.
    data = response.read()
    dict = json.loads(data)
    return render_template("index.html", datum=dict)                    # returns index page

@app.route("/<name>")                                       # route with URL variable /<name>
def hello_name(name):                                       # call method hello_name
    return "Hello "+ name                                   # which returns "hello + name

@app.route("/about")                                        # route with the about variable
def about():                                                # method called about
    name = request.args.get('name') if request.args.get('name') else "Hello World!" # received name variable
    return render_template("about.html", aboutName=name)    # returns about page


if __name__ == "__main__":                                  # when running python app.py
    app.run(debug=True)                                     # run the flask app
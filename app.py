'''from flask import Flask, render_template, request           # import flask framework
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
    app.run(debug=True)                                     # run the flask app'''

# -*- coding: utf-8 -*-

# Sample Python code for youtube.subscriptions.list
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/code-samples#python

import os

# import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

scopes = ["https://www.googleapis.com/auth/youtube.readonly"]

def main():
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "YOUR_CLIENT_SECRET_FILE.json"
    if os.path.exists(CLIENT_SECRETS_FILE):
        print('yes, the client secrets file exists')
    else:
        print('the client secrets file does not exist!')

    # Get credentials and create an API client
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, scopes)
    credentials = flow.run_console()
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials)

    request = youtube.subscriptions().list(
        part="subscriberSnippet",
        mine=True
    )
    response = request.execute()

    print(response)

if __name__ == "__main__":
    main()
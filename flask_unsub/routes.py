import requests
from isodate import parse_duration

from flask import Blueprint, render_template, current_app, request, redirect

from flask import Flask, url_for, redirect, session
from authlib.integrations.flask_client import OAuth

app = Flask(__name__)
app.secret_key = 'random secret'

# oauth config
oauth = OAuth(app)
google = oauth.register(
    name = 'google',
    client_id = '854070362812-sjj9su577pl27l09vg545jsf5o980jk8.apps.googleusercontent.com',
    client_secret='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',
    access_token_url = 'https://accounts.google.com/o/oauth2/token',
    access_token_params = None,
    authorize_url = 'https://accounts.google.com/o/oauth2/auth',
    authorize_params = None,
    api_base_url = 'https://www.googleapis.com/oauth2/v1/',
    client_kwargs = { 'scope' : 'openid profile email '}
)

main = Blueprint("main", __name__)

@main.route("/", methods=["GET", "POST"])
def index():
    search_url="https://www.googleapis.com/youtube/v3/search"
    video_url="https://www.googleapis.com/youtube/v3/videos"

    videos = []

    if request.method == "POST":
        search_params = {
            "key" : current_app.config["YOUTUBE_API_KEY"],
            "q" : request.form.get("query"),
            "part" : "snippet",
            "maxResults" : 9,
            "type" : "video"
        }

        r = requests.get(search_url, params=search_params)

        results = r.json()["items"]

        video_ids = []
        for result in results:
            video_ids.append(result["id"]["videoId"])
        
        if request.form.get("submit") == "lucky":
            return redirect(f"https://www.youtube.com/watch?v={ video_ids[0] }")

        video_params = {
            "key" : current_app.config["YOUTUBE_API_KEY"],
            "id" : ",".join(video_ids),
            "part" : "snippet,contentDetails",
            "maxResults" : 9
        }

        r = requests.get(video_url, params=video_params)
        results = r.json()["items"]
        for result in results:
            video_data = {
                "id" : result["id"],
                "url" : f"https://www.youtube.com/watch?v={ result['id'] }",
                "thumbnail" : result["snippet"]["thumbnails"]["high"]["url"],
                "duration" : int(parse_duration(result["contentDetails"]["duration"]).total_seconds() // 60),
                "title" : result["snippet"]["title"],
            }
            videos.append(video_data)

    return render_template("index.html", videos=videos)



@main.route('/login')
def login():
    google = oauth.create_client('google')
    redirect_uri = url_for('authorize', _external=True)
    return google.authorize_redirect(redirect_uri)

@main.route('/authorize')
def authorize():
    google = oauth.create_client('google')
    token = google.authorize_access_token()
    resp = google.get('userinfo')
    resp.raise_for_status()
    user_info = resp.json()
    # do something with the token and profile
    session['email'] = user_info['email']
    return redirect('/')
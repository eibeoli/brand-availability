from flask import Flask, render_template, request
import requests

# RESOURCES
# https://code.visualstudio.com/docs/python/tutorial-flask
# https://stackoverflow.com/questions/13607278/html5-restricting-input-characters


app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/name", methods=["POST"])
def scraper():
    url = request.form['textbox']
    tumblr = requests.get(f'https://{url}.tumblr.com')
    insta = requests.get(f'https://www.instagram.com/{url}')
    reddit = requests.get(f'http://www.reddit.com/u/{url}')
    github = requests.get(f'https://www.github.com/{url}')

    name_list = {tumblr:'tumblr', insta:'instagram', reddit: 'reddit', github: 'github'}
    avail = []
    not_avail = []

    for n in name_list:
        if n.status_code == 200:
            not_avail.append(name_list[n])
        elif n.status_code == 404:
            avail.append(name_list[n])
        else:
            print(f'{url}: Status Code {n.status_code}')
    return render_template("name.html", url = url, avail = avail, len_a = len(avail), not_avail = not_avail, len_na = len(not_avail))

from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/name', methods=['POST', 'GET'])
def scraper():
    url = request.form['textbox']
    tumblr = requests.get(f'https://{url}.tumblr.com')
    insta = requests.get(f'https://www.instagram.com/{url}')
    reddit = requests.get(f'http://www.reddit.com/u/{url}')
    twitch = requests.get(f'https://www.twitch.tv/{url}')
    twitter = requests.get(f'https://www.twitter.com/{url}')
    tiktok = requests.get(f'https://www.tiktok.com/@{url}')

    name_list = {tumblr:'tumblr', insta:'instagram', reddit: 'reddit', twitch: 'twitch', twitter:'twitter', tiktok: 'tiktok'}
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
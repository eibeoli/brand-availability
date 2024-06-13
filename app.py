from flask import Flask, render_template, request, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

def search_phrase_in_webpage(response, phrases):
    content = response.text
    soup = BeautifulSoup(content, 'html.parser')
    text = soup.get_text()
    found_phrases = {phrase: phrase in text for phrase in phrases}
    return found_phrases

@app.route('/name', methods=['POST', 'GET'])
def scraper():
    url = request.form['textbox']
    # social
    tumblr = requests.get(f'https://{url}.tumblr.com')
    insta = requests.get(f'https://www.instagram.com/{url}')
    reddit = requests.get(f'http://www.reddit.com/u/{url}')
    twitch = requests.get(f'https://www.twitch.tv/{url}')
    twitter = requests.get(f'https://www.twitter.com/{url}')
    tiktok = requests.get(f'https://www.tiktok.com/@{url}')

    name_list = {tumblr:'tumblr', insta:'instagram', reddit: 'reddit', twitch: 'twitch', twitter:'twitter', tiktok: 'tiktok'}
    phrases = ["sorry", "couldn't find this account", "isn't available", "doesn't exist", "is unavailable", "nobody on Reddit goes by that name"]
    avail = []
    not_avail = []

    for response, platform_name in name_list.items():
            if response.status_code == 200:
                phraselist = search_phrase_in_webpage(response, phrases)
                print(phraselist)
                if any(phraselist.values()):
                    avail.append(platform_name)
                else:
                    not_avail.append(platform_name)
            elif response.status_code == 404:
                avail.append(platform_name)
            else:
                print(f'{url}: Status Code {response.status_code}')

    return render_template("name.html", url=url, avail=avail, len_a=len(avail), not_avail=not_avail, len_na=len(not_avail))
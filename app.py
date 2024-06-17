from flask import Flask, render_template, request, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

def search_phrase_in_webpage(response, phrases, name):
    content = response.text
    soup = BeautifulSoup(content, 'html.parser')
    text = soup.get_text()

    # Open a file in write mode ('w')
    #with open(f'{name}_text.txt', 'w', encoding='utf-8') as file:
    # Write the text content to the file
    #    file.write(text)

    #print("Text saved to extracted_text.txt")
    found_phrases = {phrase: phrase in text for phrase in phrases}
    return found_phrases

@app.route('/name', methods=['POST', 'GET'])
def scraper():
    url = request.form['textbox']
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    
    name_list = {
        'tumblr': f'https://{url}.tumblr.com',
        'instagram': f'https://www.instagram.com/{url}',
        'reddit': f'http://www.reddit.com/u/{url}',
        'twitch': f'https://www.twitch.tv/{url}',
        'twitter': f'https://www.twitter.com/{url}',
        'tiktok': f'https://www.tiktok.com/@{url}'
    }
    phrases = ["sorry", "couldn't find this account", "isn't available", "doesn't exist", "is unavailable", "Sorry, nobody on Reddit goes by that name."]
    avail = []
    not_avail = []

    for platform_name, platform_url in name_list.items():
        try:
            response = requests.get(platform_url, headers=headers, timeout=10)
            if response.status_code == 200:
                phraselist = search_phrase_in_webpage(response, phrases, platform_name)
                print(f'Checking {platform_name} at {platform_url}')
                print(f'Page content length: {len(response.text)}')
                print(f'Found phrases: {phraselist}')
                
                if any(phraselist.values()):
                    avail.append(platform_name)
                else:
                    not_avail.append(platform_name)
            elif response.status_code == 404:
                avail.append(platform_name)
                print('Not taken.')
            else:
                print(f'{platform_name}: Status Code {response.status_code}')
        except requests.RequestException as e:
            print(f"Error while requesting {platform_name}: {e}")

    return render_template("name.html", url=url, avail=avail, len_a=len(avail), not_avail=not_avail, len_na=len(not_avail))

if __name__ == '__main__':
    app.run(debug=True)
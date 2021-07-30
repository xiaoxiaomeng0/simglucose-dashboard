from bs4 import BeautifulSoup
from flask import Flask, request, render_template
import requests


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/suggestions')
def suggestions():
    text = request.args.get('jsdata')

    suggestions_list = []

    if text:
        r = requests.get(
            'http://suggestqueries.google.com/complete/search?output=toolbar&hl=ru&q={}&gl=in'.format(text))

        soup = BeautifulSoup(r.content, 'html.parser')

        suggestions = soup.find_all('suggestion')

        for suggestion in suggestions:
            suggestions_list.append(suggestion.attrs['data'])

        # print(suggestions_list)

    return render_template('suggestions.html', suggestions=suggestions_list)


if __name__ == '__main__':
    app.run(debug=True, port=5002)

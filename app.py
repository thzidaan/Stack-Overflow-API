from flask import Flask, json, render_template, request, redirect
import requests
import json
import time

app = Flask(__name__)

# (1615523017 - 1614918217) (i.e March 11 - March 4 ==> 1 week)
seven_days_time = 604800
current_Time = int(time.time())  # Gets Current Time
# Sets from date for the API request
week_earlier_time = str(current_Time - seven_days_time)

# post_id == question_id --> Remember
# Use Search API

post_endpoint = 'https://api.stackexchange.com/2.2/posts'  # Will be used for comments
question_endpoint = 'https://api.stackexchange.com/2.2/questions'

search_base_endpoint = 'https://api.stackexchange.com/2.2/search'


most_voted_endpoint = '?pagesize=10&fromdate=' + week_earlier_time + \
    '&order=desc&sort=votes&site=stackoverflow&filter=!0VdjgcAdM-31Pt4LHr5ojF5Bm&tagged='
most_recent_endpoint = '?pagesize=10&order=desc&sort=creation&site=stackoverflow&filter=!0VdjgcAdM-31Pt4LHr5ojF5Bm&tagged='


Qmost_voted_endpoint = '?pagesize=10&fromdate=' + \
    week_earlier_time + '&order=asc&sort=votes&site=stackoverflow'
Qmost_recent_endpoint = '?pagesize=10&order=asc&sort=creation&site=stackoverflow&tagged='


questionCollection = {}

allDataCollection = {}


@app.route('/search', methods=['POST'])
def search():

    tag_selected = request.form["tag"]

    most_voted_search = search_base_endpoint + most_voted_endpoint + tag_selected
    most_recent_search = search_base_endpoint + most_recent_endpoint + tag_selected

    most_voted_request = requests.get(most_voted_search)
    most_recent_request = requests.get(most_recent_search)

    votes_data = json.loads(most_voted_request.content)
    recent_data = json.loads(most_recent_request.content)

    all_request_data = [
        votes_data,
        recent_data
    ]

    for request_type in all_request_data:
        # If there is Questions returned in requests
        if request_type.get('items') is not None:
            total_question_items = request_type['items']

            for item in total_question_items:
                allDataCollection[item['question_id']] = {
                    'title': item['title'],
                    'score': item['score'],
                    'creation_date': item['creation_date'],
                    'body': item['body_markdown'],
                    'comments': {},
                    'answers': {}
                }

    return render_template('test.html', votes_data=votes_data)


@ app.route('/')
def index():
    return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True)

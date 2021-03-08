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

    votes_data = dict(json.loads(most_voted_request.content))
    recent_data = dict(json.loads(most_recent_request.content))

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
                if item.get('comments') is not None:
                    # If the question has comments
                    total_question_comment_item = item['comments']
                    for question_comment_item in total_question_comment_item:
                        allDataCollection[item['question_id']] = {
                            'comments': {
                                'creation_date': question_comment_item['creation_date'],
                                'score': question_comment_item['score'],
                                'body': question_comment_item['body_markdown']

                            }
                        }
                if item.get('answers') is not None:     # If the question have answers
                    total_answer_items = item['answers']
                    for answer_item in total_answer_items:
                        allDataCollection[item['question_id']] = {
                            'answers': {
                                'creation_date': answer_item['creation_date'],
                                'score': answer_item['score'],
                                'body': answer_item['body_markdown'],
                                'comments': {}
                            }
                        }

                        # If the answer itself have comments
                        if answer_item.get('comments') is not None:
                            total_answer_comment_item = answer_item['comments']
                            for answer_comment_item in total_answer_comment_item:
                                allDataCollection[item['question_id']] = {
                                    'answers': {
                                        'comments': {
                                            'creation_date': answer_comment_item['creation_date'],
                                            'score': answer_comment_item['score'],
                                            'body': answer_comment_item['body_markdown']

                                        }
                                    }
                                }

    return render_template('test.html', votes_data=votes_data, recent_data=recent_data, totalQ=allDataCollection)


@app.route('/search2', methods=['POST'])
def search2():

    tag_selected = request.form["tag"]

    most_voted_posts = question_endpoint + most_voted_endpoint + tag_selected
    most_recent_posts = question_endpoint + most_recent_endpoint + tag_selected

    most_voted_request = requests.get(most_voted_posts)
    most_recent_request = requests.get(most_recent_posts)

    votes_data = dict(json.loads(most_voted_request.content))
    recent_data = dict(json.loads(most_recent_request.content))
    total_questions = dict(votes_data, **recent_data)

    total_question_items = total_questions['items']

    for item in total_question_items:
        questionCollection[item['question_id']] = {  # question_id will help us find corresponding comments
            'title': item['title'],
            'votes': item['score'],
            'creation_date': item['creation_date']
        }

    return render_template('search.html', data=questionCollection)


@ app.route('/')
def index():
    return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True)

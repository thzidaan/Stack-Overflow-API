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


# comment = {
#     'creation_data': '',
#     'score': '',
#     'body': ''
# }
# answer = {
#     'creation_data': '',
#     'score': '',
#     'body': '',
#     'comments': comments_collection
# }

# question = {
#     'title': '',
#     'score': '',
#     'creation_date': '',
#     'body': '',
#     'comments': comments_collection,
#     'answers': answers_collection
# }


@app.route('/search', methods=['POST'])
def search():

    tag_selected = request.form["tag"]

    # comments_collection = []
    # answers_collection = []
    questions_collection = []

    most_voted_search = search_base_endpoint + most_voted_endpoint + tag_selected
    most_recent_search = search_base_endpoint + most_recent_endpoint + tag_selected

    most_voted_request = requests.get(most_voted_search).json()
    most_recent_request = requests.get(most_recent_search).json()

    # votes_data = json.loads(most_voted_request.content)
    # recent_data = json.loads(most_recent_request.content)

    # all_request_data = [
    #     votes_data,
    #     recent_data
    # ]

    all_request_data = [
        most_voted_request,
        most_recent_request
    ]

    for request_item in all_request_data:
        print('requesstNOTDone')
        if request_item.get('items') is not None:
            print('requesstDone')
            all_data = request_item.get('items')
            print('AllDataDone')
            for item_list in range(len(request_item['items'])):
                print('Done Item Loop' + str(item_list))
                current_question = request_item['items'][item_list]
                print('got current question asked')
                new_question = ({
                    'title': current_question['title'],
                    'creation_date': current_question['creation_date']
                })
                questions_collection.append(new_question)
                print('got current question got')
            # if (all_data[item_list].get('answers')) is not None:
            # # We get all the answers for the current question
            # all_answers_data = all_data[item_list]['answers']
            # for answer_list in range(len(all_answers_data)):
            #     answer_item = all_answers_data[answer_list]
            # # If answer also have comments
            #     if (all_answers_data[answer_list].get('comments')) is not None:
            #         answer_item_comments = all_answers_data[answer_list]['comments']
            #         for answer_comment_list in range(len(answer_item_comments)):
            #             # Taking each comment from answers
            #             answer_comment_item = answer_item_comments[answer_comment_list]
            #             comments_collection.append({
            #                 'creation_date': answer_comment_item['creation_date'],
            #                 'score': answer_comment_item['score'],
            #                 'body': answer_comment_item['body_markdown']
            #             })

            #     answers_collection.append({
            #         'creation_date': answer_item['creation_date'],
            #         'score': answer_item['score'],
            #         'body': answer_item['body_markdown'],
            #         'comments': comments_collection
            #     })

  #  votesDataitem = votes_data['items'][0]['answers']  # [0]['comments'][0]

    return render_template('test.html', data=questions_collection)


@ app.route('/')
def index():
    return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True)

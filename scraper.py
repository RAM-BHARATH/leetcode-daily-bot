import requests
from bs4 import BeautifulSoup
import json
# impor pymongo

URL = "https://leetcode.com/problemset/"

class Question:
        def __init__(self, question_data):
            self.title = question_data['question']['title']
            self.id = question_data['question']['questionFrontendId']
            self.link = 'https://leetcode.com/'+question_data['link']
            self.date = question_data['date']

        def __str__(self):
            return f"{self.date} - {self.title}, {self.link}"

def fetch_question():
    res = requests.get(URL)
    soup = BeautifulSoup(res.text, 'html.parser')
    print('running scrapper...')
    # print(res.text)
    # print(soup.find(id='__NEXT_DATA__'))
    next_data = soup.find(id='__NEXT_DATA__')
    next_data = next_data.get_text()
    next_data = json.loads(next_data)
    # print(next_data)
    todays_challenge = next_data['props']['pageProps']['dehydratedState']['queries'][-1]['state']['data']['dailyCodingChallengeV2']['challenges'][-1]
    # print(todays_challenge)

    question = Question(todays_challenge)
    print(question)

    # output 
    with open("question.json", 'w') as f:
        json.dump(question.__dict__, f)
        
    # Closing file
    f.close()

if __name__ == '__main__':
    fetch_question()
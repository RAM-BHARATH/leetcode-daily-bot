import requests
from bs4 import BeautifulSoup
import json
# import pymongo

URL = "https://leetcode.com/problemset/"


class Question:

  def __init__(self, question_data):
    self.title = question_data['question']['title']
    self.id = question_data['question']['questionFrontendId']
    self.link = 'https://leetcode.com' + question_data['link']
    self.date = question_data['date']

  def __str__(self):
    return f"{self.date} - {self.title}, {self.link}"


def fetch_question():
  # print('fetch question')
  # res = requests.get(URL)
  # soup = BeautifulSoup(res.text, 'html.parser')
  # print('running scrapper...')
  # # print(res.text)
  # # print(soup.find(id='__NEXT_DATA__'))
  # next_data = soup.find(id='__NEXT_DATA__')
  # next_data = next_data.get_text()
  # next_data = json.loads(next_data)
  # # print(next_data)
  # todays_challenge = next_data['props']['pageProps']['dehydratedState'][
  #     'queries'][-1]['state']['data']['dailyCodingChallengeV2']['challenges'][
  #         -1]
  # # print(todays_challenge)

  query = '''{dailyCodingChallengeV2(year: 2024, month: 1) {  challenges {
        date
        userStatus
        link      
        question {        
            questionFrontendId        title        titleSlug      
            }    
        }
    }}'''

    # '''{dailyCodingChallengeV2(year: 2024, month: 1) {  challenges {
    #     date
    #     userStatus
    #     link      
    #     question {        
    #         questionFrontendId        title        titleSlug      
    #         }    
    #     }    
    #     weeklyChallenges {      
    #         date      
    #         userStatus     
    #         link     
    #         question {        
    #             questionFrontendId       
    #             title        
    #             titleSlug      
    #             isPaidOnly     
    #         }   
    #     }  
    # }}'''
  res = requests.post(URL+'graphql', json={'query': query})
  todays_challenge = res['data']['dailyCodingChallengeV2']['challenge'][-1]


  question = Question(todays_challenge)
  print(question)

  # output
  with open("question.json", 'w') as f:
    json.dump(question.__dict__, f)

  # Closing file
  f.close()
  return question.__dict__


if __name__ == '__main__':
  fetch_question()

import json
from datetime import datetime, timezone
from zoneinfo import ZoneInfo
import scraper

with open('question.json') as f:
    question = json.load(f)
    if(question=={} or question==""):
    # print(json.load(f))
        date = datetime.now(tz=ZoneInfo('Asia/Kolkata'))
        print(date.date())
        if(date.date()==question['date']):
            print(question)
        else:
            scraper.fetch_question()
    else:
        scraper.fetch_question()


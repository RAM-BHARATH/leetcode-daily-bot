from discord.ext import commands, tasks
from dotenv import load_dotenv
import discord
import os
import asyncio
from datetime import datetime, timedelta, timezone, time
import scraper
import json
from keep_alive import keep_alive
import pytz

intents = discord.Intents.all()
load_dotenv()
TOKEN = os.environ.get('TOKEN', 3)
CHANNEL_ID = int(os.environ.get('CHANNEL_ID', 3))

UTC = +timedelta(hours=5, minutes=30)
MORNING = time(11, 34, 0)

# bot = commands.Bot(command_prefix="/", intents=intents)
# zone = ZoneInfo('Asia/Kolkata')
target_time = "12:10"

target_timezone = pytz.timezone('Asia/Kolkata')

# Get the current time in the target time zone
current_time = datetime.now(target_timezone).time()

# Convert the target time (in the target time zone) to a datetime object
target_time_parts = list(map(int, target_time.split(":")))
target_datetime = target_timezone.localize(
    datetime(datetime.now().year,
             datetime.now().month,
             datetime.now().day, target_time_parts[0], target_time_parts[1]))


async def wait_until_tomorrow():
  now = datetime.utcnow() + UTC
  tomorrow = datetime.combine(now.date() + timedelta(days=1), time(0))
  # Seconds until tomorrow (midnight)
  seconds = (tomorrow - now).total_seconds()
  # Sleep until tomorrow and then the loop will start a new iteration
  await asyncio.sleep(seconds)


class MyClient(discord.Client):

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)

  async def setup_hook(self) -> None:
    # create the background task and run it in the background
    self.bg_task = self.loop.create_task(self.my_background_task())

  async def on_ready(self):
    print(f'Logged in as {self.user} (ID: {self.user.id})')
    # setup_hook()
    print('------')

  async def read(self):
    print('Enters read - 1')
    with open('question.json', 'r+') as f:
      question = json.load(f)
      print("question: " + str(question))
      if (len(question.keys())!=0 and question != "{}"):
        print("Enters question not empty")
        # print(json.load(f))
        date = datetime.now(tz=target_timezone)
        print(date.date())
        if (date == target_datetime):
          print("equal")
        else:
          print(date, target_datetime)
          print("ne")
        return question
        # if (question != None and date.date() == datetime.strptime(question['date'],
        #                                      '%Y-%m-%d').date()):
        #   # print(question)
        #   return question
      #   else:
      #     return scraper.fetch_question()
      # else:
      #   return scraper.fetch_question()

  async def my_background_task(self):
    await self.wait_until_ready()
    question = await self.read()
    # if (question == "Falsey"):
    #   question = await self.read()
    date = datetime.now(tz=target_timezone)
    if (date.date() != datetime.strptime(question['date'], '%Y-%m-%d').date()):
      question = scraper.fetch_question()
      channel = self.get_channel(CHANNEL_ID)  # channel ID goes here
      # while not self.is_closed():
        # question += 1
      # now = datetime.utcnow() + UTC
      # target_time = datetime.combine(now.date(), MORNING)
      
      # print("Hey", )
      # if(now > target_time):
      if(date.date() == datetime.strptime(question['date'], '%Y-%m-%d').date()):
        print("Sending")
        await channel.send(str(question))
          # break
          
        # seconds_until_target = (target_time - now).total_seconds()
        # await wait_until_tomorrow()
        # await asyncio.sleep(seconds_until_target)  # task runs every 60 seconds
        # await asyncio.sleep(30)
        # await self.read()

    # question = 0


keep_alive()
client = MyClient(intents=discord.Intents.default())

client.run(TOKEN)

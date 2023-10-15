from discord.ext import commands, tasks
from dotenv import load_dotenv
import discord
import os
import asyncio
from datetime import datetime, timezone
from zoneinfo import ZoneInfo
import scraper
import json
# from keep_alive import keep_alive

intents = discord.Intents.all()
load_dotenv()
TOKEN = os.environ.get('TOKEN', 3)
CHANNEL_ID = int(os.environ.get('CHANNEL_ID', 3))


bot = commands.Bot(command_prefix="/", intents=intents)


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
      print('Enters read')
      with open('question.json', 'r+') as f:
          question = json.load(f)
          if(question!={} or question!=""):
          # print(json.load(f))
              date = datetime.now(tz=ZoneInfo('Asia/Kolkata'))
              print(date.date())
              if(date.date()==datetime.strptime(question['date'], '%Y-%m-%d').date()):
                  print(question)
                  return question
              else:
                  return scraper.fetch_question()
          else:
              return scraper.fetch_question()

    async def my_background_task(self):
        await self.wait_until_ready()
        question = await self.read()
        if(question=="Falsey"):
          question = await self.read()
        else:
          channel = self.get_channel(CHANNEL_ID)  # channel ID goes here
          while not self.is_closed():
              # question += 1
              await channel.send(str(question))
              await asyncio.sleep(86400)  # task runs every 60 seconds
          
        # question = 0

client = MyClient(intents=discord.Intents.default())
client.run(TOKEN)

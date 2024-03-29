import os
import re
import requests
import json
import utils.json_loader
import discord

from discord import Embed
from datetime import datetime, timezone
from discord.ext import tasks, commands
from helpers.config import EVENTS_CHANNEL, EVENTS_ROLE, VATADR_BLUE, GUILD_ID
from dotenv import load_dotenv

airports = utils.json_loader.read_json("airports")
events_api_url = "https://my.vatsim.net/api/v1/events/all"

events_cs = []

class Events():
    def __init__(self, title, description, start_time, end_time, picture, link):
        self.title = title
        self.description = description
        self.start_time = start_time
        self.end_time = end_time
        self.picture = picture
        self.link = link

    def get_title(self):
        return self.title
    def get_description(self):
        return self.description
    def get_start_time(self):
        return self.start_time
    def get_end_time(self):
        return self.end_time
    def get_picture(self):
        return self.picture
    def get_link(self):
        return self.link

class EventsAnnouncement(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.events_posting.start()

    def cog_unload(self):
        self.events_posting.cancel()


    @tasks.loop(minutes=10)
    async def events_posting(self):
        events_2_obj = []
        events_2_cs = []
        events_data = requests.get(events_api_url).json()
        resp = json.dumps(events_data)
        s = json.loads(resp)
        for item in s['data']:
            #Check if any of our airports from Config is in json
            for airport in item['airports']:
                if airport['icao'] in airports:
                    description = item['short_description']
                    title = item['name']
                    start_time = datetime.strptime(item["start_time"], "%Y-%m-%dT%H:%M:%S.%fZ")
                    end_time = datetime.strptime(item["end_time"], "%Y-%m-%dT%H:%M:%S.%fZ")
                    picture = item['banner']
                    event_link = item['link']
                    

                    #Clean event description from HTML tags
                    clean = re.compile('<.*?>')
                    event_desc = re.sub(clean, '', description)
                    if start_time.date() == datetime.today().date():
                        if (start_time.hour - datetime.utcnow().hour) <=2:
                            events_obj = Events(title, event_desc, start_time, end_time, picture, event_link)
                            events_2_obj.append(events_obj)
                            events_2_cs.append(title)
                    else:
                        pass

        for i in events_2_obj:
            if i.get_title() not in events_cs:
                events_cs.append(i.get_title())
                embed = Embed(
                    title=f"{i.get_title()}",
                    description=f"{i.get_description()}",
                    color= VATADR_BLUE,
                    url=i.get_link(),
                    timestamp=i.get_start_time()
                )
                event_start_time = i.get_start_time()
                start = event_start_time.strftime("%H:%M")
                embed.set_image(url=i.get_picture())
                embed.set_footer(
                    text=f'Starting time:',
                    icon_url='https://twemoji.maxcdn.com/v/latest/72x72/1f551.png'
                )
                channel = self.bot.get_channel(EVENTS_CHANNEL)
                message=f"<@&{EVENTS_ROLE}>\n:calendar_spiral: New event has been scheduled!"
                await channel.send(message, embed=embed)

                        
                    #Check if event is finished and remove it from memory
        for i in events_cs:
            if end_time.day < datetime.now().day:
                events_cs.remove(i)
                channel = self.bot.get_channel(EVENTS_CHANNEL)
                try:
                    message = await channel.fetch_message(channel.last_message_id)
                    await message.delete()
                except:
                    print(f"Did not find message id!")
                    return
                
    
    @events_posting.before_loop
    async def before_events_posting(self):
        await self.bot.wait_until_ready()

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} cog has been loaded.\n-----")

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(
        EventsAnnouncement(bot),
        guilds= [discord.Object(id=GUILD_ID)]
    )

import discord
import requests
import time
import json
from helpers.config import GUILD_ID, ATC_CHANNEL
import utils.json_loader

from discord import Embed
from discord.ext import tasks, commands
from datetime import datetime, timezone, date, timedelta


callsign_prefix = utils.json_loader.read_json("callsign_prefix")
positions = ["GND","TWR","APP","CTR"]
online_cs = []

class Controller():
    def __init__(self, callsign, controller_name, frequency):
        self.callsign = callsign
        self.controller_name = controller_name
        self.frequency = frequency
    def get_callsign(self):
        return self.callsign
    def get_controller_name(self):
        return self.controller_name
    def get_frequency(self):
        return self.frequency

class atcAnnoucements(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.atcAnnoucements.start()

    def cog_unload(self):
        self.atcAnnoucements.cancel()
    
    @tasks.loop(minutes=5)
    async def atcAnnoucements(self):
        try:
            online_2_cs = []
            online_2_obj = []
            r = requests.get('https://data.vatsim.net/v3/vatsim-data.json').json()
            f = json.dumps(r)
            y = json.loads(f)
            controllers = y['controllers']
            for a in controllers:
                callsign = a['callsign']
                controller_name = a['name']
                frequency = a['frequency']
                time_logon = a['logon_time']
                time_log = time_logon[:19]
                logon = datetime.strptime(time_log, '%Y-%m-%dT%H:%M:%S')
                time_logg = logon.strftime('%H:%M')

                for i in callsign_prefix:
                    if i == callsign[:len(i)] and callsign[-3:] in positions:
                        controller_obj = Controller(callsign, controller_name, frequency)
                        online_2_obj.append(controller_obj)
                        online_2_cs.append(callsign)
            for i in online_2_obj:
                if i.get_callsign() not in online_cs:
                    #Check if controller is connected on primary frequency before continuing the loop
                    if i.get_frequency() == "199.998":
                        pass

                    else:
                        #Controller Online
                        online_cs.append(i.get_callsign())
                        onlineEmbed = Embed(title="ATC Announcement", description="New ATC just logged in!", color=0x00ff4c)
                        onlineEmbed.add_field(name=":id: Callsign", value=f"`{i.get_callsign()}`", inline=False)
                        onlineEmbed.add_field(name=":man: Controller", value=f"`{i.get_controller_name()}`", inline=False)
                        onlineEmbed.add_field(name=":radio: Frequency", value=f"`{i.get_frequency()}`", inline=False)
                        onlineEmbed.set_footer(text=f"Logged on at: {time_logg}z")
                        channel = self.bot.get_channel(ATC_CHANNEL)
                        await channel.send(embed=onlineEmbed)

            #Controller Offline
            for i in online_cs:
                if i not in online_2_cs:
                    online_cs.remove(i)
                    offlineEmbed = Embed(title="ATC Announcement", description=f":x: `ATC Logged off! Hope to see you soon` :x:", color=0xff9500)
                    offlineEmbed.add_field(name=":id: Callsign", value=f"{i}", inline=True)
                    channel = self.bot.get_channel(int(ATC_CHANNEL))
                    await channel.send(embed=offlineEmbed)
        except:
            pass

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} cog has been loaded\n-----")
        
async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(
        atcAnnoucements(bot),
        guilds= [discord.Object(id=GUILD_ID)]
    )
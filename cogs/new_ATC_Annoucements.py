from discord import Embed
from discord.ext.commands import Cog
from discord.ext import tasks
from datetime import datetime, timezone, date, timedelta
import requests
import time
import json

with open("callsign_prefix.json") as json_file:
    callsign_prefix = json.load(json_file)
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

class atcAnnoucements(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.atcAnnoucements.start()

    def cog_unload(self):
        self.atcAnnoucements.cancel()
    
    @tasks.loop(minutes=5)
    async def atcAnnoucements(self):
        try:
            channel = self.bot.get_channel(806457781032714280)
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
                        await channel.send(embed=onlineEmbed)

            #Controller Change
            for i in online_cs:
                if i.get_controller_name() not in online_cs:
                    online_cs.append(i.get_controller_name())
                    changeEmbed = Embed(title="ATC Annoucement", description=f"Controller Changed at {i.get_callsign()}!", color=0x00ff4c)
                    changeEmbed.add_field(name=":man: New Controller", value=f"{i.get_controller_name()}", inline=False)
                    changeEmbed.set_footer(text=f"Logged on at: {time_logg}z")
                    await channel.send(embed=changeEmbed)



            #Controller Offline
            for i in online_cs:
                if i not in online_2_cs:
                    online_cs.remove(i)
                    offlineEmbed = Embed(title="ATC Announcement", description=f"`ATC Logged off! Hope to see you soon`", color=0xff9500)
                    offlineEmbed.add_field(name=":id: Callsign", value=f"{i}", inline=True)
                    await channel.send(embed=offlineEmbed)
        except:
            pass
    @Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} cog has been loaded\n-----")
def setup(bot):
    bot.add_cog(atcAnnoucements(bot))
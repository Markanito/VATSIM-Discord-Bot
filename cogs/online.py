from discord import Embed
from discord.ext.commands import Cog, command
import requests
import json

with open("callsign_prefix.json") as json_file:
    callsign_prefix = json.load(json_file)
#callsign_prefix = json.loads(open("callsign_prefix.json").read())
positions = ["GND","TWR","APP","CTR"]

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

class online(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(name="online", description="Display online controllers.")
    async def online(self, ctx):
        t = requests.get('https://data.vatsim.net/v3/vatsim-data.json').json()
        xy = json.dumps(t)
        s = json.loads(xy)
        online_exists = False
        for item in s['controllers']:
            callsign = item['callsign']
            frequency = item['frequency']
            controller_name = item['name']

            for i in callsign_prefix:
                if i == callsign[:len(i)] and callsign[-3:] in positions:
                    controller_obj = Controller(callsign, controller_name, frequency)
                    online_exists = True
                    embed = Embed(colour=0x4c00ff)

                    embed.set_author(name='VATAdria Online ATC')
                    embed.add_field(name=':man: Controller',value=f"{controller_name}",inline=False)
                    embed.add_field(name=':id: Position', value=f"{callsign}", inline=False)
                    embed.add_field(name=':radio: Frequency', value=f"{frequency}", inline=False)

                    await ctx.send( embed=embed)
        if not online_exists:
            noEmbed = Embed(description=":x: We couldn't find any controllers online at the moment. :x:", color=0xff0000)
            await ctx.send(embed=noEmbed)
   
    @Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} cog has been loaded\n-----")
def setup(bot):
    bot.add_cog(online(bot))
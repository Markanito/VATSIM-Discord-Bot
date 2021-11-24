from discord import Embed, Colour
import json
import xml.etree.ElementTree as ET
from discord.ext.commands.cooldowns import BucketType
from discord.ext.commands.core import command, Cog, cooldown
import requests
from datetime import datetime, timezone, date, time

#atc = json.loads(open("atc_positions.json").read())
with open("callsign_prefix.json") as json_file:
    callsign_prefix = json.load(json_file)
positions = ["GND","TWR","APP","CTR"]


class Controller():
    def __init__(self, callsign, booked):
        self.callsign = callsign
        self.booked = booked
    def get_callsign(self):
        return self.callsign
    def get_booked(self):
        return self.booked

class bookings(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(name="bookings", brief="Display all bookings.")
    @cooldown(2, 60, BucketType.user)
    async def bookings(self, ctx):
        tree = ET.fromstring(requests.get('http://vatbook.euroutepro.com/xml2.php?fir=').text)
        bookings_exists = False
        for atcs in tree.find('atcs'):
            callsign = atcs.find('callsign').text
            time_start = atcs.find('time_start').text
            time_end = atcs.find('time_end').text
            booked = atcs.find('name').text
            booking_start = datetime.strptime(time_start, '%Y-%m-%d %H:%M:%S')
            booking_end = datetime.strptime(time_end, '%Y-%m-%d %H:%M:%S')

            for i in callsign_prefix:
                    if i == callsign[:len(i)] and callsign[-3:] in positions:
                        if (booking_start.day - datetime.now().day) == 0:
                            controller_obj = Controller(callsign, booked)
                            bookings_exists = True
                            #Time Builder, do not mess with the lines below
                            booking_start_month = booking_start.month
                            booking_start_day = booking_start.day
                            booking_start_hour = booking_start.hour
                            booking_start_minute = booking_start.minute
                            booking_end_hour = booking_end.hour
                            booking_end_minute = booking_end.minute

                            if booking_start_month < 10:
                                booking_start_month = f'0{booking_start_month}'
                            if  booking_start_day < 10:
                                booking_start_day = f'0{booking_start_day}'
                            if booking_start_hour < 10:
                                booking_start_hour = f'0{booking_start_hour}'
                            if booking_start_minute < 10:
                                booking_start_minute = f'0{booking_start_minute}'
                            if booking_end_hour <10:
                                booking_end_hour = f'0{booking_end_hour}'
                            if booking_end_minute <10:
                                booking_end_minute = f'0{booking_end_minute}'

                            if booking_start > datetime.now():
                                bokembed = Embed(title="VATAdria Bookings", description="\n\n", colour = Colour.dark_red())
                                bokembed.add_field(name=':radio: Position', value=f"`{(callsign)}`", inline=False)
                                bokembed.add_field(name=':date: Date', value=f"`{booking_start_day}.{booking_start_month}.{booking_start.year}`", inline=False)
                                bokembed.add_field(name=":timer: Start Time", value=f"`{booking_start_hour}:{booking_start_minute}z`", inline=False)
                                bokembed.add_field(name=':timer: End Time', value=f"`{booking_end_hour}:{booking_end_minute}z`", inline=False)
                                bokembed.set_footer(
                                    text =f"Booked by: {booked}"
                                )
                                await ctx.send(embed=bokembed)
                            else:
                                pass
        if not bookings_exists:
            noEmbed = Embed(description=":x: Sorry, couldn't find any bookings :x:", color=0xff0000)
            await ctx.send(embed=noEmbed)
    @Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} cog has been loaded\n-----")
def setup(bot):
    bot.add_cog(bookings(bot))
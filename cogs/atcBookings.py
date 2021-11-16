import discord
from discord.ext import tasks
from discord.ext.commands import command, Cog
import json
import xml.etree.ElementTree as ET
import requests
from datetime import datetime, timezone, date, time

with open("callsign_prefix.json") as json_file:
    callsign_prefix = json.load(json_file)
positions = ["GND","TWR","APP","CTR"]
booked_cs = []

class Controller():
    def __init__(self, callsign, booked, bookings_start, bookings_end):
        self.callsign = callsign
        self.booked = booked
        self.bookings_start = bookings_start
        self.bookings_end = bookings_end
    def get_callsign(self):
        return self.callsign
    def get_booked(self):
        return self.booked
    def get_bookings_start(self):
        return self.bookings_start
    def get_bookings_end(self):
        return self.bookings_end

class atcBookings(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.newBooking.start()

    def cog_unload(self):
        self.newBooking.cancel()

    @tasks.loop(minutes=1)
    async def newBooking(self):
        try:
            channel = self.bot.get_channel(781834455765483562)
            booked_2_cs = []
            booked_2_obj = []
            tree = ET.fromstring(requests.get('http://vatbook.euroutepro.com/xml2.php?fir=').text)
            for atcs in tree.find('atcs'):
                callsign = atcs.find('callsign').text
                time_start = atcs.find('time_start').text
                time_end = atcs.find('time_end').text
                booked = atcs.find('name').text
                booking_start = datetime.strptime(time_start, '%Y-%m-%d %H:%M:%S')
                booking_end = datetime.strptime(time_end, '%Y-%m-%d %H:%M:%S')
                bookings_start_time = booking_start.strftime('%H:%M')
                bookings_end_time = booking_end.strftime('%H:%M')
                
                for i in callsign_prefix:
                    if i == callsign[:len(i)] and callsign[-3:] in positions:
                        if (booking_start.day - datetime.now().day) == 0:
                            controller_obj = Controller(callsign, booked, bookings_start_time, bookings_end_time)
                            booked_2_obj.append(controller_obj)
                            booked_2_cs.append(callsign)
                        else:
                            pass

            #Check if new booking has been made
            for i in booked_2_obj:
                if i.get_callsign() not in booked_cs:
                    booked_cs.append(i.get_callsign())
                    bokembed = discord.Embed(title="VATAdria Booking Annoucement", description="New booking found for today!", colour = discord.Colour.dark_red())
                    bokembed.add_field(name=':radio: Position', value=f"`{i.get_callsign()}`", inline=False)
                    bokembed.add_field(name=":timer: Start Time", value=f"`{i.get_bookings_start()}z`", inline=False)
                    bokembed.add_field(name=':timer: End Time', value=f"`{i.get_bookings_end()}z`", inline=False)
                    bokembed.set_footer(
                        text =f"Booked by: {i.get_booked()}"
                        )
                    await channel.send(embed=bokembed)

            #Check if booking is removed!
            for i in booked_cs:
                if i not in booked_2_cs:
                    booked_cs.remove(i)
                    bookremove = discord.Embed(name="VATAdria Booking Annoucement", description=f"ATC Booking was removed!", color=0xff9500)
                    bookremove.add_field(name=":id: Callsign", value=f"{i}", inline=True)
                    await channel.send(embed=bookremove)
        except:
            pass

    @Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} cog has been loaded\n-----")

def setup(bot):
    bot.add_cog(atcBookings(bot))
#Welcome to VATSIM Discord Bot designed by VATAdria. This bot display online ATC, departures, arrivals and future bookings. 
#Modify code with correct data in order for bot to work correctly
#Author: Marko Tomicic (VATAdria Training Director)
#If you have any questions feel free to contact me at: marko.tomicic@vatadria.net or over Discord: Markan#4169
#I will make updates to this code once when new fatures get implemented so keep an eye on updates!
#If you want you can modify this code and if you come up with good function please share it with everyone
#Future features including: Filter arrival and departure data by ICAO, implement METAR command (decoded metar will be added), automatic online ATC messages once when member
#open station and when it closes!

import discord
import requests
import asyncio
import json
import math
import discord.utils
import datetime
import xml.etree.ElementTree as ET
from datetime import datetime, timezone, date, time
from discord.ext import commands, tasks
from discord.ext.commands import Bot
from discord.utils import get
from itertools import cycle

# Define all clients and constants for code calls
client = discord.Client()
token = open("token.txt", "r").read() #open token.txt and enter your bot token. Without this bot will not be able to work. 
ROLE = "Member" #You can change this to whatever you want in order for bot to assign role when member joins the server!
url = "https://api.checkwx.com/metar/" #Metar URL DO NOT CHANGE THIS
rule= "/decoded?pretty=1" #rule for decoded METAR data DO NOT CHANGE THIS!
status = cycle(["with VASTIM Data", "what can I show you?", "Type !commands for help"]) #You can change this or disable it if you don't want to change status over time!
airport = ["ICAO1", "ICAO2"] #Replace ICAO with ICAO code of airports in your FIR or vACC so bot can look up only listed airports

atc = ["XXXX_CTR", "XXXX_APP", "XXXX_TWR", "XXXX_GND", "XXXX_DEL", "XXXX_DEP"] #Replace this with all stations callsign (include any prefix for stations so bot can look it up and not ignore it)

# On bot run evet, it will console log log in message and set automatic status on Discord to "Watching for new controllers!"
@client.event
async def on_ready():
    change_status.start()
    #await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="VATSIM Data!")) #remove # before await in order to activate only 1 discord acitivity 
    print('We have logged in as {0.user}'.format(client))

# Welcomes new members into the server. Modify member.send command to send custom DM to members who join your discord server. Include some rules and link 
# that might be usefull for members who are joining. 
@client.event
async def on_member_join(member):
  role = get(member.guild.roles, name=ROLE)
  await member.add_roles(role)
  await member.send(f'''{member.mention} Welcome to the official VATSIM Adria Discord! \nPlease read following rules: \n1) Use your First and Last name as your Discord nickname \n2) Post text messages in correct text channel or they will be removed! \n3) Do not post piracy or pornographical links \n4) Any religious, political or national debate is forbiden! \n\nOn behalf of VATSIM Adria we wish you a warm welcome to our small community! \nCheck us out on social media! \nFacebook: https://www.facebook.com/VATSIMAdria \nInstagram: https://www.instagram.com/vatadria \nTwitter:https://twitter.com/VATSIM_Adria \nWebsite: http://www.vatadria.net/''')
  channel = client.get_channel(706609609900687430) #Add channel ID where you want to bot to announce who joined the server! Disable default server notifications in order to prevent spam
  await channel.send(f'''{member.mention} just joined the server.''')

#user ban message
@client.event
async def on_member_ban(guild, member):
    channel = client.get_channel(706609609900687430)
    await channel.send(f'''{member.name} has been banned from the server.''')

@client.event
async def on_member_remove(member):
    channel = client.get_channel(706609609900687430)
    await channel.send(f'''{member.name} just left the server.''')

# You can remove this if you want to use only 1 status 
@tasks.loop(minutes=10)
async def change_status():
    await client.change_presence(activity=discord.Game(next(status)))

#This is where all magic happens. Modify it as needed in order to make bot to work correctly. Math and functions are tested and working
@client.event
async def on_message(message, user: discord.User = None):
    if message.author == client.user:
        return

    #bookings display data
    tree = ET.fromstring(requests.get('http://vatbook.euroutepro.com/xml2.php?fir=').text)
    #API Key for METAR API
    hdr = { 'X-API-Key': 'Your-Api-Key-Goes-Here' }
    # send request to vatsim data
    t = requests.get('http://cluster.data.vatsim.net/vatsim-data.json').json()
    xy = json.dumps(t)
    s = json.loads(xy)
    # Bookins Data Display
    utc = datetime.now(timezone.utc)
    # Command for displaying ATC online
    if message.content.startswith('!online'):
        online_exists = False
        for item in s['clients']:
            if item['callsign'] in atc:
                online_exists = True
                embed = discord.Embed(colour = discord.Colour.purple()) #replace purple with any colour you want

                embed.set_author(name='Online ATC')
                embed.add_field(name='Controller',value=item['realname'],inline=False)
                embed.add_field(name='Position', value=item['callsign'], inline=False)
                embed.add_field(name='Frequency', value=item['frequency'], inline=False)

                await message.channel.send( embed=embed)
        if not online_exists:
            await message.channel.send('```There is no ATC Online at the moment! Use !bookings to check ATC bookings for today or !allbookings to check all ATC bookings in future!```')
    
    #Display future bookings. 
    if message.content.startswith('!bookings'):
        bookings_exists = False
        for atcs in tree.find('atcs'):
            callsign = atcs.find('callsign').text
            time_start = atcs.find('time_start').text
            time_end = atcs.find('time_end').text
            booking_start = datetime.strptime(time_start, '%Y-%m-%d %H:%M:%S')
            booking_end = datetime.strptime(time_end, '%Y-%m-%d %H:%M:%S')
            if (booking_start.day - datetime.today.day()) == 0 and callsign in atc:
                bookings_exists = True
                if booking_start.minute <10 and booking_end.minute <10 and booking_end.month <10:
                    boke = discord.Embed(colour = discord.Colour.dark_red())
                    boke.set_author(name='ATC Bookings')
                    boke.add_field(name='Position', value=f"{(callsign)}", inline=False)
                    boke.add_field(name='Date', value=f"{booking_start.day}.0{booking_start.month}.{booking_start.year}", inline=False)
                    boke.add_field(name="Start Time", value=f"{booking_start.hour}:0{booking_start.minute}z", inline=False)
                    boke.add_field(name='End Time', value=f"{booking_end.hour}:0{booking_end.minute}z", inline=False)
                    await message.channel.send(embed=boke)
                else: 
                    boke1 = discord.Embed(colour = discord.Colour.dark_red())
                    boke1.set_author(name='ATC Bookings')
                    boke1.add_field(name='Position', value=f"{(callsign)}", inline=False)
                    boke1.add_field(name='Date', value=f"{booking_start.day}.{booking_start.month}.{booking_start.year}", inline=False)
                    boke1.add_field(name="Start Time", value=f"{booking_start.hour}:{booking_start.minute}z", inline=False)
                    boke1.add_field(name='End Time', value=f"{booking_end.hour}:{booking_end.minute}z", inline=False)
                    await message.channel.send(embed=boke1)
        if not bookings_exists:
            await message.channel.send('```No ATC bookings found.```')

    if message.content.startswith('!allbookings'):
        bookings_exists = False
        for atcs in tree.find('atcs'):
            callsign = atcs.find('callsign').text
            time_start = atcs.find('time_start').text
            time_end = atcs.find('time_end').text
            booking_start = datetime.strptime(time_start, '%Y-%m-%d %H:%M:%S')
            booking_end = datetime.strptime(time_end, '%Y-%m-%d %H:%M:%S')
            if callsign in atc:
                bookings_exists = True
                if booking_start.minute <10 and booking_end.minute <10 and booking_start.month <10:
                    boka = discord.Embed(colour = discord.Colour.dark_red())
                    boka.set_author(name='ATC Bookings')
                    boka.add_field(name='Position', value=f"{(callsign)}", inline=False)
                    boka.add_field(name='Date', value=f"{booking_start.day}.0{booking_start.month}.{booking_start.year}", inline=False)
                    boka.add_field(name="Start Time", value=f"{booking_start.hour}:0{booking_start.minute}z", inline=False)
                    boka.add_field(name='End Time', value=f"{booking_end.hour}:0{booking_end.minute}z", inline=False)
                    await message.channel.send(embed=boka)
                else:
                    boka1 = discord.Embed(colour = discord.Colour.dark_red())
                    boka1.set_author(name='ATC Bookings')
                    boka1.add_field(name='Position', value=f"{(callsign)}", inline=False)
                    boka1.add_field(name='Date', value=f"{booking_start.day}.{booking_start.month}.{booking_start.year}", inline=False)
                    boka1.add_field(name="Start Time", value=f"{booking_start.hour}:{booking_start.minute}z", inline=False)
                    boka1.add_field(name='End Time', value=f"{booking_end.hour}:{booking_end.minute}z", inline=False)
                    await message.channel.send(embed=boka1)
        if not bookings_exists:
            await message.channel.send('```No ATC bookings found.```')

    if message.content.startswith('!arrivals'):
        ad = message.content[10:]
        if ad in airport:
            xy = json.dumps(t)
            s = json.loads(xy)
            arrivals_exist = False
            for item in s['clients']:
                if item['planned_destairport'] == ad:
                    arrivals_exist = True

                    lan = 0.0
                    long = 0.0
                    # Positions of the airports (LAT and LONG)
                    if item['planned_destairport'] == "XXXX":#REPLACE ALL XXXX WITH CORRECT AIRPORT ICAO
                        lan = 42.561389 #REPLACE THIS WITH CORRECT POSITION IN ORDER TO GET CORRECT ETA CALCULATIONS
                        long = 18.268333
                    elif item['planned_destairport'] == "XXXX":
                        lan = 44.819444
                        long = 20.306944
                    elif item['planned_destairport'] == "XXXX":
                        lan = 45.743056
                        long = 16.068889
                    elif item['planned_destairport'] == "XXXX":
                        lan = 44.108333
                        long = 15.346667
                    elif item['planned_destairport'] == "XXXX":
                        lan = 44.89361
                        long = 13.922222
                    elif item['planned_destairport'] == "XXXX":
                        lan = 43.538889
                        long = 16.298056
                    elif item['planned_destairport'] == "XXXX":
                        lan = 45.462778
                        long = 18.810278
                    elif item['planned_destairport'] == "XXXX":
                        lan = 45.216944
                        long = 14.570278
                    elif item['planned_destairport'] == "XXXX":
                        lan = 46.224444
                        long = 14.456111
                    elif item['planned_destairport'] == "XXXX":
                        lan = 46.479722
                        long = 15.686111
                    elif item['planned_destairport'] == "XXXX":
                        lan = 45.473353
                        long = 13.614978
                    elif item['planned_destairport'] == "XXXX":
                        lan = 42.359444
                        long = 19.251944
                    elif item['planned_destairport'] == "XXXX":
                        lan = 45.147778
                        long = 21.309722
                    elif item['planned_destairport'] == "XXXX":
                        lan = 42.404722
                        long = 18.723333
                    elif item['planned_destairport'] == "XXXX":
                        lan = 43.337222
                        long = 21.853611
                    elif item['planned_destairport'] == "XXXX":
                        lan = 43.818611
                        long = 20.585278
                    elif item['planned_destairport'] == "XXXX":
                        lan = 43.898886
                        long = 19.697683
                    elif item['planned_destairport'] == "XXXX":
                        lan = 41.961111
                        long = 21.626944
                    elif item['planned_destairport'] == "XXXX":
                        lan = 41.18
                        long = 20.742222
                    elif item['planned_destairport'] == "XXXX":
                        lan = 41.414722
                        long = 19.720556
                    elif item['planned_destairport'] == "XXXX":
                        lan = 43.824722
                        long = 18.331389
                    elif item['planned_destairport'] == "XXXX":
                        lan = 43.282778
                        long = 17.845833
                    elif item['planned_destairport'] == "XXXX":
                        lan = 44.936111
                        long = 17.299167
                    elif item['planned_destairport'] == "XXXX":
                        lan = 44.458611
                        long = 18.724722
                    elif item['planned_destairport'] == "XXXX":
                        lan = 42.572778
                        long = 21.035833

                    # calculations

                    lat1 = item['latitude'] * math.pi / 180
                    lat2 = lan * math.pi / 180
                    lon1 = item['longitude'] * math.pi / 180
                    lon2 = long * math.pi / 180

                    dlat = lat2 - lat1
                    dlon = lon2 - lon1

                    R = (6371 * 1000) / 1852
                    a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2) * math.sin(dlon/2)

                    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

                    distance = R * c

                    if item['groundspeed'] < 70:
                        if distance < 10:
                            departures_exist = True
                            arr1e1 = discord.Embed(colour = discord.Colour.green())
                            arr1e1.set_author(name="VATAdria Arrivals")
                            arr1e1.add_field(name="Callsign", value=item['callsign'], inline=False)
                            arr1e1.add_field(name="Departure Airport", value=item['planned_depairport'], inline=False)
                            arr1e1.add_field(name="Destination Airport", value=item['planned_destairport'], inline=False)
                            arr1e1.add_field(name="Status", value="Arrived at destination", inline=False)
                            arr1e1.add_field(name="Route", value=item['planned_route'], inline=False)
                            await message.channel.send(embed=arr1e1)
                        else:
                            arr2e2 = discord.Embed(colour = discord.Colour.dark_gold())
                            arr2e2.set_author(name="VATAdria Arrivals")
                            arr2e2.add_field(name="Callsign", value=item['callsign'], inline=False)
                            arr2e2.add_field(name="Departure Airport", value=item['planned_depairport'], inline=False)
                            arr2e2.add_field(name="Destination Airport", value=item['planned_destairport'], inline=False)
                            arr2e2.add_field(name="Status", value="Preparing for the flight", inline=False)
                            arr2e2.add_field(name="Route", value=item['planned_route'], inline=False)
                            await message.channel.send(embed=arr2e2)
                    else:
                        time = distance / item['groundspeed']

                        hour = int(time)
                        arrival_hour = utc.hour + hour
                        arrival_minute = utc.minute + int((time - int(time))*60)
                        if arrival_minute > 59:
                            add_hour = int(arrival_minute / 60)
                            arrival_minute = int(((arrival_minute / 60) - add_hour) * 60)
                            arrival_hour = arrival_hour + add_hour
                            if arrival_hour > 23:
                                days = int(arrival_hour / 24)
                                arrival_hour = (arrival_hour - (days * 24))
                                if days == 1:
                                    if arrival_minute < 10:
                                        arr3e3 = discord.Embed(colour = discord.Colour.blue())
                                        arr3e3.set_author(name="VATAdria Arrivals")
                                        arr3e3.add_field(name="Callsign", value=item['callsign'], inline=False)
                                        arr3e3.add_field(name="Departure Airport", value=item['planned_depairport'], inline=False)
                                        arr3e3.add_field(name="Destination Airport", value=item['planned_destairport'], inline=False)
                                        arr3e3.add_field(name="Status", value="On the way", inline=False)
                                        arr3e3.add_field(name="Arrival Time", value=f"{arrival_hour}:0{arrival_minute}z tommorow", inline=False)
                                        arr3e3.add_field(name="Route", value=item['planned_route'], inline=False)
                                        await message.channel.send(embed=arr3e3)
                                    else:
                                        arr4e4 = discord.Embed(colour = discord.Colour.blue())
                                        arr4e4.set_author(name="VATAdria Arrivals")
                                        arr4e4.add_field(name="Callsign", value=item['callsign'], inline=False)
                                        arr4e4.add_field(name="Departure Airport", value=item['planned_depairport'], inline=False)
                                        arr4e4.add_field(name="Destination Airport", value=item['planned_destairport'], inline=False)
                                        arr4e4.add_field(name="Status", value="On the way", inline=False)
                                        arr4e4.add_field(name="Arrival Time", value=f"{arrival_hour}:{arrival_minute}z tommorow", inline=False)
                                        arr4e4.add_field(name="Route", value=item['planned_route'], inline=False)
                                        await message.channel.send(embed=arr4e4)
                                else:
                                    if arrival_minute < 10:
                                        arr5e5 = discord.Embed(colour = discord.Colour.blue())
                                        arr5e5.set_author(name="VATAdria Arrivals")
                                        arr5e5.add_field(name="Callsign", value=item['callsign'], inline=False)
                                        arr5e5.add_field(name="Departure Airport", value=item['planned_depairport'], inline=False)
                                        arr5e5.add_field(name="Destination Airport", value=item['planned_destairport'], inline=False)
                                        arr5e5.add_field(name="Status", value="On the way", inline=False)
                                        arr5e5.add_field(name="Arrival Time", value=f"{days}:{arrival_hour}:0{arrival_minute}z", inline=False)
                                        arr5e5.add_field(name="Route", value=item['planned_route'], inline=False)
                                        await message.channel.send(embed=arr5e5)
                                    else:
                                        arr6e6 = discord.Embed(colour = discord.Colour.blue())
                                        arr6e6.set_author(name="VATAdria Arrivals")
                                        arr6e6.add_field(name="Callsign", value=item['callsign'], inline=False)
                                        arr6e6.add_field(name="Departure Airport", value=item['planned_depairport'], inline=False)
                                        arr6e6.add_field(name="Destination Airport", value=item['planned_destairport'], inline=False)
                                        arr6e6.add_field(name="Status", value="On the way", inline=False)
                                        arr6e6.add_field(name="Arrival Time", value=f"{days}:{arrival_hour}:{arrival_minute}z", inline=False)
                                        arr6e6.add_field(name="Route", value=item['planned_route'], inline=False)
                                        await message.channel.send(embed=arr6e6)
                        if arrival_minute < 10:
                                        arr7e7 = discord.Embed(colour = discord.Colour.blue())
                                        arr7e7.set_author(name="VATAdria Arrivals")
                                        arr7e7.add_field(name="Callsign", value=item['callsign'], inline=False)
                                        arr7e7.add_field(name="Departure Airport", value=item['planned_depairport'], inline=False)
                                        arr7e7.add_field(name="Destination Airport", value=item['planned_destairport'], inline=False)
                                        arr7e7.add_field(name="Status", value="On the way", inline=False)
                                        arr7e7.add_field(name="Arrival Time", value=f"{arrival_hour}:0{arrival_minute}z", inline=False)
                                        arr7e7.add_field(name="Route", value=item['planned_route'], inline=False)
                                        await message.channel.send(embed=arr7e7)
                        else:
                                        arr8e8 = discord.Embed(colour = discord.Colour.blue())
                                        arr8e8.set_author(name="VATAdria Arrivals")
                                        arr8e8.add_field(name="Callsign", value=item['callsign'], inline=False)
                                        arr8e8.add_field(name="Departure Airport", value=item['planned_depairport'], inline=False)
                                        arr8e8.add_field(name="Destination Airport", value=item['planned_destairport'], inline=False)
                                        arr8e8.add_field(name="Status", value="On the way", inline=False)
                                        arr8e8.add_field(name="Arrival Time", value=f"{arrival_hour}:{arrival_minute}z", inline=False)
                                        arr8e8.add_field(name="Route", value=item['planned_route'], inline=False)
                                        await message.channel.send(embed=arr8e8)

            if not arrivals_exist:
                await message.channel.send('**There is no arrivals at the moment!**')
        else:
            await message.channel.send('**Please provide ICAO code within VATAdria!**')

    # Display arrivals to all airports
    if message.content.startswith('!allarrivals'):
        arrivals_exist = False
        for item in s['clients']:
            if item['planned_destairport'] in airport:
                arrivals_exist = True

                lan = 0.0
                long = 0.0
                # Positions of the airports (LAT and LONG)
                if item['planned_destairport'] == "XXXX": #REPLACE ALL XXXX WITH CORRECT AIRPORT ICAO
                    lan = 42.561389 #REPLACE THIS WITH CORRECT POSITION IN ORDER TO GET CORRECT ETA CALCULATIONS
                    long = 18.268333 
                elif item['planned_destairport'] == "XXXX":
                    lan = 44.819444
                    long = 20.306944
                elif item['planned_destairport'] == "XXXX":
                    lan = 45.743056
                    long = 16.068889
                elif item['planned_destairport'] == "XXXX":
                    lan = 44.108333
                    long = 15.346667
                elif item['planned_destairport'] == "XXXX":
                    lan = 44.893611
                    long = 13.922222
                elif item['planned_destairport'] == "XXXX":
                    lan = 43.538889
                    long = 16.298056
                elif item['planned_destairport'] == "XXXX":
                    lan = 45.462778
                    long = 18.810278
                elif item['planned_destairport'] == "XXXX":
                    lan = 45.216944
                    long = 14.570278
                elif item['planned_destairport'] == "XXXX":
                    lan = 46.224444
                    long = 14.456111
                elif item['planned_destairport'] == "XXXX":
                    lan = 46.479722
                    long = 15.686111
                elif item['planned_destairport'] == "XXXX":
                    lan = 45.473353
                    long = 13.614978
                elif item['planned_destairport'] == "XXXX":
                    lan = 42.359444
                    long = 19.251944
                elif item['planned_destairport'] == "XXXX":
                    lan = 45.147778
                    long = 21.309722
                elif item['planned_destairport'] == "XXXX":
                    lan = 42.404722
                    long = 18.723333
                elif item['planned_destairport'] == "XXXX":
                    lan = 43.337222
                    long = 21.853611
                elif item['planned_destairport'] == "XXXX":
                    lan = 43.818611
                    long = 20.585278
                elif item['planned_destairport'] == "XXXX":
                    lan = 43.898886
                    long = 19.697683
                elif item['planned_destairport'] == "XXXX":
                    lan = 41.961111
                    long = 21.626944
                elif item['planned_destairport'] == "XXXX":
                    lan = 41.18
                    long = 20.742222
                elif item['planned_destairport'] == "XXXX":
                    lan = 41.414722
                    long = 19.720556
                elif item['planned_destairport'] == "XXXX":
                    lan = 43.824722
                    long = 18.331389
                elif item['planned_destairport'] == "XXXX":
                    lan = 43.282778
                    long = 17.845833
                elif item['planned_destairport'] == "XXXX":
                    lan = 44.936111
                    long = 17.299167
                elif item['planned_destairport'] == "XXXX":
                    lan = 44.458611
                    long = 18.724722
                elif item['planned_destairport'] == "XXXX":
                    lan = 42.572778
                    long = 21.035833

                # calculations

                lat1 = item['latitude'] * math.pi / 180
                lat2 = lan * math.pi / 180
                lon1 = item['longitude'] * math.pi / 180
                lon2 = long * math.pi / 180

                dlat = lat2 - lat1
                dlon = lon2 - lon1

                R = (6371 * 1000) / 1852
                a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2) * math.sin(dlon/2)

                c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

                distance = R * c

                if item['groundspeed'] < 70:
                    if distance < 10:
                        departures_exist = True
                        arr1e = discord.Embed(colour = discord.Colour.green())
                        arr1e.set_author(name="Arrivals")
                        arr1e.add_field(name="Callsign", value=item['callsign'], inline=False)
                        arr1e.add_field(name="Departure Airport", value=item['planned_depairport'], inline=False)
                        arr1e.add_field(name="Destination Airport", value=item['planned_destairport'], inline=False)
                        arr1e.add_field(name="Status", value="Arrived at destination", inline=False)
                        arr1e.add_field(name="Route", value=item['planned_route'], inline=False)
                        await message.channel.send(embed=arr1e)
                    else:
                        arr2e = discord.Embed(colour = discord.Colour.dark_gold())
                        arr2e.set_author(name="Arrivals")
                        arr2e.add_field(name="Callsign", value=item['callsign'], inline=False)
                        arr2e.add_field(name="Departure Airport", value=item['planned_depairport'], inline=False)
                        arr2e.add_field(name="Destination Airport", value=item['planned_destairport'], inline=False)
                        arr2e.add_field(name="Status", value="Preparing for the flight", inline=False)
                        arr2e.add_field(name="Route", value=item['planned_route'], inline=False)
                        await message.channel.send(embed=arr2e)
                else:
                    time = distance / item['groundspeed']

                    hour = int(time)
                    arrival_hour = utc.hour + hour
                    arrival_minute = utc.minute + int((time - int(time))*60)
                    if arrival_minute > 59:
                        add_hour = int(arrival_minute / 60)
                        arrival_minute = int(((arrival_minute / 60) - add_hour) * 60)
                        arrival_hour = arrival_hour + add_hour
                        if arrival_hour > 23:
                            days = int(arrival_hour / 24)
                            arrival_hour = (arrival_hour - (days * 24))
                            if days == 1:
                                if arrival_minute < 10:
                                    arr3e = discord.Embed(colour = discord.Colour.blue())
                                    arr3e.set_author(name="Arrivals")
                                    arr3e.add_field(name="Callsign", value=item['callsign'], inline=False)
                                    arr3e.add_field(name="Departure Airport", value=item['planned_depairport'], inline=False)
                                    arr3e.add_field(name="Destination Airport", value=item['planned_destairport'], inline=False)
                                    arr3e.add_field(name="Status", value="On the way", inline=False)
                                    arr3e.add_field(name="Arrival Time", value=f"{arrival_hour}:0{arrival_minute}z tommorow", inline=False)
                                    arr3e.add_field(name="Route", value=item['planned_route'], inline=False)
                                    await message.channel.send(embed=arr3e)
                                else:
                                    arr4e = discord.Embed(colour = discord.Colour.blue())
                                    arr4e.set_author(name="Arrivals")
                                    arr4e.add_field(name="Callsign", value=item['callsign'], inline=False)
                                    arr4e.add_field(name="Departure Airport", value=item['planned_depairport'], inline=False)
                                    arr4e.add_field(name="Destination Airport", value=item['planned_destairport'], inline=False)
                                    arr4e.add_field(name="Status", value="On the way", inline=False)
                                    arr4e.add_field(name="Arrival Time", value=f"{arrival_hour}:{arrival_minute}z tommorow", inline=False)
                                    arr4e.add_field(name="Route", value=item['planned_route'], inline=False)
                                    await message.channel.send(embed=arr4e)
                            else:
                                if arrival_minute < 10:
                                    arr5e = discord.Embed(colour = discord.Colour.blue())
                                    arr5e.set_author(name="Arrivals")
                                    arr5e.add_field(name="Callsign", value=item['callsign'], inline=False)
                                    arr5e.add_field(name="Departure Airport", value=item['planned_depairport'], inline=False)
                                    arr5e.add_field(name="Destination Airport", value=item['planned_destairport'], inline=False)
                                    arr5e.add_field(name="Status", value="On the way", inline=False)
                                    arr5e.add_field(name="Arrival Time", value=f"{days}:{arrival_hour}:0{arrival_minute}z", inline=False)
                                    arr5e.add_field(name="Route", value=item['planned_route'], inline=False)
                                    await message.channel.send(embed=arr5e)
                                else:
                                    arr6e = discord.Embed(colour = discord.Colour.blue())
                                    arr6e.set_author(name="Arrivals")
                                    arr6e.add_field(name="Callsign", value=item['callsign'], inline=False)
                                    arr6e.add_field(name="Departure Airport", value=item['planned_depairport'], inline=False)
                                    arr6e.add_field(name="Destination Airport", value=item['planned_destairport'], inline=False)
                                    arr6e.add_field(name="Status", value="On the way", inline=False)
                                    arr6e.add_field(name="Arrival Time", value=f"{days}:{arrival_hour}:{arrival_minute}z", inline=False)
                                    arr6e.add_field(name="Route", value=item['planned_route'], inline=False)
                                    await message.channel.send(embed=arr6e)
                    if arrival_minute < 10:
                                    arr7e = discord.Embed(colour = discord.Colour.blue())
                                    arr7e.set_author(name="Arrivals")
                                    arr7e.add_field(name="Callsign", value=item['callsign'], inline=False)
                                    arr7e.add_field(name="Departure Airport", value=item['planned_depairport'], inline=False)
                                    arr7e.add_field(name="Destination Airport", value=item['planned_destairport'], inline=False)
                                    arr7e.add_field(name="Status", value="On the way", inline=False)
                                    arr7e.add_field(name="Arrival Time", value=f"{arrival_hour}:0{arrival_minute}z", inline=False)
                                    arr7e.add_field(name="Route", value=item['planned_route'], inline=False)
                                    await message.channel.send(embed=arr7e)
                    else:
                                    arr8e = discord.Embed(colour = discord.Colour.blue())
                                    arr8e.set_author(name="Arrivals")
                                    arr8e.add_field(name="Callsign", value=item['callsign'], inline=False)
                                    arr8e.add_field(name="Departure Airport", value=item['planned_depairport'], inline=False)
                                    arr8e.add_field(name="Destination Airport", value=item['planned_destairport'], inline=False)
                                    arr8e.add_field(name="Status", value="On the way", inline=False)
                                    arr8e.add_field(name="Arrival Time", value=f"{arrival_hour}:{arrival_minute}z", inline=False)
                                    arr8e.add_field(name="Route", value=item['planned_route'], inline=False)
                                    await message.channel.send(embed=arr8e)

        if not arrivals_exist:
            await message.channel.send('**There is no arrivals at the moment!**')

#Display filtered airport data keep in mind I placed filter to only allow aiports in aiport data, you can remove it if you want!
    if message.content.startswith('!departures'):
        ad1 = message.content[12:]
        if ad1 in airport:
            departures_exist = False
            for item in s['clients']:
                if item['planned_depairport'] == ad1:
                    departures_exist = True
                    depe = discord.Embed(colour = discord.Colour.green())
                    depe.set_author(name="VATAdria Departures")
                    depe.add_field(name="Callsign", value=item['callsign'], inline=False)
                    depe.add_field(name="Departure Airport", value=item['planned_depairport'], inline=False)
                    depe.add_field(name="Destination Airport", value=item['planned_destairport'], inline=False)
                    depe.add_field(name="Planned Dep Time", value=f"{item['planned_deptime']}z", inline=False)
                    depe.add_field(name="Route", value=item['planned_route'], inline=False)
                    await message.channel.send(embed=depe)
            if not departures_exist:
                await message.channel.send('**There is no departures at the moment!**')
        else:
            await message.channel.send('**Please provide ICAO code within XXXXXX**')
# Display all departures from all airports 
    if message.content.startswith('!departures'):
        departures_exist = False
        for item in s['clients']:
            if item['planned_depairport'] in airport:
                departures_exist = True
                depe = discord.Embed(colour = discord.Colour.green())
                depe.set_author(name="Departures")
                depe.add_field(name="Callsign", value=item['callsign'], inline=False)
                depe.add_field(name="Departure Airport", value=item['planned_depairport'], inline=False)
                depe.add_field(name="Destination Airport", value=item['planned_destairport'], inline=False)
                depe.add_field(name="Planned Dep Time", value=f"{item['planned_deptime']}z", inline=False)
                depe.add_field(name="Route", value=item['planned_route'], inline=False)
                await message.channel.send(embed=depe)
        if not departures_exist:
            await message.channel.send('**There is no departures at the moment!**')

    # sector file
    if message.content.startswith('!sectorfile'):
                sece = discord.Embed(title="Sector File", url="http://files.aero-nav.com/", colour = discord.Colour.red()) #Add correct link in url section to send members to correct sector file site!
                sece.set_author(name="Sector File")
                sece.add_field(name="Description", value="Download sector files for EuroScope and VRC", inline=False)
                sece.add_field(name="EuroScope Instalation", value="If you are installing EuroScope Download install package", inline=False)
                sece.add_field(name="EuroScope Update", value="If you are updating from previous Airac cycle, download update package", inline=False)
                sece.add_field(name="VRC Installation and Update", value="You have only one option here and download XXXX VRC Package", inline=False)
                await message.channel.send(embed=sece)
              
    
    # all commands for discord bot, this will send list of all commands you have so if you change any command make sure to replace it here as well!
    if message.content.startswith('!commands'):
        come = discord.Embed(title="Commands", description ="**List of all commands for bot**", colour = discord.Colour.orange())
        come.set_author(name="VATAdria")
        come.add_field(name="Show online ATC", value="**!online**", inline=False,)
        come.add_field(name="Show all arrivals", value="**!arrivals**", inline=False)
        come.add_field(name="Show all departures", value="**!departures**", inline=False)
        come.add_field(name="Display future ATC bookings", value="**!allbookings**", inline=False)
        come.add_field(name="Display ATC bookings for today", value="**!bookings**", inline=False)
        come.add_field(name="Sector file link", value="**!sectorfile**", inline=False)
        come.add_field(name="Bot version", value="**!ver**", inline=False)
        come.add_field(name="Changelog", value="**!changelog**", inline=False)
        come.add_field(name="Contact", value="**!contact**", inline=False)
        await message.channel.send(embed=come)

    # Displays server time. You can run this bot free on heroku so you can check the server time if you get calculations wrong. This is more of testing command so if you want you can disable it!
    if message.content.startswith('!utc'):
        await message.channel.send(f"```Current UTC time: {utc.hour}:{utc.minute}```") 

    # version
    if message.content.startswith('!ver'):
        await message.channel.send(f"```Current Version: ¨X.X```") #you can remove this. I use this for checking bot updates

    #Changelog
    if message.content.startswith("!changelog"): #I implemented this in order to let member know what changed in bot. You can simply remove this if you want!
        chle = discord.Embed(title="Changelog", colour = discord.Colour.dark_gold())
        chle.set_author(name="VATAdria")
        chle.add_field(name="1", value="*random comment goes here*", inline=False)
        chle.add_field(name="2", value="*random comment goes here*", inline=False)
        chle.add_field(name="3", value="*random comment goes here*", inline=False)
        chle.add_field(name="4", value="*random comment goes here*", inline=False)
        await message.channel.send(embed=chle)
    
    #Contact information
    if message.content.startswith("!contact"):
        cone = discord.Embed(title="Contact Info", colour = discord.Colour.dark_gold())
        cone.set_author(name="Contact info")
        cone.add_field(name="vACC Director", value="**INSERT VALID EMAIL ADRESS**", inline=False)
        cone.add_field(name="Training Department", value="**INSERT VALID EMAIL ADRESS**", inline=False)
        cone.add_field(name="Events", value="**INSERT VALID EMAIL ADRESS**", inline=False)
        await message.channel.send(embed=cone)

    #METAR display
    if message.content.startswith('!metar'):
        icao = message.content[7:]
        final_url = f"{url}{icao}{rule}"
        req = requests.get(final_url, headers=hdr).json()
        xi = json.dumps(req)
        d = json.loads(xi)
        for item in d['data']:
            if item['wind']['speed_kts'] < 10:
                if item['wind']['degrees'] == 0:
                    mete = discord.Embed(title="Metar Info", colour = discord.Colour.dark_gold())
                    mete.set_author(name="VATAdria")
                    mete.add_field(name="Airport", value=f"{item['station']['name']}", inline=False)
                    mete.add_field(name="Raw Metar", value=f"{item['raw_text']}", inline=False)
                    mete.add_field(name="Winds", value=f"VRB0{item['wind']['speed_kts']}KT", inline=False)
                    mete.add_field(name="Visibility", value=f"{item['visibility']['meters_float']}", inline=False)
                    mete.add_field(name="Temperature", value=f"{item['temperature']['celsius']}", inline=False)
                    mete.add_field(name="Dew Point", value=f"{item['dewpoint']['celsius']}", inline=False)
                    mete.add_field(name="QNH", value=f"{item['barometer']['hpa']}", inline=False)
                    await message.channel.send(embed=mete)
                else:
                    mete1 = discord.Embed(title="Metar Info", colour = discord.Colour.dark_gold())
                    mete1.set_author(name="VATAdria")
                    mete1.add_field(name="Airport", value=f"{item['station']['name']}", inline=False)
                    mete1.add_field(name="Raw Metar", value=f"{item['raw_text']}", inline=False)
                    mete1.add_field(name="Winds", value=f"{item['wind']['degrees']}0{item['wind']['speed_kts']}KT", inline=False)
                    mete1.add_field(name="Visibility", value=f"{item['visibility']['meters_float']}", inline=False)
                    mete1.add_field(name="Temperature", value=f"{item['temperature']['celsius']}", inline=False)
                    mete1.add_field(name="Dew Point", value=f"{item['dewpoint']['celsius']}", inline=False)
                    mete1.add_field(name="QNH", value=f"{item['barometer']['hpa']}", inline=False)
                    await message.channel.send(embed=mete1)
            else:
                mete2 = discord.Embed(title="Metar Info", colour = discord.Colour.dark_gold())
                mete2.set_author(name="VATAdria")
                mete2.add_field(name="Airport", value=f"{item['station']['name']}", inline=False)
                mete2.add_field(name="Raw Metar", value=f"{item['raw_text']}", inline=False)
                mete2.add_field(name="Winds", value=f"{item['wind']['degrees']}{item['wind']['speed_kts']}KT", inline=False)
                mete2.add_field(name="Visibility", value=f"{item['visibility']['meters_float']}", inline=False)
                mete2.add_field(name="Temperature", value=f"{item['temperature']['celsius']}", inline=False)
                mete2.add_field(name="Dew Point", value=f"{item['dewpoint']['celsius']}", inline=False)
                mete2.add_field(name="QNH", value=f"{item['barometer']['hpa']}", inline=False)
                await message.channel.send(embed=mete2)


# Login with bot on Discord!
client.run(token) 
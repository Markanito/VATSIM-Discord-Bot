import discord
import os
import json
import requests

from dotenv import load_dotenv
from distutils.util import strtobool

load_dotenv('.env')

DESCRIPTION = 'VATEye is Discord bot developed by Marko Tomicic - 1359931. This bot is only ment to be used withing VATAdria Discord server.'

VATSCA_BLUE = 0x002d68
VATADR_BLUE = 0x002d68
VATADR_RED = 0xc00000

COGS = [
    'cogs.general',
    'cogs.tasks',
    'cogs.arrivals',
    'cogs.atcBookings',
    'cogs.bookings',
    'cogs.departures',
    'cogs.metar',
    'cogs.ATCAnnouncements',
    'cogs.online',
    'cogs.presence_update',
    'cogs.events',
    'cogs.server_join',
    'cogs.role_react'
]

COGS_LOAD = {
    'admin': 'cogs.general',
    'check_members': 'cogs.tasks',
    'arrivals': 'cogs.arrivals',
    'departures': 'cogs.departures',
    'atcBookings': 'cogs.atcBookings',
    'atcAnnouncements': 'cogs.ATCAnnouncements',
    'bookings': 'cogs.bookings',
    'metar': 'cogs.metar',
    'online': 'cogs.online',
    'update_presence': 'cogs.update_presence',
    'events': 'cogs.events',
    'server_join': 'cogs.server_join',
    'role_react': 'cogs.role_reacts',
    'AutoResponse': 'cogs.AutoResponse' 
}

STAFF_ROLES = [
    'Staff',
    'Discord Admin',
    'Moderator'
]

ROLE_REASONS = {
    'vatadr_add': 'Member is now part of VATAdria',
    'vatadr_remove': 'Member is no longer part of VATAdria',
    'no_cid': 'User does not have a VATSIM ID in his/her nickname.',
    'no_auth': 'User did not authenticate via the Community Website',
    'mentor_add': 'Member is now a mentor',
    'mentor_remove': 'Member is no longer a mentor',
    'reaction_add': 'Member reacted to a message',
    'reaction_remove': 'Member removed a reaction from a message',
}

BOT_TOKEN = str(os.getenv('BOT_TOKEN'))
VATSIM_API_TOKEN = str(os.getenv('VATSIM_API_TOKEN'))
CHECKWX_API_KEY = str(os.getenv('CHECKWX_API_KEY'))

VATSIM_CHECK_MEMBER_URL = str(os.getenv('VATSIM_CHECK_MEMBER_URL'))
VATSIM_SUBDIVISION = str(os.getenv('VATSIM_SUBDIVISION'))
DIVISION_URL = str(os.getenv('DIVISION_URL'))

VATADR_MEMBER_ROLE = int(os.getenv('VATADR_MEMBER_ROLE'))
VATSIM_MEMBER_ROLE = int(os.getenv('VATSIM_MEMBER_ROLE'))
EVENTS_ROLE = int(os.getenv('EVENTS_ROLE'))
OBS_RATING_ROLE = int(os.getenv('OBS_RATING_ROLE'))
MENTOR_ROLE = int(os.getenv('MENTOR_ROLE'))

FIR_DATA = str(os.getenv('FIR_DATA')).split(',')
FIRS = []
FIR_ROLES = []
for fir in FIR_DATA:
    FIRS.append(fir.split(':')[0])
    FIR_ROLES.append(fir.split(':')[1])

AIRPORTS = str(os.getenv('AIRPORTS')).split(',')
AIRPORT = []
for airport in AIRPORTS:
    AIRPORT.append(airport)

CALLSIGN_PREFIXES = str(os.getenv('AIRPORTS')).split(',')
CALLSIGN_PREFIX = []
for callsign in CALLSIGN_PREFIXES:
    CALLSIGN_PREFIX.append(callsign)
    
    
REACTION_ROLE_DATA = str(os.getenv('REACTION_ROLE_DATA')).split(',')
REACTION_EMOJI = []
REACTION_MESSAGE_IDS = []
REACTION_ROLE_IDS = []
for reaction_role in REACTION_ROLE_DATA:
    REACTION_EMOJI.append(reaction_role.split('|')[0])
    REACTION_MESSAGE_IDS.append(reaction_role.split('|')[1])
    REACTION_ROLE_IDS.append(reaction_role.split('|')[2])

FIR_MENTORS = dict(zip(FIRS, FIR_ROLES))

REACTION_ROLES = dict(zip(REACTION_EMOJI, REACTION_ROLE_IDS))

GUILD_ID = int(os.getenv('GUILD_ID'))
STAFFING_INTERVAL = int(os.getenv('STAFFING_INTERVAL'))

CHECK_MENTORS_INTERVAL = int(os.getenv('CHECK_MENTORS_INTERVAL'))

EVENTS_CHANNEL = int(os.getenv('EVENTS_CHANNEL'))
RULES_CHANNEL = int(os.getenv('RULES_CHANNEL'))
ROLES_CHANNEL = int(os.getenv('ROLES_CHANNEL'))
ATC_CHANNEL = int(os.getenv('ATC_CHANNEL'))
BOOKINGS_CHANNEL = int(os.getenv('BOOKINGS_CHANNEL'))

BOT_CHANNEL = int(os.getenv('BOT_CHANNEL'))

CHECK_MEMBERS_INTERVAL = int(os.getenv('CHECK_MEMBERS_INTERVAL', 86400))

def status() -> discord.Status:
    return discord.Status.online

def activity() -> discord.Activity:
    data = requests.get('https://data.vatsim.net/v3/vatsim-data.json').json()
    resp = json.dumps(data)
    s = json.loads(resp)
    users = s['general']['unique_users']
    return discord.Activity(type=discord.ActivityType.watching, name=f"{users} VATSIM Users")

async def load_cogs(bot: discord.ext.commands.Bot) -> None:
    for cog in COGS:
        try:
            await bot.load_extension(cog)
        except Exception as e:
            print(f'Failed to load cog - {cog}. \n Error: {e}')

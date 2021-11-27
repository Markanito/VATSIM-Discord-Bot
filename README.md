<div id="top"></div>
<!--

[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project
VATSIM Bot Developed by Marko Tomicic (VATSIM ID: 1359931). This bot started as an idea to bring certain data from VATSIM to Discord server in order to get data you need fast and on all devices. Bot started as simple Python script and now we are in V3 with a lot of functions that seemed imposible for me to design. 

Here are features of this bot:
* ATC & Bookings Annoucements
* Arrivals & Departures
* Custom Paginated Help command
* Broadcast commands for Admins & Staff (used for Events, Annoucements, Sector files updates and news)
* Load, unload & reload entire bot without the need to restart the bot
* Decoded METAR
* Easy customatization of bot (only input data in json files there is no need to touch the code)

I spent a lot of time working on this project and experimenting with the performance and response time and I guess we are at the top of the line with this bot!

<p align="right">(<a href="#top">back to top</a>)</p>



### Built With

This bot was built with:

* [Python](https://www.python.org/)
* [Discord.py](https://github.com/Rapptz/discord.py)
* [Pytaf](https://github.com/dmbaturin/pytaf)

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started
This bot was built to be used by VATSIM vACC/ARTCC but I can't provide 1 bot you could invite to your server due to my current programming knowledge so you will need to host it on your own. I made sure you don't need to touch code at all but there will be some edditing needed in order to get this bot working.

### Prerequisites

* Visual Studio Code
* VPS (To host the bot, you can get DigitalOcean Droplet for around 5$ a motnh or host it on your own machine, Raspberry Pi, etc)


### Installation

_In order to make this bot work you follow instructions step by step!!_
_Important notice! In `cogs/reload.py` replace line 10 with proper code based on where you host your bot!_
   ```py
    COGS = [path.split("/")[-1][:-3] for path in glob("./cogs/*.py")] #Linux based systems
   ```
   with

   ```py
    COGS = [path.split("\\")[-1][:-3] for path in glob("./cogs/*.py")] #Windows based systems
   ```

1. Create your bot on [Discord Developer POrtal](https://discord.com/developers/applications), once you created your bot navigate to Bot tab and make sure all Intents are turned on! Now you can invite it to your server and give it admin privilages!
2. Get a free [CheckWX API Key](https://www.checkwxapi.com/)
3. Clone the repo
   ```sh
   git clone https://github.com/Markanito/VATSIM-Discord-Bot.git
   ```
4. Install required packages (Make sure you have Python and Pip installed beofre installing packages!)
   ```sh 
    pip install -r requirements.txt #Windows
   ```
   Or if you are on Linux based system
      ```sh
    sudo pip install -r requirements.txt #Linux
   ```
5. Enter your bot token in  `bot_config/secrets.json`
   ```py
    "token": 'ENTER YOUR TOKEN'
   ```
6. Enter roles names and channel ID's in  `bot_config/config.json` (Make sure to enable Discord Developer Mode to get text channel ID's)
   ```py
    "atc_channel": "781834455765483562",
    "bookings_channel": "781834455765483562",
    "events_channel": "692681048798265347",
    "news_channel": "781834455765483562",
    "sector_file_channel": "781834455765483562",
    "checkwx_api_key": "0b955dec24ccb45ede04524bec",
    "staff_role_name": "Staff",
    "discord_admin_role_name": "Admin",
    "moderator_role_name": "Moderator"
   ```
7. Enter airports ICAO code in `airports.json`
   ```py
    [
        "LJLJ", 
        "LJMB",
    }
   ```
8. Enter ATC Callsigns in `callsign_prefix.json`
   ```py
    [
        "LDZO", 
        "LYBA",
    }
   ```
9. Run your bot by runing `python3.10 bot.py` (_If you are running bot on Linux based server make sure you run it as root user or you may encounter errors with commands_)

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- CONTACT -->
## Contact

If you need any help setting up this bot you can always reach out to me via [VATSIM Adria Discord Server](https://discord.gg/nsBQcdY) (Username: Marko Tomicic - 1359931)

<p align="right">(<a href="#top">back to top</a>)</p>

<!---To Do-->
## To Do

There are some planned updates coming in the future which will happen soon or sometimes in future. It all depends on how much time I have on my hand to keep working on this project and ideas I have and all suggestions comming in from the rest of VATSIM community. 

Here is list of planned updates for now:
- [x] Add support for Slash commands
- [x] Pagginated arrivals & departures embeds
- [ ] Switch to Discord.py v2
- [ ] Implement VATSIM API usage



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/othneildrew/Best-README-Template.svg?style=for-the-badge
[contributors-url]: https://github.com/othneildrew/Best-README-Template/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/othneildrew/Best-README-Template.svg?style=for-the-badge
[forks-url]: https://github.com/othneildrew/Best-README-Template/network/members
[stars-shield]: https://img.shields.io/github/stars/othneildrew/Best-README-Template.svg?style=for-the-badge
[stars-url]: https://github.com/othneildrew/Best-README-Template/stargazers
[issues-shield]: https://img.shields.io/github/issues/othneildrew/Best-README-Template.svg?style=for-the-badge
[issues-url]: https://github.com/othneildrew/Best-README-Template/issues
[license-shield]: https://img.shields.io/github/license/othneildrew/Best-README-Template.svg?style=for-the-badge
[license-url]: https://github.com/othneildrew/Best-README-Template/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/othneildrew
[product-screenshot]: images/screenshot.png
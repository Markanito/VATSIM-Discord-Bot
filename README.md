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
VATSIM Bot aka VATEye Developed by Marko Tomicic (VATSIM ID: 1359931). Bring nice features to your Discord server and let your member get to know your vACC/ARTCC better! With modern Discord features, integration alongiside VATSIM bot we make your life easier! 

Here are features of this bot:
* ATC & Bookings Annoucements
* Arrivals & Departures
* Load, unload & reload entire bot without the need to restart the bot
* Decoded METAR & TAF
* Easy customatization of bot
* Automatically assign Local Member roles to your members if they are part of your Subdivision
* VATSIM Events API to post events reminders 2 hours before events
* If user DM's your bot it will reply to it (if we have an answer for it) - Still in active development

I spent a lot of time going over Nextcord, Pycord and now when Discord.py is back in development it was time to update this bot.

Big thanks to VATSIM-Scandinavia team for introducing me to Slash commands, Events posting and role assignement for users.

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
_If you wish to use feature where bot will send few messages when it joins the server make sure to edit `cogs/on_server_join.py` with all your info and messages!_
_If you wish to disable any of the features of the bot locate `helpers/config.py` and remove any cogs you don't want to use from COGS array!_
 
1. Create your bot on [Discord Developer Portal](https://discord.com/developers/applications)
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
5. Create .env file and fill in all data from example .env
6. Enter airports ICAO code in `bot_config/airports.json`
   ```py
    [
        "LJLJ", 
        "LJMB",
    }
   ```
7. Enter ATC Callsigns in `bot_config/callsign_prefix.json`
   ```py
    [
        "LDZO", 
        "LYBA",
    }
   ```
8. Run your bot by runing `python3.10 bot.py`
9. Invite your bot to your server and have fun! Make sure to grant it APPLICATION.COMMANDS scope before inviting the server or commands won't work at all!

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
- [X] Put all arrivals & all departures into single embed
- [X] Put all bookings into single embed 
- [X] Add support for Slash commands
- [X] Switch to Discord.py v2
- [X] Implement VATSIM API usage 
- [X] Implement automatic events posting
- [ ] Implement Auto Reponses for bot (few of them only working in DM)
- [ ] Completely remove bot_config folder and switch to .env



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
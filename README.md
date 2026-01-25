### ⌚ Zkylhine
Do you need an easy way to remmeber your friend's timezones?

Add and load them to a database and check them instantly on Discord.

## Current functionality
* Set and update your timezone and your friend's!
* Check the time at any given time. No message littering either, since they are only visible to yourself!
* ...wait, that's it?

## how to run locally
1. clone this repository with
`git clone https://www.github.com/JustNotSebas/Zkylhine.git` or download and unzip the repository.

2. rename .env.example to .env and set your variables

| variable            | description                                                                        | default                 | 
| ------------        | -----------                                                                        | -----------             | 
| TOKEN               | Sets the token used by py-cord to start the bot. Required.                         | ADD_YOUR_BOT_TOKEN_HERE | 
| TIMEZONE            | Sets the timezone used for time-related purposes. Uses PYTZ format. | UTC | UTC                     |
|   DB_URL | Sets the URI for MongoDB to use. No other databases are supported out of the box. | SET_YOUR_DB_URL_HERE  | 

3. run with ``python3 main.py`` or ``py main.py`` if you're on windows. no extra arguments required, as long as you have set all your variables correctly.

## Acknowledgements
The bot is designed to run on the following scenario:

- A database hosted on mongodb ([atlas is recommended)](https://www.mongodb.com/products/platform) 
- All .env variables set correctly (all are required.)
- A single bot instance running per-server

As such, any variation might have an impact on the bot's usage. For the 'intented' experience, I recommend using the bot's public instance hosted by me, [which you can find here](https://discord.com/oauth2/authorize?client_id=1397871121587634226).

No bot intents are required, and the bot runs by default with ``discord.Intents.default()``, so you only need to create a bot application in the [discord developer portal](https://discord.dev) to be able to use this bot.

I don't expect contributions but I will review and appreciate any one available.

## license
This program is released under the GNU General Public License v3.0 (GPL-3.0). You are free to use, modify or distribute it as long as your changes remain open source (if distributing) and licensed under GPL. [Click here to read the full license hosted in this repository.](LICENSE)
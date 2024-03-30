# Discord Spotify Presence Tracker Bot

This README.md provides instructions on how to set up and run the Discord Spotify Presence Tracker Bot. This bot tracks when members of a Discord server are listening to Spotify and records the songs they are listening to in a MongoDB database.

## Prerequisites

Before setting up the bot, make sure you have the following:

- Python 3.x installed on your machine.
- MongoDB installed locally or access to a remote MongoDB server.
- A Discord Developer account to create a bot and obtain a token.

## Setup Instructions

### 1. Clone the Repository

Clone this repository to your local machine using the following command:

```bash
git clone https://github.com/Josephfallen/Spotify_Scout.git
```

### 2. Install Dependencies

Navigate to the cloned directory and install the required Python packages using pip:

```
cd Spotify_Scout
pip install -r requirements.txt
```

### 3. Configure the Bot

Open the `main.py` file in a text editor and update the following configurations:

#### Discord Bot Configuration

```
# Discord bot configuration
intents = discord.Intents.default()
intents.guilds = True
intents.guild_messages = True
intents.message_content = True
intents.members = True
intents.presences = True

client = commands.Bot(command_prefix='!', intents=intents)
```

#### MongoDB Configuration

```
# MongoDB configuration
mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")  # Change if connecting to a remote MongoDB server
db = mongo_client["YOUR_DATABASE_NAME"]  # Name this whatever you like, the bot will auto-create the database
collection = db["YOUR_COLLECTION_NAME"]  # Name this whatever you like, the bot will auto-create the collection
```

#### Bot Token

Replace `'YOUR_TOKEN_HERE'` with your Discord bot token obtained from the Discord Developer Portal:

```
# Start the bot
client.run('YOUR_TOKEN_HERE')
```

### 4. Run the Bot

Execute the following command to run the bot:

```
python spotify.py
```

## Bot Commands

- `!query`: Fetches and displays the top 20 most listened to Spotify songs from the database.

## How It Works

- The bot listens for presence updates from Discord members.
- When a member is listening to Spotify, the bot records the song details (title, artist, album, track URL, etc.) in the MongoDB database.
- You can query the database to see the top 20 most listened to Spotify songs by using the `!query` command.

## Contributing

If you would like to contribute to this project, please fork the repository and submit a pull request. We welcome any contributions!

## Support
Go to the [Support server](https://discord.gg/6y2hyz9uSk) to ask questions, talk to other developers, or if you need any help!

## License

This project is licensed under the MIT License. See `LICENSE` for more information.

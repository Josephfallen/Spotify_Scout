import discord
from discord.ext import commands
import pymongo
import matplotlib.pyplot as plt

# Define intents
intents = discord.Intents.default()
intents.guilds = True
intents.guild_messages = True
intents.message_content = True
intents.members = True

client = commands.Bot(command_prefix='!', intents=intents)

# MongoDB configuration
mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")
db = mongo_client["spotify"]
collection = db["presences"]

@client.event
async def on_ready():
    print(f'Logged in as {client.user.name} ({client.user.id})')
    print("Fetching presence data from all members...")

    # Set bot status
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name='Spotify Scout'))

    for guild in client.guilds:
        for member in guild.members:
            if any(
                    activity.type == discord.ActivityType.listening and activity.name == 'Spotify Scout'
                    for activity in member.activities
            ):
                await handle_presence_update(member)

    print('Ready to query!')

@client.event
async def on_message(message):
    if message.content.startswith('!query'):
        # Aggregate and fetch the top 3 most appearing songs from the database
        pipeline = [
            {
                "$group": {
                    "_id": {
                        "track_url": "$track_url",
                        "title": "$title",
                        "artist": "$artist"
                    },
                    "count": {"$sum": 1}
                }
            },
            {
                "$sort": {"count": -1}
            },
            {
                "$limit": 3
            }
        ]
        
        top_songs = list(collection.aggregate(pipeline))
        
        # Create an embed to list the top 3 most appearing songs
        embed = discord.Embed(title="Top 3 Most Appearing Songs", color=discord.Color.blue())
        
        for idx, song in enumerate(top_songs, 1):
            embed.add_field(
                name=f"{idx}. {song['_id']['title']} - {song['_id']['artist']}",
                value=f"Track URL: {song['_id']['track_url']}\nAppearances: {song['count']}",
                inline=False
            )

        # Send the embed to the Discord channel
        await message.channel.send(embed=embed)
    print('Discord queried top 3 most appearing songs from the database')

# Placeholder function for user data insertion into MongoDB
async def insert_user_data(user, activity):
    details = activity.details
    spotify_url = details.split(" ")[-1] if details and "spotify" in details else None

    user_data = {
        'track_url': spotify_url,
        'title': details.split(" - ")[0] if details and "spotify" in details and " - " in details else None,
        'artist': details.split(" - ")[1] if details and "spotify" in details and " - " in details else None
    }
    collection.insert_one(user_data)

# Function to handle presence update
async def handle_presence_update(member):
    for activity in member.activities:
        if activity.type == discord.ActivityType.listening and activity.name == 'Spotify Scout':
            await insert_user_data(member, activity)

client.run('DISCORD_BOT_TOKEN')

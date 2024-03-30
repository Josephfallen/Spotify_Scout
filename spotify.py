import discord
from discord.ext import commands
import pymongo
import asyncio

# Discord bot configuration
intents = discord.Intents.default()
intents.guilds = True
intents.guild_messages = True
intents.message_content = True
intents.members = True
intents.presences = True

client = commands.Bot(command_prefix='!', intents=intents)

# MongoDB configuration for primary Database
mongo_client = pymongo.MongoClient("mongodb://localhost:27017/") # Change if connecting to a remote mongoDB server
db = mongo_client["YOUR_DATABASE_HERE"] # Name this what ever you would like, the bot will auto make the database
collection = db["YOUR_COLLECTION_HERE"] # Name this what ever you would like, the bot will auto make the collection

# MongoDB configuration for Second Database (this is for a the webserver, remove if not wanted (Webserver WIP)
mongo_client2 = pymongo.MongoClient("mongodb://localhost:27017/")  # Change if connecting to a remote MongoDB server
db2 = mongo_client2["DATABASE_NAME_2"]  # Replace with your database name for collection2
collection2 = db2["COLLECTION_NAME_2"]  # Replace with your collection name for collection2

# Dictionary to store the last track_id for each member
last_track_ids = {}

@client.event
async def on_ready():
    print(f'Logged in as {client.user.name} ({client.user.id})')
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name='Spotify'))

    # Create the task for updating presence data
    client.loop.create_task(update_presence_data())

    # Fetch presence data from all members
    print("Fetching presence data from all members...")
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
        # Aggregate and fetch the top 20 most appearing songs from the database
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
                "$limit": 20
            }
        ]

        top_songs = list(collection.aggregate(pipeline))

        # Create an embed to list the top 20 most appearing songs
        embed = discord.Embed(title="Top 20 Most Appearing Songs", color=discord.Color.blue())

        for idx, song in enumerate(top_songs, 1):
            embed.add_field(
                name=f"{idx}. {song['_id']['title']} - {song['_id']['artist']}",
                value=f"Track URL: {song['_id']['track_url']}\nAppearances: {song['count']}",
                inline=False
            )

        # Send the embed to the Discord channel
        await message.channel.send(embed=embed)

    print('Discord queried top 20 most appearing songs from the database')

async def insert_user_data(user, activity):
    details = activity.details
    spotify_url = details.split(" ")[-1] if details and "spotify" in details else None

    user_data = {
        'track_url': spotify_url,
        'title': details.split(" - ")[0] if details and "spotify" in details and " - " in details else None,
        'artist': details.split(" - ")[1] if details and "spotify" in details and " - " in details else None
    }
    collection.insert_one(user_data)

async def handle_presence_update(member):
    for activity in member.activities:
        if activity.type == discord.ActivityType.listening and activity.name == 'Spotify Scout':
            await insert_user_data(member, activity)

async def update_presence_data():
    await client.wait_until_ready()
    print("Bot is ready to update presence data.")
    
    while not client.is_closed():
        print("Updating presence data...")
        for guild in client.guilds:
            for member in guild.members:
                for activity in member.activities:
                    if isinstance(activity, discord.Spotify):
                        current_track_id = activity.track_id
                        if member.id not in last_track_ids:
                            last_track_ids[member.id] = None
                        
                        if current_track_id != last_track_ids[member.id]:
                            presence_data = {
                                'user_id': str(member.id),
                                'username': member.name,
                                'discriminator': member.discriminator,
                                'activity_type': str(activity.type),
                                'track_id': current_track_id,
                                'track_url': activity.track_url,
                                'album': activity.album,
                                'title': activity.title,
                                'artist': activity.artist,
                                'start_time': activity.start,
                                'end_time': activity.end
                            }
                            
                            print(f"Found Spotify activity for {member.name}:")
                            print(f"Song Title: {activity.title}")
                            print(f"Artist: {activity.artist}")
                            print(f"Album: {activity.album}")

                            print(f"Inserting presence data for {member.name}.")
                            collection.insert_one(presence_data)
                            last_track_ids[member.id] = current_track_id

        print("Finished updating presence data. Waiting for next update...")
        await asyncio.sleep(10)  # Wait for 10 seconds before the next update

# Start the bot
client.run('YOUR_TOKEN_HERE')

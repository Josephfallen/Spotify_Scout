import discord
import pymongo
import asyncio

intents = discord.Intents.default()
intents.guilds = True
intents.guild_messages = True
intents.message_content = True
intents.members = True
intents.presences = True

client = discord.Client(intents=intents)

# MongoDB configuration
mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")
db = mongo_client["spotify"]
collection = db["presences"]

# Dictionary to store the last track_id for each member
last_track_ids = {}

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
        await asyncio.sleep(10)  # Wait for 120 seconds (2 minutes) before the next update

@client.event
async def on_ready():
    print(f'Logged in as {client.user.name} ({client.user.id})')
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name='Spotify'))
    
    # Create the task for updating presence data
    client.loop.create_task(update_presence_data())

# Start the bot
client.run('PUT_YOUR_TOKEN_HERE')

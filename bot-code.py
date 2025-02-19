import os
import discord
import threading
from flask import Flask

# Load token from Railway environment variables
TOKEN = os.getenv("DISCORD_BOT_TOKEN")

# Check if token is set
if not TOKEN:
    raise ValueError("Bot token is missing! Set DISCORD_BOT_TOKEN in Railway variables.")

# Source Channel IDs
SOURCE_CHANNEL_1_ID = 851712915433848852
SOURCE_CHANNEL_2_ID = 785753308279209995

# Target Channel IDs
TARGET_CHANNEL_1_ID = 1324336294603653130
TARGET_CHANNEL_2_ID = 1324057754570063986

# Set up intents
intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.message_content = True

client = discord.Client(intents=intents)

# Flask Setup for UptimeRobot
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!"

def run_flask():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    thread = threading.Thread(target=run_flask, daemon=True)
    thread.start()

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author.bot:
        return  # Ignore bot messages

    # Check if the message is from a source channel and copy to the target channel
    if message.channel.id == SOURCE_CHANNEL_1_ID:
        target_channel = client.get_channel(TARGET_CHANNEL_1_ID)
        if target_channel:
            await target_channel.send(f"📢 **Auto Message:**\n{message.content}")

    elif message.channel.id == SOURCE_CHANNEL_2_ID:
        target_channel = client.get_channel(TARGET_CHANNEL_2_ID)
        if target_channel:
            await target_channel.send(f"📢 **Auto Message:**\n{message.content}")

# Start Flask before running the bot
keep_alive()
client.run(TOKEN)

import discord
import asyncio
import datetime
from discord.ext import commands  # Import the commands extension

# Define your channel IDs
channels = {
    "general-chat": 1234567890,  # Replace with the actual channel ID
    "events": 1234567891,        # Replace with the actual channel ID
}

# Define the intents
intents = discord.Intents.default()
intents.typing = False  # Disable typing event to reduce unnecessary traffic

# Create a bot instance with intents
bot = commands.Bot(command_prefix='!', intents=intents)  # Use commands.Bot from discord.ext.commands

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@bot.command(name='ADD', help='Schedule a message to be sent at a specific date and time.')
async def schedule_message(ctx):
    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    await ctx.send("Please enter the date and time (e.g., YYYY-MM-DD HH:MM):")
    date_time = await bot.wait_for('message', check=check)

    await ctx.send("Please enter the text you want to post:")
    message_text = await bot.wait_for('message', check=check)

    await ctx.send("Please enter the name of the channel where you want to post the message (e.g., general-chat or events):")
    channel_name = (await bot.wait_for('message', check=check)).content.lower()

    try:
        # Convert the date and time to a datetime object
        scheduled_date = datetime.datetime.strptime(date_time.content, '%Y-%m-%d %H:%M')

        # Find the target channel by name or mention
        target_channel_id = channels.get(channel_name)
        target_channel = bot.get_channel(target_channel_id)

        if scheduled_date and target_channel:
            scheduled_messages[ctx.author.id] = {
                'scheduled_date': scheduled_date,
                'message_text': message_text.content,
                'target_channel': target_channel
            }
            await ctx.send("Message scheduled successfully!")
        else:
            await ctx.send("Invalid date, time, or channel name. Please try again.")
    except ValueError:
        await ctx.send("Invalid date or time format. Please use YYYY-MM-DD HH:MM format.")

# Run your bot with the token
bot.run('YOUR_BOT_TOKEN')

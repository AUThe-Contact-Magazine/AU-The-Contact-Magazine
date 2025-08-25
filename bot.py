import discord
from discord.ext import commands
import asyncio
from datetime import datetime

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='/', intents=intents)

@bot.event
async def on_ready():
    print(f'✅ Logged in as {bot.user}')

@bot.command()
async def schedule(ctx, message: str, channel_mention: str, date: str, time: str):
    # Parse channel ID from mention
    if channel_mention.startswith('<#') and channel_mention.endswith('>'):
        channel_id = int(channel_mention[2:-1])
    else:
        await ctx.send("❌ Invalid channel mention format.")
        return

    # Parse datetime
    try:
        scheduled_time = datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M")
    except ValueError:
        await ctx.send("❌ Invalid date/time format. Use YYYY-MM-DD HH:MM")
        return

    now = datetime.now()
    delay = (scheduled_time - now).total_seconds()

    if delay <= 0:
        await ctx.send("❌ Scheduled time must be in the future.")
        return

    await ctx.send(f"✅ Message scheduled for <#{channel_id}> at {scheduled_time}")

    # Wait until the scheduled time
    await asyncio.sleep(delay)

    # Send the message
    channel = bot.get_channel(channel_id)
    if channel:
        await channel.send(message)
    else:
        await ctx.send("❌ Target channel not found.")

# Replace with your bot token
bot.run('MTQwNzU0MDYxMDkzMTM2MDAxNg.G5FmA4.fkmRsNkSBUaR4HeeLYC0k3b7m-a1TkVUnZxCAU')
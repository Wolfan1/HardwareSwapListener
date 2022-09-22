import os
from time import sleep
from threading import Thread

import asyncpraw

import discord
from discord.ext import commands

REDDIT_SECRET = os.environ.get('HWS_SCREENER_SECRET')
DISCORD_SECRET = os.environ.get('HWS_DISCORD_TOKEN')

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix='.', intents=intents)
subscribed_users = []
    
@bot.event
async def on_ready():
    print("=====================================================")
    print(f"\nLogged in as {bot.user} (ID: {bot.user.id})")
    print("\n=====================================================")

@bot.command(name='subscribe')
async def subscribe(ctx):
    member = ctx.message.author
    subscribed_users.append(member)

    await member.send("You are now recieving HWS updates")

async def notify_users(title:str, url:str) -> None:
    for member in subscribed_users:
        await member.send(f'NEW HARDWARE SWAP POST:\n{title}\n{url}')

@bot.command(name='startscan')
async def start_scanning(ctx) -> None:
    reddit = asyncpraw.Reddit(
        client_id = 'Xpvw0QvKT_KMNy0VGJhRfA',
        client_secret = REDDIT_SECRET,
        user_agent = 'Hardware Swap Scraper',
    )

    subreddit = await reddit.subreddit("hardwareswap")

    scanned_posts = []
    while True:
        async for submission in subreddit.new(limit=3):
            title = submission.title
            url = submission.url
            id = submission.id

            if id in scanned_posts:
                pass
            else:
                print(title)
                print(url + '\n')
                scanned_posts.append(id)

                if ('2070' in title) or ('2080' in title) or ('3060' in title) or ('3070' in title):
                    await notify_users(title, url)
                
        
        sleep(5)

bot.run(DISCORD_SECRET)

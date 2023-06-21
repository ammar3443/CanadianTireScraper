import discord
import os
import nest_asyncio
from discord.ext import commands
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By # allow search with parameters
from selenium.webdriver.firefox.options import Options
import time
nest_asyncio.apply()

TOKEN = 'Put Bot Token Here'
CHANNEL_ID = 1119122000305193054
chat = 'General'
bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

@bot.event
async def on_ready():
    channel = bot.get_channel(CHANNEL_ID)
    print('We have logged in as {0.user}'.format(bot))
    
@bot.command()
async def ct(ctx, *args):
    arguments = ' '.join(args)
    print(arguments)
    driver = webdriver.Firefox()
    driver.get("https://www.canadiantire.ca/en.html")
    time.sleep(1)
    item = driver.find_element(By.ID, 'search-input-0')
    item.send_keys(' '+arguments)
    item.send_keys(Keys.RETURN)
    time.sleep(3)
    driver.find_element(By.CLASS_NAME, "nl-product-card__no-button").click()
    time.sleep(2)
    await ctx.send("The price of "+arguments +" is: "+(driver.find_element(By.CLASS_NAME, "nl-price--total").text))
    await ctx.send("Here is the item: "+(driver.current_url))
    
@bot.command()
async def join(ctx):
    if(ctx.author.voice):
        channel = ctx.message.author.voice.channel
        await channel.connect()
    else:
        await ctx.send("You are not in a voice channel!")

@bot.command()
async def leave(ctx):
    if(ctx.voice_client):
        await ctx.guild.voice_client.disconnect()
        await ctx.send("I left he voice channel")
    else:
        await ctx.send("I am not in a voice channel")

bot.run(TOKEN)

import discord
from discord.ext import commands
import json
import bs4
import requests
import urllib


bot = commands.Bot(command_prefix='NB!')


# LIST OF COMMANDS

@bot.command(name='commands')
async def help(ctx):
    embed = discord.Embed(color=0x00ff00)
    embed.add_field(name='NB!commands: ', value='Returns a list of availiable commands.')
    embed.add_field(name='NB!images-apod: ', value='Returns the Astronomy Picture Of the Day.')
    embed.add_field(name='NB!images-search <query>: ', value='Returns the image resulting in a query.')
    embed.add_field(name='NB!iss-location: ', value='Returns the latitude and longitude of the ISS.')
    embed.add_field(name='NB!people: ', value='Returns the number of people in space, their names and the craft they are on.')
    await ctx.send(embed=embed)


# ASTRONOMY PICTURE OF THE DAY COMMAND

@bot.command(name='images-apod')
async def picoftheday(ctx):
    url = 'https://api.nasa.gov/planetary/apod?api_key=Uqw93pcralIeuAyelUbrGMBzvIdM8Z6QxoWSNDjk'
    r = requests.get(url)
    jsonpage = json.loads(r.content)
    print(jsonpage['hdurl'])
    embed = discord.Embed(color=0x00ff00)
    embed.title = f'Image of the day: {jsonpage["title"]}'
    imgurl = str(jsonpage['url'])
    embed.set_image(url=imgurl)
    embed.description = f"""Copyright: {jsonpage['copyright']}                                                                                                                                            
     Explanation: {jsonpage['explanation']}"""
    await ctx.send(embed=embed)


# NASA IMAGES QUERY COMMAND

@bot.command(name='images-search')
async def query(ctx, query='None'):
    embed = discord.Embed(color=0x00ff00)
    url = 'https://images-api.nasa.gov/search?q='+str(query)
    r = requests.get(url)
    jsonpage  = json.loads(r.content)
    for thing in jsonpage['collection']['items']:
        for thing2 in thing['links']:
           embed.set_image(url=str(thing2['href']))
    await ctx.send(embed=embed)


# ISS LOCATION COMMAND

@bot.command(name='iss-location')
async def location(ctx):
    embed = discord.Embed(color=0x00ff00)
    url = 'http://api.open-notify.org/iss-now.json'
    r = requests.get(url)
    jsonpage = json.loads(r.content)
    embed.add_field(name='Latitude: ', value=jsonpage['iss_position']['latitude'])
    embed.add_field(name='Longitude: ', value=jsonpage['iss_position']['longitude'])
    await ctx.send(embed=embed)


# PEOPLE IN SPACE COMMAND

@bot.command(name='people')
async def people(ctx):
    url = 'http://api.open-notify.org/astros.json'
    r = requests.get(url)
    jsonpage  = json.loads(r.content)
    embed = discord.Embed(color=0x00ff00)
    embed.add_field(name='Number of people in space: ', value=str(jsonpage['number']))
    for person in jsonpage['people']:
        num = 1
        embed.add_field(name=person["name"], value=f'Spacecraft: {person["craft"]}')
        num += 1
    embed.set_footer(text='Source: http://api.open-notify.org/astros.json')
    await ctx.send(embed=embed)
bot.run(os.getenv('TOKEN'))

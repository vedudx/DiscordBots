import discord
import os
import requests
import json
import random
from discord.ext import commands
import pymongo
from pymongo import MongoClient

cluster = MongoClient("mongodb+srv://vedant:password@cluster0.zvlz2.mongodb.net/test")

db = cluster["botDb"]

collection = db["botC"]

client = discord.Client()
sad_words = ["sad", "depressed", "unhappy", "angry", "miserable"]

lonely_words = ['lonely', 'bored', 'missing']

starter_encouragements = [
  "Cheer up! @",
  "Hang in there. @",
  "You are a great person @"
]
def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " -" + json_data[0]['a']
  return(quote)

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

# @client.event
# async def on_member_join(member):
#     await member.create_dm()
#     await member.dm_channel.send(
#         f'Hi {member.name}, welcome to my Discord server!'
#     )
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    quer = {"_id": message.author.id}
    if message.content.startswith('-play'):
        if (collection.count_documents(quer) == 0):  
            song = []
            song.append(message.content)
            post = {"_id": message.author.id, "songs":song}
            collection.insert_one(post)
            name = str(message.author)
            end = name.find('#')
            name = name[:end]
            await message.channel.send('added to the playlist of ' + name)
        else:
            query = {"_id": message.author.id}
            user = collection.find(query)
            for result in user:
                score = result["songs"]
            score.append(message.content)
            collection.update_one({"_id":message.author.id}, {"$set":{"songs":score}})
            name = str(message.author)
            end = name.find('#')
            name = name[:end]
            await message.channel.send('added to the playlist by ' + name)

    if message.content.startswith('$fetch'):
        if (collection.count_documents(quer) == 0): 
            await message.channel.send('for now only the user who made the playlist can fetch!')
        else:
            query = {"_id": message.author.id}
            user = collection.find(query)
            for result in user:
                songArray = result["songs"]
            songString = ""
            for song in songArray:
                songString += song + "\n"
            await message.channel.send(songString)


            
    myquery = { "_id": message.author.id }
    if (collection.count_documents(myquery) == 0):
        if "python" in str(message.content.lower()):
            post = {"_id": message.author.id, "score": 1}
            collection.insert_one(post)
            await message.channel.send('accepted!')
    else:
         if "python" in str(message.content.lower()):
            query = {"_id": message.author.id}
            user = collection.find(query)
            for result in user:
                score = result["score"]
            score = score + 1
            collection.update_one({"_id":message.author.id}, {"$set":{"score":score}})
            await message.channel.send('accepted!')

    if message.content.lower() in sad_words:
        word = random.choice(starter_encouragements)
        word += str(message.author)
        await message.channel.send(word)

    if message.content.startswith('$inspire'):
        quote = get_quote()
        await message.channel.send(quote)

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

client.run(TOKEN)
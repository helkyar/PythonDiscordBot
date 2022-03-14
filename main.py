import os
import discord
import requests
import json
import random

api_url  = "https://zenquotes.io/api/random"
sad_words = ["sad", "depressed", "unhappy", "angry", "misserable"]
cheers = ["Cheer up!","You are a great person / bot"]

client = discord.Client()

def get_quote():
  response = requests.get(api_url)
  json_data = json.loads(response.text)
  quote = f'{json_data[0]["q"]} - {json_data[0]["a"]}'
  return quote

@client.event
async def on_ready():
  print(f'We have logged in as {client.user}')

@client.event
async def on_message(msg):
  mct = msg.content
  mch = msg.channel
  
  if msg.author == client.user:
    return

  if mct.startswith('$inspire'):
    quote = get_quote()
    await mch.send(quote)
    
  if any (word in mct for word in sad_words):
    await mch.send(random.choice(cheers) )

client.run(os.environ['TOKEN'])

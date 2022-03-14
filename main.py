import os
import discord
import requests
import json

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
  if msg.author == client.user:
    return

  if msg.content.startswith('$inspire'):
    quote = get_quote()
    await msg.channel.send(quote)

client.run(os.environ['TOKEN'])

import os
import discord
import requests
import json
import random
from replit import db

api_url  = "https://zenquotes.io/api/random"
sad_words = ["sad", "depressed", "unhappy", "angry", "misserable"]
cheers = ["Cheer up!","You are a great person / bot"]

#================= API CONNECTION =====================
def get_quote():
  response = requests.get(api_url)
  json_data = json.loads(response.text)
  quote = f'{json_data[0]["q"]} - {json_data[0]["a"]}'
  return quote
  
#=============== DATABASE CONNECTION ==================
def update_cheers(cheer_msg):
  if "cheers" in db.keys():
    cheers = db["cheers"]
    cheers.append(cheer_msg)
    db["cheers"] = cheers
  else:
     db["cheers"] = cheer_msg

def delete_cheer(index):
  cheers = db["cheers"]
  
  if len(cheers) > index:
    del cheers[index]
  db["cheers"] = cheers

#=============== DISCORD CONNECTION ===================
client = discord.Client()

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

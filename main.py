import os
import discord
import requests
import json
import random
from replit import db

"""
Bots will go to sleep after 1h of incativity, the keep_alive file makes shura that doesn't happen. 
"""

api_url  = "https://zenquotes.io/api/random"
sad_words = ["sad", "depressed", "unhappy", "angry", "misserable"]
cheers = ["Cheer up!","You are a great person / bot"]

#================= API CONNECTION =====================
if "responding" not in db.keys():
  db["responding"] = True

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

  if db["responding"]:
    options = cheers
    if "cheers" in db.keys():
      options = options + db["cheers"]
      
    if any (word in mct for word in sad_words):
      await mch.send(random.choice(cheers) )

  if msg.startswith("$new"):
    new_cheer = msg.split("$new ", 1)[1]
    update_cheers(new_cheer)
    await mch.send("New encouraging message added")

  if msg.startswith("$del"):
    cheer_list = []
    if "cheers" in db.keys():
      index = int(msg.split("$del ",1)[1])
      delete_cheer(index)
      cheer_list = db["cheers"]
      
    await mch.send(cheer_list)

  if msg.startswith("$list"):
    cheer_list = []
    if "cheers" in db.keys():
      cheer_list = db["cheers"]
    await mch.send(cheer_list)

  if msg.startswith("$responding"):
    value = msg.split("$responding ", 1)[1]
    if value.lower() == "true":
      db["responding"] = True
      await mch.send("Responding is on")
    elif value.lower() == "false":
      db["responding"] = False      
      await mch.send("Responding is off")
client.run(os.environ['TOKEN'])

import os
import discord
from discord.ext import commands
import requests
import json
import youtube_dl
import ffmpeg

intents = discord.Intents.default()
intents.members = True

client = commands.Bot(command_prefix = '!', intents = intents)


@client.event
async def on_ready():
  print("The Bot is Online")
  print("/n")

@client.command()
async def hello(ctx): 
  await ctx.send("Hello :)")

@client.event
async def on_member_join(member):
  url = "https://joke3.p.rapidapi.com/v1/joke"

  headers = {
    'x-rapidapi-key': "94bbbef195msh0b7e13c91b2867ep1bcaa5jsn7baee203acb0",
    'x-rapidapi-host': "joke3.p.rapidapi.com"
    }

  response = requests.request("GET", url, headers=headers)

  print(response.text)
  channel = client.get_channel(839829180640133122)
  await channel.send("Hello")
  await channel.send(json.loads(response.text)['content'])
'''
@client.command(pass_context = True)
async def joke(ctx):
  url = "https://joke3.p.rapidapi.com/v1/joke"

  headers = {
    'x-rapidapi-key': "94bbbef195msh0b7e13c91b2867ep1bcaa5jsn7baee203acb0",
    'x-rapidapi-host': "joke3.p.rapidapi.com"
    }

  response = requests.request("GET", url, headers=headers)

  print(response.text)
  #channel = client.get_channel(839829180640133122)
  await ctx.send(json.loads(response.text)['content'])
'''
@client.command()
async def joke(ctx):
  url = "https://joke3.p.rapidapi.com/v1/joke"

  headers = {
    'x-rapidapi-key': "94bbbef195msh0b7e13c91b2867ep1bcaa5jsn7baee203acb0",
    'x-rapidapi-host': "joke3.p.rapidapi.com"
    }

  response = requests.request("GET", url, headers=headers)


  channel = client.get_channel(839829180640133122)
  await channel.send(json.loads(response.text)['content'])

@client.event
async def on_member_remove(member):
  channel = client.get_channel(839829180640133122)
  await channel.send("Goodbye")

@client.command(pass_context = True)
async def join(ctx):
  if (ctx.author.voice):
    channel = ctx.message.author.voice.channel
    await channel.connect(cls = discord.voice_client.VoiceClient)
  else:
    await ctx.send("To use this command you must be in a voice channel")

@client.command(pass_context = True)
async def leave(ctx):
  if (ctx.voice_client):
    await ctx.guild.voice_client.disconnect()
    await ctx.send("I left the voice channel")
  else:
    await ctx.send("I am not in a voice channel")


@client.command(pass_context = True)
async def pause(ctx):
  voice = discord.utils.get(client.voice_clients, guild = ctx.guild)
  if voice.is_playing():
    voice.pause()
  else:
    await ctx.send("There are no songs playing")

@client.command(pass_context = True)
async def resume(ctx):
  voice = discord.utils.get(client.voice_clients, guild = ctx.guild)
  if voice.is_paused():
    voice.resume()
  else:
    await ctx.send("There are no songs paused")

@client.command(pass_context = True)
async def stop(ctx):
  voice = discord.utils.get(client.voice_clients, guild = ctx.guild)
  voice.stop()


@client.command(pass_context = True)
async def play(ctx, url : str):
  song_there = os.path.isfile("song.mp3")
  try:
    if song_there:
      os.remove("song.mp3")
  except PermissionError:
    await ctx.send("A song is playing currently, wait or stop using !stop")
    return
  ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
      'key' : 'FFmpegExtractAudio',
      'preferredcodec': 'mp3',
      'preferredquality': '192',
    }],
  }

  with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    ydl.download([url])
  for file in os.listdir("./"):
    if file.endswith(".mp3"):
      os.rename(file, "song.mp3")

  ctx.voice_client.play(discord.FFmpegPCMAudio(url))


client.run('ODM5ODI3NzE3NjU0NTc3MTgz.YJPUgw.CMrluDGUb44SkdAAraSvczYGq3A')
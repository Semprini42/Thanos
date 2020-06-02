import discord, time, json
from discord.ext import commands
from datetime import datetime
from random import seed, choice
#
with open('config.json') as f:
    config = json.load(f)

bot = commands.Bot(command_prefix="!")

vc = None
channel = None

seed(datetime.now()) #sets the random seed

#announces when the bot is connected
@bot.event
async def on_ready():
    print('Logged in as {}'.format(bot.user.name))
    print('------')

#joins the bot to vc
@bot.command(name = "join")
async def connect(ctx):
    global vc, channel
    vc = ctx.author.voice.channel
    channel = await vc.connect()

#disconnects the bot from vc from vc
@bot.command(name="leave")
async def leave(ctx):
    await channel.disconnect()


#disconnects a user from vc randomly
#perfectly balances
@bot.command(name = "snap")
async def disconectRandUserVC(ctx):
    global vc, channel
    vc = ctx.author.voice.channel
    members = vc.members #gets list of members currently in vc

    #creates audio variables
    snap = discord.FFmpegPCMAudio('fingerSnap2.mp3')

    channel = await vc.connect()
    #plays audio
    channel.play(snap, after = None)
    time.sleep(0.25)
    # number of users to disconnect
    if (len(members) == 1):
        balance = 1
    else:
        balance = int(len(members) / 2)

    for i in range(balance):
        victim = choice(members)
        members.remove(victim)
        await ctx.channel.send("Goodbye {}.".format(victim.name))

        await victim.edit(voice_channel=None)

    time.sleep(0.75)
    await ctx.channel.send("Perfectly balanced.")
    time.sleep(0.75)
    await ctx.channel.send("As all things should be.")
    time.sleep(0.75)
    await channel.disconnect()

bot.run(config['token'])
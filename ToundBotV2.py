import sys

import discord
from discord.ext import commands
import random
import ImageRecog

#ToundBot Version 2.1
#discord.py Version 1.4.1

client = commands.Bot(command_prefix='!')  # discord.Client()

mute = False

# ====================EXTRAS========================
def grammarCheck(message):
    if message != '':
        messageContentList = message.split(' ')
        with open('swearWords.txt') as f:
            for i in range(len(messageContentList)):
                if messageContentList[i] in f.read():
                    f.close()
                    return 1


def checkForGoodWords(content):
    messageContentList = content.split(' ')
    for i in range(len(messageContentList)):
        if messageContentList[i] in good_words:
            return 1


# ==================================================
# Bot ready in cmd
@client.event
async def on_ready():
    print('Logged in as')
    print('ToundBot')
    print('350611730918801418')
    print('READY!')


good_words = ['lovely', 'gorgeous', 'cutie', 'ily']


@client.event
async def on_member_join(member):
    print('{member} has joined, welcome!')


@client.event
async def on_member_remove(member):
    print('{member} has left :(')


@client.event
async def on_message(message):
    if message.author != client.user and not mute:
        channel = message.channel
        if grammarCheck(message.content) == 1:
            await channel.send('@{} Excuse me... please do not say that'.format(message.author))
            await message.delete()
            #Log time and date
            return

        if message.content.startswith('Toundy'):
            await channel.send('YOU CALLED')

        elif message.content.startswith('remove'):
            await channel.send('ToundBot shutting down')
            exit()

        elif message.content.startswith("!unmod ben"):
            await channel.send('Unmodding Skidaddlemynoodle in 5 seconds...')
            for i in range(4, 0, -1):
                await channel.send(i)
            await channel.send('Skidaddlemynoodle has returned to role: Regular')

        elif checkForGoodWords(message.content) == 1:
            await message.add_reaction('\U0001F970')
            await message.add_reaction('\U00002764')

        elif message.content.startswith('!delmessages'):
            content = message.content.split(' ')
            if len(content) > 2:
                await channel.send('{} invalid use of command; 1 arg required'.format(message.author))
                return
            channelMessages = await channel.history(limit=int(content[1]))
            for i in range(len(channelMessages)):
                await message.delete(channelMessages[i])
            await channel.send('{} messages deleted'.format(int(content[1])))
    await client.process_commands(message)


@client.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount=10):
    await ctx.channel.purge(limit=amount)


@client.command()
async def sleep(ctx):
    global mute
    if not mute:
        mute = True
        await ctx.send('z z Z Z Z')
    else:
        await ctx.send('ToundBot is already sleeping.')


@client.command()
async def wake(ctx):
    global mute
    if not mute:
        await ctx.send("Excuse me, I'm already awake...")
        mute = False
    else:
        await ctx.send('Wassup Gamers')
        mute = False


@client.command()
async def joinVC(ctx, vChannel):
    client.move_to(vChannel)
    await ctx.send(f'ToundBot is joining {vChannel}')

@client.command()
async def toundsgf(ctx):
    await ctx.send(file=discord.File('camila.jpg'))

@client.command()
async def disconnect(ctx):
    if client.is_connected():
        client.disconnect
    else:
        await ctx.send('ToundBot aint even in a damn VC...')


@client.command()
async def complimentme(ctx):
    with open('compliments.txt') as f:
        lines = f.read().splitlines()
        await ctx.send(random.choice(lines))
        f.close

@client.command()
async def imbored(ctx):
    with open('compliments.txt') as f:
        lines = f.read().splitlines()
        await ctx.send(random.choice(lines))
        f.close


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Sort the arguments out please')
    elif isinstance(error, commands.CommandNotFound):
        await ctx.send('No idea what that is boo x')
    else:
        print(error)

@client.command()
async def whatsthis(ctx, thing):
    await ctx.send('Hmmmm, I think that is a... hmmmm')
    try:
        # predictions, percentages = ImageRecog.imageRecog(thing)
        # for index in range(len(predictions)):
        #     percentages[index] = int(percentages[index])
        #     if percentages[index] != 0:
        #         await ctx.send(f"I'm {percentages[index]} % certain that's a {predictions[index]}")
        objects, confidence, personInfo = ImageRecog.imageRecog(thing)
        confidence = int(confidence*100)
        personString = ''
        if len(objects) > 1:
            string = ''
            for i in range(len(objects)):
                string = string + objects[i]
                string = string + ', '

            await ctx.send(f"I'm {confidence} % certain that this image contains a {string}")
        else:
            await ctx.send(f"I'm {confidence} % certain that's a {objects[0]}")

        if personInfo != []:
            if len(personInfo[0]) > 1:
                for i in range(len(personInfo[0])):
                    await ctx.send("Calculating genders")
            else:
                await ctx.send(f"I'm {personInfo[0][0]} % certain the person is a {personInfo[1][0]}")
    except:
        print(sys.exc_info()[0])
        await ctx.send("Oh snap, I need to learn that")


client.run('')

#STUFF TO ADD
#Image recognition
#im bored bot
#Split up commands
#Zombies calc
#Bday counter (how old)
#heads or tails
#beatboxer
#leaderboard
#sqldatabase
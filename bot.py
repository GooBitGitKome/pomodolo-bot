import discord
from discord.ext import commands
import os
import asyncio

intents = discord.Intents.default()
intents.all()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)
timer = 25
interval = 5
times = 4
interval_long = 15
stop_flg = False
finished_jobs = 0
tasks = []
# @bot.command()
# async def join(ctx):
#     if ctx.author.voice:
#         channel = ctx.author.voice.channel
#         await channel.connect()
#         print(f'Joined {channel}')
#     else:
#         await ctx.send('You must be in a voice channel to use this command!')

# @bot.command() 
# async def leave(ctx):
#     if ctx.voice_client:
#         await ctx.guild.voice_client.disconnect()
#         print('Left voice channel')
#     else:
#         await ctx.send('I am not in a voice channel!')

@bot.command()
async def stop(ctx):
    global stop_flg
    stop_flg = True
    await ctx.send('Stopped timer')

@bot.command()
async def start(ctx):
    global stop_flg
    stop_flg = False
    global finished_jobs
    if not ctx.author.voice:
        await ctx.send('You need to be in a voice channel to use this command.')
        return

    #countdown
    for i in range(5):
        if(await stopped(ctx)):
            return
        await my_sleeptimer(ctx, 1)
        await ctx.send(f'Start after {5 - i } sedonds')
    await ctx.send('Pomodoro timer started!')
    # await ctx.send(f'Timer set to {timer} minutes, interval set to {interval} minutes, times set to {times}, long interval set to {interval_long} minutes')
    while(True):
        if(await stopped(ctx)):
            break
        else:
            for i in range(times):
                if(await stopped(ctx)):
                    break
                await set_mute(ctx,ctx.author , True)
                await set_deafen(ctx, ctx.author, True)

                await job_timer(ctx)

                await set_mute(ctx, ctx.author, False)
                await set_deafen(ctx, ctx.author, False)
                finished_jobs += 1
                await status(ctx)
                if(await my_sleeptimer(ctx, interval * 60) == False): #interrupted
                    return#stopped
            await ctx.send('Nice job!')
            #finished n times jobs
            if(await my_sleeptimer(ctx, interval_long * 60) == False): #interrupted
                return#stopped
            

        
@bot.command()
async def set_timer(ctx, _timer, _interval, _times, _interval_long):
    global timer
    timer = _timer
    global interval
    interval = _interval  
    global times
    times = _times
    global interval_long
    interval_long = _interval_long
    await ctx.send(f'Timer set to {timer} minutes, interval set to {interval} minutes, times set to {times}, long interval set to {interval_long} minutes')

@bot.command()
async def set_preset(ctx):
    global timer 
    timer = 25
    global interval
    interval = 5
    global times
    times = 4
    global interval_long
    interval_long = 15
    await ctx.send('Timer set to 25 minutes, interval set to 5 minutes, times set to 4, long interval set to 15 minutes') 

async def status(ctx):
    await ctx.send(f'Finished jobs: {finished_jobs}')
    await ctx.send(f'Total job time: {finished_jobs * timer}')

async def job_timer(ctx):
    global timer
    for i in range(timer):
        if(await stopped(ctx)):
            return
        await my_sleeptimer(ctx, 60)
        # await asyncio.sleep(1)
        if(not (timer - i + 1) == 0 
        and (timer - i + 1) % 5  == 0
            and (not (timer - i + 1) == timer)):
            await ctx.send(f'{(timer - i + 1)} minutes left!')

async def stopped(ctx):
    global stop_flg
    global tasks
    if(stop_flg):
        for task in tasks:
            task.cancel()
        await set_mute(ctx, ctx.author, False)
        await set_deafen(ctx, ctx.author, False)
        return True
    return False

async def set_mute(ctx, member: discord.Member, mute):
    # Check if the user is in a voice channel
    if ctx.author.voice:
        # Mute the user
        for member in ctx.author.voice.channel.members:
            await member.edit(mute=mute)
        # await ctx.send(f'{member.display_name} has been muted.')
    # else:
        # await ctx.send('You need to be in a voice channel to use this command.')

# Define a command to deafen a user
async def set_deafen(ctx, member: discord.Member, deafen):
    # Check if the user is in a voice channel
    if ctx.author.voice:
        # Deafen the user
        for member in ctx.author.voice.channel.members:
            await member.edit(deafen=deafen)
        # await ctx.send(f'{member.display_name} has been deafened.')
    # else:
        # await ctx.send('You need to be in a voice channel to use this command.')
async def my_sleeptimer(ctx, sec): 
    for i in range(sec):
        await asyncio.sleep(1)
        if await stopped(ctx):
            finished_jobs = 0 if finished_jobs > 0 else finished_jobs - 1
            return False
    return True
# bot.add_command(test)
bot.run(os.getenv('TOKEN'))
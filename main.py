from discord.ext import commands, tasks
import os
import discord
import random

# These color constants are taken from discord.js library
colors = {
  'DEFAULT': 0x000000,
  'WHITE': 0xFFFFFF,
  'AQUA': 0x1ABC9C,
  'GREEN': 0x2ECC71,
  'BLUE': 0x3498DB,
  'PURPLE': 0x9B59B6,
  'LUMINOUS_VIVID_PINK': 0xE91E63,
  'GOLD': 0xF1C40F,
  'ORANGE': 0xE67E22,
  'RED': 0xE74C3C,
  'GREY': 0x95A5A6,
  'NAVY': 0x34495E,
  'DARK_AQUA': 0x11806A,
  'DARK_GREEN': 0x1F8B4C,
  'DARK_BLUE': 0x206694,
  'DARK_PURPLE': 0x71368A,
  'DARK_VIVID_PINK': 0xAD1457,
  'DARK_GOLD': 0xC27C0E,
  'DARK_ORANGE': 0xA84300,
  'DARK_RED': 0x992D22,
  'DARK_GREY': 0x979C9F,
  'DARKER_GREY': 0x7F8C8D,
  'LIGHT_GREY': 0xBCC0C0,
  'DARK_NAVY': 0x2C3E50,
  'BLURPLE': 0x7289DA,
  'GREYPLE': 0x99AAB5,
  'DARK_BUT_NOT_BLACK': 0x2C2F33,
  'NOT_QUITE_BLACK': 0x23272A
}


channel_id = 858500378336034826

def get_prefix(client, message):
    prefixes = ['!']    # sets the prefix
    return prefixes

bot = commands.Bot(                         # Create a new bot
    command_prefix=get_prefix,              # Set the prefix
    description='A bot that sends out automated reminders and keeps track of lists',  # Set a description for the bot
    owner_id=858379602452152340,            # Your unique User ID
    case_insensitive=True                   # Make the commands case insensitive
)


        
cogs = ['cogs.basic']


@bot.event
async def on_ready(): # Do this when the bot is logged in
    print(f'Logged in as {bot.user.name} - {bot.user.id}')  # Print the name and ID of the bot logged in.
    bot.remove_command('help') # Removes built-in help command
    for cog in cogs:
        bot.load_extension(cog)
    return

@tasks.loop(seconds = 10)
async def called_once_a_day():
  message_channel = bot.get_channel(channel_id)
  basic = bot.get_cog("Basic")
  users = basic.users
  for auth in users:
    color_list = [c for c in colors.values()]
    msg = await message_channel.send(content='Now generating the embed...')

    color_list = [c for c in colors.values()]
        # Convert the colors into a list
        # To be able to use random.choice on it

    embed = discord.Embed(
        title=users[auth].title,
        description=users[auth].reminder,
        color=random.choice(color_list)
    )

    embed.set_author(
            name=auth.name,
            icon_url=auth.avatar_url
        )

    await msg.edit(
        embed=embed,
        content="@everyone"
    )

@called_once_a_day.before_loop
async def before():
    await bot.wait_until_ready()
    print("Finished waiting")

called_once_a_day.start()
  
# Finally, login the bot
bot.run(os.environ['TOKEN'], bot=True, reconnect=True)
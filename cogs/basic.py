from discord.ext import commands, tasks
from datetime import datetime as d
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

auth = None

class Reminder:
  def __init__(self, name, reminder, embed):
    self.title = name
    self.reminder = reminder
    self.embed = embed

# New - The Cog class must extend the commands.Cog class
class Basic(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
        self.users = {}
    
    # Define a new command
    @commands.command(
        name='ping',
        description='pong!',
        aliases=['p']
    )
    async def ping_command(self, ctx):
        start = d.timestamp(d.now())
        # Gets the timestamp when the command was used

        msg = await ctx.send(content='Pinging')
        # Sends a message to the user in the channel the message with the command was received.
        # Notifies the user that pinging has started

        await msg.edit(content=f'Pong!\nOne message round-trip took {(d.timestamp(d.now())-start) * 1000}ms.')
        # Ping completed and round-trip duration show in ms
        # Since it takes a while to send the messages, it will calculate how much time it takes to edit an message.
        # It depends usually on your internet connection speed

        return
    
    @commands.command(
        name='remind',
        description='create a reminder',
        aliases=['r']
    )
    async def remind_command(self, ctx):
      def check(ms):
            # Look for the message sent in the same channel where the command was used
            # As well as by the user who used the command.
            return ms.channel == ctx.message.channel and ms.author == ctx.message.author
      auth = ctx.message.author

      # ask the user for the name of reminder
      await ctx.send(content='What would you like to name the reminder?')
      msg = await self.bot.wait_for('message', check=check)
      title = msg.content # Set the title

      # ask for the reminder
      await ctx.send(content='What would you like the reminder to be?')
      msg = await self.bot.wait_for('message', check=check)
      desc = msg.content

        
      await ctx.send(content=f"Sucess! Here is how the reminder will look:")

      msg = await ctx.send(content='Now generating the embed...')

      color_list = [c for c in colors.values()]
      # Convert the colors into a list
      # To be able to use random.choice on it

      embed = discord.Embed(
          title=title,
          description=desc,
          color=random.choice(color_list)
      )

      # Also set the embed author to the command user
      embed.set_author(
          name=ctx.message.author.name,
          icon_url=ctx.message.author.avatar_url
      )

      await msg.edit(
          embed=embed,
          content=None
      )
      self.users[auth] = Reminder(title, desc, embed)
          
      return  
    
    @commands.command(
        name='view',
        description='view your reminder',
        aliases=['v']
    )
    async def view_command(self, ctx):
        auth = ctx.message.author
        if auth in self.users:
          msg = await ctx.send(content='Now generating the embed...')

          color_list = [c for c in colors.values()]
          # Convert the colors into a list
          # To be able to use random.choice on it

          embed = discord.Embed(
              title=self.users[auth].title,
              description=self.users[auth].reminder,
              color=random.choice(color_list)
          )

          # Also set the embed author to the command user
          embed.set_author(
              name=auth.name,
              icon_url=auth.avatar_url
          )

          await msg.edit(
              embed=embed,
              content=None
          )
              
          return  
        else:
          await ctx.send(content='You do not have a reminder created. Type !remind or !r to set one up!') 
      
    @commands.command(
      name='edit',
      description='edit your reminder',
      aliases=['e']
    )
    async def edit_command(self, ctx):
      def check(ms):
            # Look for the message sent in the same channel where the command was used
            # As well as by the user who used the command.
            return ms.channel == ctx.message.channel and ms.author == ctx.message.author
      auth = ctx.message.author
      msg = ctx.message.content

        # Extracting the text sent by the user
        # ctx.invoked_with gives the alias used
        # ctx.prefix gives the prefix used while invoking the command
      prefix_used = ctx.prefix
      alias_used = ctx.invoked_with
      text = msg[len(prefix_used) + len(alias_used):]

      if auth in self.users: 
        
        if text != ' name' and text != ' reminder':
          await ctx.send(content='Please state whether you would like to edit the name or message of the reminder')
          return

        if text == ' name':
          # ask the user for the name of reminder
          await ctx.send(content='What would you like to name the reminder?')
          msg = await self.bot.wait_for('message', check=check)
          self.users[auth].title = msg.content # Set the title

        if text == ' reminder':
          # ask for the reminder
          await ctx.send(content='What would you like the reminder to be?')
          msg = await self.bot.wait_for('message', check=check)
          self.users[auth].reminder = msg.content
          
        await ctx.send(content="Sucess! Here is how the reminder will look:")

        msg = await ctx.send(content='Now generating the embed...')

        color_list = [c for c in colors.values()]
        # Convert the colors into a list
        # To be able to use random.choice on it

        embed = discord.Embed(
            title=self.users[auth].title,
            description=self.users[auth].reminder,
            color=random.choice(color_list)
        )

        # Also set the embed author to the command user
        embed.set_author(
            name=ctx.message.author.name,
            icon_url=ctx.message.author.avatar_url
        )

        await msg.edit(
            embed=embed,
            content=None
        )
              
        return  

      else:
        await ctx.send(content='You do not have a reminder created. Type !remind or !r to set one up!')
        return
    
    @commands.command(
      name='delete',
      description='delete your reminder',
      aliases=['d', 'del']
    )
    async def delete_command(self, ctx):
      def check(ms):
            # Look for the message sent in the same channel where the command was used
            # As well as by the user who used the command.
            return ms.channel == ctx.message.channel and ms.author == ctx.message.author
      auth = ctx.message.author
      msg = ctx.message.content

        # Extracting the text sent by the user
        # ctx.invoked_with gives the alias used
        # ctx.prefix gives the prefix used while invoking the command
      prefix_used = ctx.prefix
      alias_used = ctx.invoked_with
      text = msg[len(prefix_used) + len(alias_used):]

      if auth in self.users:
        while True:
          await ctx.send(content='Are you sure you want to delete your reminder?')
          msg = await self.bot.wait_for('message', check=check)

          if msg.content.lower() == "yes":
            del self.users[auth]
            await ctx.send(content='Reminder deleted!')
            break
          elif msg.content.lower() == "no":
            await ctx.send(content='Canceled!')
            break
          else:
            await ctx.send(content='Please choose yes or no.')
      else:
        await ctx.send(content='You do not have a reminder created. Type !remind or !r to set one up!')
      return
    
    @commands.command(
      name='help',
      description='recieve a list of commands',
      aliases=['h'],
    )

    async def help_command(self, ctx):
      color_list = [c for c in colors.values()]
      help_embed = discord.Embed(
          title='Help',
          color=random.choice(color_list)
      )
      help_embed.set_thumbnail(url=self.bot.user.avatar_url)
      help_embed.set_footer(
          text=f'Requested by {ctx.message.author.name}',
          icon_url=self.bot.user.avatar_url
      )

      # Get a list of all cogs
      cogs = [c for c in self.bot.cogs.keys()]

   # If cog is not specified by the user, we list all cogs and commands
      for cog in cogs:
           # Get a list of all commands under each cog

           cog_commands = self.bot.get_cog(cog).get_commands()
           commands_list = ''
           for comm in cog_commands:
               commands_list += f'!**{comm.name}** - {comm.description}\n'

           # Add the cog's details to the embed.

           help_embed.add_field(
               name="List of Commands",
               value=commands_list,
               inline=False
           ).add_field(
               name='\u200b', value='\u200b', inline=False
           )

           # Also added a blank field '\u200b' is a whitespace character.
      pass
      await ctx.send(embed=help_embed)

      return

def setup(bot):
  bot.add_cog(Basic(bot))
    # Adds the Basic commands to the bot
    # Note: The "setup" function has to be there in every cog file
from discord.ext import commands
import discord
import config

def is_owner():
    # Check if the message author is in the config.owners list
    def predicate(ctx):
        if ctx.author.id not in config.owners:
            raise commands.NotOwner()
        else:
            return True
    
    return commands.check(predicate)
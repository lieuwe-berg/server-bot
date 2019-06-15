import os
import config
from discord.ext import commands

bot = commands.Bot(
    command_prefix=config.prefix,
    description=config.description,
    case_insensitive=True,
    help_command=None
)

bot.config = config

for file in os.listdir('cogs'):
    if file.endswith('.py'):
        name = file[:-3]
        bot.load_extension(f"cogs.{name}")

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} -- {bot.user.id}')
    

bot.run(config.token)
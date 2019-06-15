from discord.ext import commands
import discord
import config

class Basic(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(description='Pong! See if the bot is online.')
    async def ping(self, ctx):
        await ctx.send(embed=discord.Embed(description='Pong! 🏓', color=config.embed_color))
    
    
    @commands.command(description='The help menu.', usage='help [command]')
    async def help(self, ctx, *, command=None):
        if command:
            command = self.bot.get_command(command)
            if not command:
                return await ctx.send(f'Command not found. Use `{ctx.prefix}help` to see all commands.')
            
            embed = discord.Embed(title=command.name, description=command.description, color=config.embed_color)
            if not command.usage: command.usage = command.name
            embed.add_field(name='Usage', value=f'`{ctx.prefix + command.usage}`')

            await ctx.send(embed=embed)
            
        else:
            help_menu = f"{self.bot.description}\n\nPrefix: `{ctx.prefix}`\nAdditional help: `{ctx.prefix}{self.bot.get_command('help').usage}`\n"
            for (cog_name, cog) in self.bot.cogs.items():
                if len(cog.get_commands()) is 0:
                    continue

                help_menu += f'\n**{cog_name}:**\n```'
                for cmd in cog.get_commands():
                    help_menu += f'\n{cmd.name}'
                help_menu += '```'
            
            await ctx.send(embed=discord.Embed(title=self.bot.user.name + ' help menu', description=help_menu, color=config.discord_color))


def setup(bot):
    bot.add_cog(Basic(bot))
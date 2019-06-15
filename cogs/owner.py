from discord.ext import commands
import discord
import config

import ast, sys, io, textwrap, traceback
from contextlib import redirect_stdout

class Owner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_result = None
    
    def cleanup_code(self, content):
        if content.startswith("```") and content.endswith("```"):
            return "\n".join(content.split("\n")[1:-1])
        return content.strip("` \n")


    @commands.command(description='Reloads all cogs (command categories).')
    async def reload(self, ctx):
        reloaded = 0
        for cog in self.bot.cogs.keys():
            cog = cog.lower()
            self.bot.unload_extension(f'cogs.{cog}')
            self.bot.load_extension(f'cogs.{cog}')
            reloaded += 1
        await ctx.send(f'Reloaded {reloaded} cogs.')

    
    @commands.command(description='Restarts the bot.')
    async def restart(self, ctx):
        await ctx.send('Restarting...')
        await self.bot.logout()
    
    
    @commands.command(name='eval', description='Evaluates the supplied code in the bot.', usage='eval <code>')
    async def _eval(self, ctx, *, body=None):
        if not body:
            await ctx.send('Please provide code to evaluate.')
            return
        
        env = {
            "bot": self.bot,
            "ctx": ctx,
            "channel": ctx.channel,
            "author": ctx.author,
            "guild": ctx.guild,
            "message": ctx.message,
            "_": self._last_result,
        }

        env.update(globals())
        body = self.cleanup_code(body)
        stdout = io.StringIO()
        to_compile = f'async def func():\n{textwrap.indent(body, "  ")}'
        try:
            exec(to_compile, env)
        except Exception as e:
            return await ctx.send(
                embed=discord.Embed(
                    description=f"```py\n{e.__class__.__name__}: {e}\n```",
                    color=config.embed_color,
                )
            )
        func = env["func"]
        try:
            with redirect_stdout(stdout):
                ret = await func()
        except Exception:
            value = stdout.getvalue()
            await ctx.send(
                embed=discord.Embed(
                    description=f"```py\n{value}{traceback.format_exc()}\n```",
                    color=config.embed_color,
                )
            )
        else:
            value = stdout.getvalue()
            try:
                await ctx.message.add_reaction("✅")
            except discord.Forbidden:
                pass
            if ret is None:
                if value:
                    await ctx.send(
                        embed=discord.Embed(
                            descrption=f"```py\n{value}\n```",
                            color=config.discord_color,
                        )
                    )
            else:
                self._last_result = ret
                await ctx.send(
                    embed=discord.Embed(
                        description=f"```py\n{value}{ret}\n```",
                        color=config.discord_color,
                    )
                )


def setup(bot):
    bot.add_cog(Owner(bot))
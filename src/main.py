import sys

import discord
from discord.ext import commands

if __name__ == "__main__":
    print(f"discord.py version: {discord.__version__}")
    print("input bot token:", end = '')
    token = input()

    bot = commands.Bot(command_prefix = '$')

    @bot.command()
    async def say(ctx: commands.Context, str: str):
        '''botに発言させる 詳細は'$say help' '''
        if str == "help":
            embed = discord.Embed(title = "usage: $say [str]")
            embed.add_field(name = "str", value = "strをbotが発言する")
            await ctx.send(embed = embed)
        else:
            await ctx.send(str)

    @say.error
    async def say_error(ctx: commands.Context, ec: commands.CommandError):
        if isinstance(ec, commands.MissingRequiredArgument):
            await ctx.send("コマンド'$say'に引数が足りない\nTry '$say help' for more information")

    @bot.command()
    async def voice(ctx: commands.Context, option: str):
        ''' botと音声チャンネル関連コマンド 詳細は'$voice help' '''
        if option == "connect":
            if ctx.author.voice is None:
                await ctx.send("先にコマンド送信者がボイスチャンネルに入っている必要性があります")
            else:
                await ctx.author.voice.channel.connect()
        elif option == "disconnect":
            if ctx.guild.voice_client is None:
                await ctx.send("Botがボイスチャンネルに入っていません")
            else:
                await ctx.guild.voice_client.disconnect()
        elif option == "help":
            embed = discord.Embed(title = "usage: $voice [cmd]")
            embed.add_field(name = "connect", value = "botを音声チャンネルに入室させる", inline = False)
            embed.add_field(name = "disconnect", value = "botを音声チャンネルから退出させる", inline = False)
            await ctx.send(embed = embed)

    @voice.error
    async def voice_error(ctx: commands.Context, ec: commands.CommandError):
        if isinstance(ec, commands.MissingRequiredArgument):
            await ctx.send("コマンド'$voice'に引数が足りない\nTry '$voice help' for more information")

    @bot.event
    async def on_ready():
        print(f"We have logged in as {bot.user}")

        servers = bot.guilds
        
        if servers is None:
            print("Bot is not on the server", file = sys.stderr)
            sys.exit(1)

        for server in servers:
            # botが入っているすべてのサーバーのテキストチャンネルにログインメッセージ
            # チャンネルがどの順序でchannelsに入ってるのか不明なのでどのチャンネルにログインメッセージが送られるかは不明
            # channel.positionで一番上にあるチャンネルに送ることができるがラグでposition:0が存在しないことがありutils.getの戻り値がNoneになる可能性ありなので要検討
            # TODO: システムメッセージチャンネルに送りたいがdiscord APIに存在しない?
            main_text_channel = discord.utils.find(lambda c: c.type == discord.ChannelType.text, server.channels)
            await main_text_channel.send(f"bot({bot.user}) is online!")

    bot.run(token)

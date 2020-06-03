import sys

import discord

if __name__ == "__main__":
    print(f"discord.py version: {discord.__version__}")
    print("input bot token:", end = '')
    token = input()

    client = discord.Client()

    @client.event
    async def on_ready():
        print(f"We have logged in as {client.user}")

        servers = client.guilds
        
        if servers is None:
            print("Bot is not on the server", file = sys.stderr)
            sys.exit(1)

        for server in servers:
            # botが入っているすべてのサーバーのテキストチャンネルにログインメッセージ
            # チャンネルがどの順序でchannelsに入ってるのか不明なのでどのチャンネルにログインメッセージが送られるかは不明
            # channel.positionで一番上にあるチャンネルに送ることができるがラグでposition:0が存在しないことがありutils.getの戻り値がNoneになる可能性ありなので要検討
            # TODO: システムメッセージチャンネルに送りたいがdiscord APIに存在しない?
            main_text_channel = discord.utils.find(lambda c: c.type == discord.ChannelType.text, server.channels)
            await main_text_channel.send(f"bot({client.user}) is online!")
        
    client.run(token)

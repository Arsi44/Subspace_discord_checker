import json

import discord

from config import TOKEN, CHAT_ID, YOUR_ID

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('/check'):
        # get channel by id
        channel = client.get_channel(CHAT_ID)

        # validation (must contain limit value and '/check' word )
        if len(message.content.split(' ')) != 2:
            await channel.send('Wrong number of parameters\nExample: ```/check 5```\nMaximum value is 100 messages')
        else:
            if int(message.content.split(' ')[1]) > 100:
                limit = 100
            else:
                limit = int(message.content.split(' ')[1])

            # get messages from new to old
            async for message in channel.history(limit=limit):
                info = {}
                print(f'Message id: {message.id} || Author: {message.author.name} || Author ID: {message.author.id}')
                info['Message id'] = message.id
                info['Author'] = message.author.name
                info['Author ID'] = message.author.id
                info['Reacted users'] = []
                for reaction in message.reactions:
                    async for user in reaction.users():
                        info['Reacted users'].append({"Name": user.name, "User ID": user.id,
                                                      "Created at": user.created_at.strftime("%m/%d/%Y, %H:%M:%S")})

                # Send in channel
                # await channel.send(json.dumps(info))

                # Send in DM
                user = await client.fetch_user(YOUR_ID)
                await user.send(json.dumps(info))




if __name__ == '__main__':
    client.run(TOKEN)

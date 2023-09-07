import json

import asyncio
import discord

# load variables
import os
from dotenv import load_dotenv
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
YOUR_ID = os.getenv("YOUR_ID")

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print('Bot is ready')

@client.event
async def on_message(message):
    global parsing_active
    global user_counts

    if message.content.startswith('!start_parse'):
        parsing_active = True
        print('Parsing has started')
        while parsing_active:
            await get_voice_channel_members()
            await asyncio.sleep(5)

    elif message.content.startswith('!end_parse'):
        parsing_active = False
        print('Parsing has stopped')

    elif message.content.startswith('!write_json'):
        with open('users.json', 'w') as file:
            json.dump(user_counts, file)
        await message.channel.send('The user_counts dictionary is saved in the file user_counts.json')

    elif message.content.startswith('!print_users'):
        user_list = '\n'.join([f'{user} - {count}' for user, count in user_counts.items()])
        await message.channel.send(f'Participants:\n{user_list}')

    elif message.content.startswith('!refresh_counter'):
        user_counts = {}
        print('user_counts has refreshed')

    elif message.content.startswith('!help'):
        await message.channel.send(f'Usable commands:\n!start_parse\n!end_parse\n!write_json\n!print_users\n!refresh_counter\n!help')



async def get_voice_channel_members():
    # navigate to voice
    channel_id = 1224296501207892029
    voice_channel = client.get_channel(channel_id)
    if voice_channel is None:
        print('Wrong channel ID')
        return

    # get members in dict
    members = voice_channel.members
    member_names = [member.name for member in members]
    for name in member_names:
        user_counts[name] = user_counts.get(name, 0) + 1

    print(f'Participants in voice channel: {", ".join(member_names)}', user_counts)

if __name__ == '__main__':
    # Create an empty dictionary to store the data
    user_counts = {}
    # PArsing flag
    parsing_active = False
    client.run(TOKEN)




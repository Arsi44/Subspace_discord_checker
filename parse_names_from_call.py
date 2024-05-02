import asyncio
import discord
import csv

# load variables
import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

TOKEN = os.getenv("TOKEN")
channel_id = int(os.getenv("channel_id"))

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print('Bot is ready')


@client.event
async def on_message(message):
    global parsing_active
    global user_counters

    if message.content.startswith('!start_parse'):
        parsing_active = True
        await message.channel.send('Parsing has started (1 point in 5 seconds instead of 60 for tests)')
        while parsing_active:
            await get_voice_channel_members()
            await asyncio.sleep(5)

    elif message.content.startswith('!end_parse'):
        parsing_active = False
        await message.channel.send('Parsing has stopped')

    elif message.content.startswith('!write_csv'):
        with open('users.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Name', 'Count'])
            for user, count in user_counters.items():
                writer.writerow([user, count])
        await message.channel.send('The user_counters dictionary is saved in the file users.csv')

    elif message.content.startswith('!print_users'):
        user_list = '\n'.join([f'{user} - {count}' for user, count in user_counters.items()])
        await message.channel.send(f'Participants:\n{user_list}')

    elif message.content.startswith('!refresh_counter'):
        user_counters = {}
        await message.channel.send('user_counters have been refreshed')

    elif message.content.startswith('!help_addition'):
        await message.channel.send(
            f'Usable commands:\n!start_parse\n!end_parse\n!write_csv\n!print_users\n!refresh_counter\n!help_addition')


async def get_voice_channel_members():
    # navigate to voice
    voice_channel = client.get_channel(channel_id)
    if voice_channel is None:
        print('Wrong channel ID')
        return

    # get members in dict
    members = voice_channel.members
    member_names = [member.name for member in members]
    for name in member_names:
        user_counters[name] = user_counters.get(name, 0) + 1

    print(f'Participants in voice channel: {", ".join(member_names)}', user_counters)


if __name__ == '__main__':
    # Create an empty dictionary to store the data
    user_counters = {}
    # PArsing flag
    parsing_active = False
    client.run(TOKEN)

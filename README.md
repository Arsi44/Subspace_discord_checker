The program is based on the discord.py package especially to help the SubSpace project. The package consists of several bots and will be supplemented as needed.

_All functionality can be launched inside one single bot. The description is divided into logical modules for convenience._

### 1. A bot that collects statistics on people who are currently using a specific Discord voice channel
The bot connects to the specified chat and simply checks its participants. It receives those who are currently in the voice channel and adds points to them.
As a result, we can display the scores both inside the discord and in a text file.
As result we have such output:
Participants:
discrod_user1 - 11
discrod_user2 - 15
discrod_user3 - 20
discrod_user4 - 17
...


### 2. A bot that scans user message history to count them
##### Bot operating procedure:
1) Get channel by id
2) Get messages from channel
3) Get info (users who sent messages with their account details, reactions and users who sent reactions)
4) Send info in direct message

In order to start using the bot, it is necessary to:
- Install requirements **pip install -r requirements.txt**
- Specify the Token, as well as the id of the chat in which the check will be carried out. We will use `config.py` file for this.
- Run file `main.py` **python3 main.py**


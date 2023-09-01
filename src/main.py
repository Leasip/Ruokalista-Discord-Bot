import discord
from ruokalista_tool import *
import config

# Replace YOUR_BOT_TOKEN with your bot's token
bot_token = config.bot_token

# Replace YOUR_CHANNEL_ID with the ID of the channel you want to send the message to
channel_id = config.channel_id
debug_channel_id = config.debug_channel_id

print(bot_token)
# Define the client object
intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)
message= str 

def send_msg(text: str) -> None:
    global message

    message = text
    client.run(bot_token)

def send_debug(text: str) -> None:
    global message
    global channel_id

    message = text
    channel_id = debug_channel_id
    client.run(bot_token)

# Define an event handler for when the client is ready
@client.event
async def on_ready() -> None:
    # Get the channel object
    channel = client.get_channel(int(channel_id))

    # Send the message
    await channel.send(message)

    # Disconnect the client
    await client.close()


if __name__=="__main__":
    # Connect the client to the Discord API
    try:
        ruokalista = get_ruokalista()
        assert ruokalista.__len__() != 0

        send_msg("@everyone\n" + ruokalista)

    except AssertionError as error:
        send_debug("ERROR:\nget_ruokalista() returned empty str\n" + str(error))
    
    except AttributeError as error:
        # Check if the AttributeError was caused 
        # by the parser function not finding any food
        if "'int' object has no attribute '__len__'" in str(error):
            print("No food today")
            exit()

        send_debug("ERROR:\nAttributeError happended :(\n" + str(error))
        send_msg("Tapahtui odottamaton virhe")
                

    except Exception as error:
        send_debug("ERROR:\nException happended :(\n" + str(error))
        send_msg("Tapahtui odottamaton virhe")
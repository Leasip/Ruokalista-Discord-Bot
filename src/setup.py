import time
new_file_name = "src/config.py"

print("This script will create the config file for the bot")
print("Please remember that thiese are private information and should not be shared with anyone")
print("This config file is only stored locally and is not uploaded to github")
bot_token= input("please input your bot token: ")
bot_token ="bot_token = "+ bot_token
channel_id= input("please input the channel id you want to send the message to: ")
channel_id ="channel_id = "+ channel_id
debug_channel_id= input("please input the debug channel id: ")
debug_channel_id ="debug_channel_id = "+ debug_channel_id

print("Make sure to add the bot to the server and give it the required permissions")
print("also check that the information you inputted is correct")
with open(new_file_name, "w") as new_file:
    new_file.write(bot_token + "\n"+ channel_id + "\n" + debug_channel_id)

print("The config file has been created successfully.")
time.sleep(3)
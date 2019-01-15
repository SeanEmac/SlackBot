import os
import time
import re
import requests
from slackclient import SlackClient

slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))
starterbot_id = None

RTM_READ_DELAY = 1 # 1 second delay between reading from RTM
MENTION_REGEX = "^<@(|[WU].+?)>(.*)"
AVAIL_COMMANDS = "joke, time or fortune" # can add more

'''
    These 2 functions determine if a message is directed at the bot
    If it is, the handle_command function is called
'''
def parse_bot_commands(slack_events):
    for event in slack_events:
        if event["type"] == "message" and not "subtype" in event:
            user_id, message = parse_direct_mention(event["text"])
            if user_id == starterbot_id:
                return message, event["channel"]
    return None, None

def parse_direct_mention(message_text):
    matches = re.search(MENTION_REGEX, message_text)
    # the first group contains the username, the second group contains the remaining message
    return (matches.group(1), matches.group(2).strip()) if matches else (None, None)

'''
    This function checks if a command exists
    If it does, it performs the command
    This is where Code will go
'''
def handle_command(command, channel):
    default_response = "Not sure what you mean. Try *{}*.".format(AVAIL_COMMANDS)
    response = None

    if command.startswith("joke"):
        response = get_joke()

    elif command.startswith("time"):
        response = "Time code will go here"

    elif command.startswith("fortune"):
        response = "fortune code will go here"

    # Send response back to slack channel
    slack_client.api_call(
        "chat.postMessage",
        channel=channel,
        text=response or default_response
    )

'''
    Send request to the Internet Chuck Norris DataBase
    Get a random joke
'''
def get_joke():
    res = requests.get("http://api.icndb.com/jokes/random")
    data = res.json()
    return data["value"]["joke"]

'''
    Runs the bot, checks messages every second
'''
if __name__ == "__main__":
    if slack_client.rtm_connect(with_team_state=False):
        print("Starter Bot connected and running!")
        # Read bot's user ID by calling Web API method `auth.test`
        starterbot_id = slack_client.api_call("auth.test")["user_id"]
        while True:
            command, channel = parse_bot_commands(slack_client.rtm_read())
            if command:
                handle_command(command, channel)
            time.sleep(RTM_READ_DELAY)
    else:
        print("Connection failed. Exception traceback printed above.")
from slackclient import SlackClient
import g
import os
import re
import time
import requests
import json

slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))
starterbot_id = None

RTM_READ_DELAY = 1 # 1 second delay between reading from RTM
MENTION_REGEX = "^<@(|[WU].+?)>(.*)"
AVAIL_COMMANDS = "```listRepos \ngetRepo <Repo Name> \nlistBranches <Repo Name>```" # can add more

def parse_bot_commands(slack_events):
    for event in slack_events:
        if event["type"] == "message" and not "subtype" in event:
            user_id, message = parse_direct_mention(event["text"])
            if user_id == starterbot_id:
                return message, event["channel"], event["ts"]
    return None, None, None


def parse_direct_mention(message_text):
    matches = re.search(MENTION_REGEX, message_text)
    # the first group contains the username, the second group contains the remaining message
    return (matches.group(1), matches.group(2).strip()) if matches else (None, None)


def handle_command(command, channel, ts):
    default_response = "Not sure what you mean, try:\n {}".format(AVAIL_COMMANDS)
    response = None
    print(ts)
    if (len(command.split()) > 1):
        command, arguments = command.split(' ', 1)

    if command.startswith("listRepos"):
        response = g.get_repos()

    elif command.startswith("getRepo"):
        response = g.get_repo('SeanEmac', arguments)

    elif command.startswith("listBranches"):
        response = g.get_branches('SeanEmac', arguments)

    # Send response back to slack channel
    slack_client.api_call(
        "chat.postMessage",
        channel=channel,
        text=response or default_response,
        thread_ts=ts,
    )


if __name__ == "__main__":
    if slack_client.rtm_connect(with_team_state=False):
        print("Starter Bot connected and running!")
        # Read bot's user ID by calling Web API method `auth.test`
        starterbot_id = slack_client.api_call("auth.test")["user_id"]
        while True:
            command, channel, ts = parse_bot_commands(slack_client.rtm_read())
            if command:
                handle_command(command, channel, ts)
            time.sleep(RTM_READ_DELAY)
    else:
        print("Connection failed. Exception traceback printed above.")
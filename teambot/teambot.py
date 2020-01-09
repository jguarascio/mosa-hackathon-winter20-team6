# Based on https://www.fullstackpython.com/blog/build-first-slack-bot-python.html

import random
import os
import re
import slack
import certifi
import ssl as ssl_lib

# instantiate Slack client
ssl_context = ssl_lib.create_default_context(cafile=certifi.where())
bot_token = os.environ["SLACK_BOT_TOKEN"]
oauth_token = os.environ["SLACK_OAUTH_TOKEN"]
web_client = slack.WebClient(token=bot_token)
rtm_client = slack.RTMClient(token=bot_token, ssl=ssl_context)

# starterbot's user ID in Slack: value is assigned after the bot starts up
# TODO: Setting this causes RTM to fail, not sure why
#starterbot_id = web_client.auth_test()["user_id"]

# constants
MENTION_REGEX = "^<@(|[WU].+?)>(.*)"


def random_teams(channel_members, team_size):
    """
    A function to randomly pair people in a list
    :param channel_members: list of members in channel
    :result: resulting pairs
    """
    random.shuffle(channel_members)
    length = len(channel_members) // team_size
    return list(zip(channel_members[:length], channel_members[length:]))


def parse_direct_mention(message_text):
    """
        Finds a direct mention (a mention that is at the beginning) in message text
        and returns the user ID which was mentioned. If there is no direct mention, returns None
    """
    matches = re.search(MENTION_REGEX, message_text)
    # the first group contains the username, the second group contains the remaining message
    return (matches.group(1), matches.group(2).strip()) if matches else (None, None)


@slack.RTMClient.run_on(event="message")
def handle_command(**payload):
    data = payload["data"]
    #web_client = payload["web_client"]
    channel_id = data.get("channel")
    #user_id = data.get("user")
    text = data.get("text")

    print(text)

    mention, command = parse_direct_mention(text)

    #TODO: This should check against the derived bot ID, not against a constant
    if mention == "USDBDBULX": #starterbot_id:
        # Default response is help text for the user
        default_response = "Not sure what you mean."

        # Finds and executes the given command, filling in response
        response = None
        # This is where you start to implement more commands!
        if command == "getteams":
            channels_info = web_client.channels_info(channel=channel_id)
            channel_members = channels_info["channel"]["members"]
            #TODO: Don't include bots in the teams
            #TODO: Make sure every group has > 1 member (e.g., make a team of 3 if doing pairs)
            teams = random_teams(channel_members, 2)
            response = "Ok, I'll create channels for the following teams:\n"

            i = 1
            for team in teams:
                # TODO: Create the channel or DM here
                user_list = str(team)
                user_list = user_list.translate({ord(i): None for i in "()' "})
                print(user_list)
                try:
                    # Create a direct multi-party IM
                    mpim = web_client.mpim_open(users=user_list)
                    # TODO: OR create a channel
                    # new_channel_name = ""
                    # Not sure if this is how to pass user IDs to kwargs...
                    # new_channel = web_client.conversations_create(name=, "user_ids=" + user_list)
                except:
                    pass

                response = response + "Team " + str(i) + ": "
                for user in team:
                    users_info = web_client.users_info(user=user)
                    user_name = users_info["user"]["name"]
                    response = response + user_name + ", "
                response = response[:-2] + "\n"
                i += 1

        # Sends the response back to the channel
        web_client.chat_postMessage(channel=channel_id, text=response or default_response)


if __name__ == "__main__":
    print("Starting RTM client...")
    rtm_client.start()

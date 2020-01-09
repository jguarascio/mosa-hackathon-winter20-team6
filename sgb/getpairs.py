import os
import slack
import ssl as ssl_lib
import certifi
import random


def random_pairs(bot, channel):
    """
    A function to randomly pair people in a list
    :param bot:
    :param channel:
    :result: resulting pairs
    """
    channels_info = bot.channels_info(channel=channel)
    print("here", channels_info)
    channel_members = channels_info["channel"]["members"]

    random.shuffle(channel_members)
    length = len(channel_members)//2
    return list(zip(channel_members[:length], channel_members[length:]))


if __name__ == "__main__":
    ssl_context = ssl_lib.create_default_context(cafile=certifi.where())

    # set up bot and oauth tokens
    bot_token = os.environ["SLACK_BOT_TOKEN"]
    oauth_token = os.environ["SLACK_OAUTH_TOKEN"]
    user = slack.WebClient(token=oauth_token)
    bot = slack.WebClient(token=bot_token)

    # Get channel list for workspace
    channels_list = bot.channels_list()
    for channel in channels_list["channels"]:
        pairs = random_pairs(bot, channel["id"])

        if len(pairs) > 0:
            for i in range(0, len(pairs)):
                # convert pair to a string and strip unnecessary characters
                pair = str(pairs[i])
                pair = pair.translate({ord(i): None for i in "()' "})
                print(pair)
                try:
                    mpim = user.mpim_open(users=pair)
                except:
                    pass

import os
import logging
import asyncio
import ssl as ssl_lib

import certifi
import slack

from mcit_community import MCITCommunity

"""This file runs asynchronously."""

# For simplicity we'll store our app data in-memory with the following data structure.
# start_app_messages_sent = {"channel": {"user_id": start_app_message}}
start_app_messages_sent = {}


async def start_app(web_client: slack.WebClient, user_id: str, channel: str):
    # Create a new onboarding tutorial.
    mcit_community = MCITCommunity(channel)

    # Get the onboarding message payload
    message = mcit_community.get_message_payload('start')

    # Post the onboarding message in Slack
    response = await web_client.chat_postMessage(**message)

    # Capture the timestamp of the message we've just posted so
    # we can use it to update the message after a user
    # has completed an onboarding task.
    mcit_community.timestamp = response["ts"]

    # Store the message sent 
    if channel not in start_app_messages_sent:
        start_app_messages_sent[channel] = {}
    start_app_messages_sent[channel][user_id] = mcit_community

async def find_classmate(web_client: slack.WebClient, user_id: str, channel: str):
    # Create a new onboarding tutorial.
    mcit_community = MCITCommunity(channel)

    # Get the find classmate message payload
    message = mcit_community.get_message_payload('find')

    # Post the onboarding message in Slack
    response = await web_client.chat_postMessage(**message)

    # Capture the timestamp of the message we've just posted so
    # we can use it to update the message after a user
    # has completed an onboarding task.
    mcit_community.timestamp = response["ts"]

    # Store the message sent 
    if channel not in start_app_messages_sent:
        start_app_messages_sent[channel] = {}
    start_app_messages_sent[channel][user_id] = mcit_community

# ================ Team Join Event =============== #
# When the user first joins a team, the type of the event will be 'team_join'.
# Here we'll link the onboarding_message callback to the 'team_join' event.
@slack.RTMClient.run_on(event="team_join")
async def onboarding_message(**payload):
    """Create and send an onboarding welcome message to new users. Save the
    time stamp of this message so we can update this message in the future.
    """
    # Get WebClient so you can communicate back to Slack.
    web_client = payload["web_client"]

    # Get the id of the Slack user associated with the incoming event
    user_id = payload["data"]["user"]["id"]

    # Open a DM with the new user.
    response = web_client.im_open(user_id)
    channel = response["channel"]["id"]

    # Post the onboarding message.
    await start_onboarding(web_client, user_id, channel)


# ============= Reaction Added Events ============= #
# When a users adds an emoji reaction to the onboarding message,
# the type of the event will be 'reaction_added'.
# Here we'll link the update_emoji callback to the 'reaction_added' event.
@slack.RTMClient.run_on(event="reaction_added")
async def update_emoji(**payload):
    """Update the onboarding welcome message after receiving a "reaction_added"
    event from Slack. Update timestamp for welcome message as well.
    """
    data = payload["data"]
    web_client = payload["web_client"]
    channel_id = data["item"]["channel"]
    user_id = data["user"]

    # Get the original tutorial sent.
    onboarding_tutorial = onboarding_tutorials_sent[channel_id].get(user_id)

    if onboarding_tutorial is None:
        return

    # Mark the reaction task as completed.
    onboarding_tutorial.reaction_task_completed = True

    # Get the new message payload
    message = onboarding_tutorial.get_message_payload()

    # Post the updated message in Slack
    updated_message = await web_client.chat_update(**message)

    # Update the timestamp saved on the onboarding tutorial object
    onboarding_tutorial.timestamp = updated_message["ts"]


# ============== Message Events ============= #
# When a user sends a DM, the event type will be 'message'.
# Here we'll link the message callback to the 'message' event.
@slack.RTMClient.run_on(event="message")
async def message(**payload):
    """Display the onboarding welcome message after receiving a message
    that contains "start".
    """
    data = payload["data"]
    web_client = payload["web_client"]
    channel_id = data.get("channel")
    user_id = data.get("user")
    text = data.get("text")

    if text and text.lower() == "start":
        return await start_app(web_client, user_id, channel_id)
    elif text and text.lower() == "find":
        return await find_classmate(web_client, user_id, channel_id)
    else:
        return #await help_user(web_client, user_id, channel_id)


if __name__ == "__main__":
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.addHandler(logging.StreamHandler())
    ssl_context = ssl_lib.create_default_context(cafile=certifi.where())
    slack_token = os.environ["SLACK_BOT_TOKEN"]
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    rtm_client = slack.RTMClient(
        token=slack_token, ssl=ssl_context, run_async=True, loop=loop
    )
    loop.run_until_complete(rtm_client.start())

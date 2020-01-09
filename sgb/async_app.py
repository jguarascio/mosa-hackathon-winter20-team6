import os
import logging
import asyncio
import ssl as ssl_lib

import certifi
import slack

from mcit_community import MCITCommunity
import getpairs

"""This file runs asynchronously."""

async def find_classmate(web_client: slack.WebClient, channel: str):
    mcit_community = MCITCommunity(channel)
    message = mcit_community.get_message_payload('find')
    response = await web_client.chat_postMessage(**message)

async def help_user(web_client: slack.WebClient, channel: str):
    mcit_community = MCITCommunity(channel)
    message = mcit_community.get_message_payload('help')
    response = await web_client.chat_postMessage(**message)

# ============== Message Events ============= #
@slack.RTMClient.run_on(event="message")
async def message(**payload):

    data = payload["data"]
    web_client = payload["web_client"]
    channel_id = data.get("channel")
    user_id = data.get("user")
    text = data.get("text")

    mcit_community = MCITCommunity(channel_id)
    
    if text.lower() == 'find':
        pairs = getpairs.random_pairs(web_client, channel_id)
        message = mcit_community.get_pairs_message(pairs)
        return await web_client.chat_postMessage(**message)
    elif text.lower() == 'start':
        message = mcit_community.get_start_message()
        return await web_client.chat_postMessage(**message)
    elif text.lower() == 'help':
        message = mcit_community.get_help_message()
        return await web_client.chat_postMessage(**message)
    


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

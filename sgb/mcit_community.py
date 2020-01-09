class MCITCommunity:
    """Constructs the onboarding message and stores the state of which tasks were completed."""

    # TODO: Create a better message builder:
    # https://github.com/slackapi/python-slackclient/issues/392
    # https://github.com/slackapi/python-slackclient/pull/400

    WELCOME_BLOCK = {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": (
                "Welcome to the MCIT Community Bot! :wave::blush:\n\n"
                "*Get started by following the instructions below:*"
            ),
        },
    }
    DIVIDER_BLOCK = {"type": "divider"}

    def __init__(self, channel):
        self.channel = channel
        self.username = "MCIT Community Bot"
        self.icon_emoji = ":robot_face:"
        self.timestamp = ""

    def get_start_message(self):
        return {
            "ts": self.timestamp,
            "channel": self.channel,
            "username": self.username,
            "icon_emoji": self.icon_emoji,
            "blocks": [
                self.WELCOME_BLOCK,
                self.DIVIDER_BLOCK,
                *self._get_start_block(),
                self.DIVIDER_BLOCK,
            ],
        }

    def get_help_message(self):
        return {
            "ts": self.timestamp,
            "channel": self.channel,
            "username": self.username,
            "icon_emoji": self.icon_emoji,
            "blocks": [
                *self._get_help_block(),
            ],
        }
    
    def get_pairs_message(self, pairs: list):
        return {
            "ts": self.timestamp,
            "channel": self.channel,
            "username": self.username,
            "icon_emoji": self.icon_emoji,
            "blocks": [
                *self._get_random_pairs_block(pairs),
            ],
        }

    def _get_start_block(self):
        text = (
            f"*Find a classmate* :thinking_face:\n"
            "You can quickly find a classmate to chat with by typing 'find'.\n"
            "If you need help at any time, just type 'help'."
        )
        return self._get_task_block(text)
    
    def _get_help_block(self):
        text = (
            f"*Unknown command* :thinking_face:\n"
            "Please enter 'find' to find a classmate."
        )
        return self._get_task_block(text)

    def _get_random_pairs_block(self, pairs: list):
        string = " "
        string = string.join(pairs)
        text = (
            f"*Here are the pairs!*\n"
            '{string}'.format(string)
            )
        return self._get_task_block(text)

    @staticmethod
    def _get_task_block(text):
        return [
            {"type": "section", "text": {"type": "mrkdwn", "text": text}},
        ]

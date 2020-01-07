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
        self.find_task_completed = False

    def get_message_payload(self, command: str):
        if command == 'start':
            return {
                "ts": self.timestamp,
                "channel": self.channel,
                "username": self.username,
                "icon_emoji": self.icon_emoji,
                "blocks": [
                    self.WELCOME_BLOCK,
                    self.DIVIDER_BLOCK,
                    *self._get_find_block(),
                    self.DIVIDER_BLOCK,
                ],
            }
        elif command == 'find':
            return {
                "ts": self.timestamp,
                "channel": self.channel,
                "username": self.username,
                "icon_emoji": self.icon_emoji,
                "blocks": [
                    *self._get_classmate_block(),
                ],
            }

    def _get_find_block(self):
        task_checkmark = self._get_checkmark(self.find_task_completed)
        text = (
            f"{task_checkmark} *Find a classmate* :thinking_face:\n"
            "You can quickly find a classmate to chat with by typing 'find'."
        )
        return self._get_task_block(text)

    def _get_classmate_block(self):
        text = (
            f" *We have found you the perfect match!*\n"
            "There should now be a 'Direct Message' set up between you and your classmate.\n"
            "Don't be a stranger!"
            )
        return self._get_task_block(text)

    @staticmethod
    def _get_checkmark(task_completed: bool) -> str:
        if task_completed:
            return ":white_check_mark:"
        return ":white_large_square:"

    @staticmethod
    def _get_task_block(text):
        return [
            {"type": "section", "text": {"type": "mrkdwn", "text": text}},
        ]

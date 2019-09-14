import discord
from typing import Callable, List, Dict, Tuple


class Client(discord.Client):

    def __init__(self):
        self.on_message_functions = []
        self.on_message_args = []
        super().__init__()

    def register_on_message_callback(
            self,
            fun: Callable[[discord.Message, any], Tuple[str, discord.Channel]],
            args: List[any]
    ) -> None:
        """
        This function adds a call back function to be executed when the
        client receives a message.

        When called, the function will receive the discord message, then the arguments.
        The function should return a tuple containing the message to send, and then the channel
        to send the response to.s
        """
        self.on_message_functions.append(fun)
        self.on_message_args.append(args)

    async def on_ready(self) -> None:
        print('Successfully Logged in as {0}', self.user)

    async def on_message(self, message: discord.Message) -> None:
        """
        Called when a message is received, executed all registered callback functions,
        passing in the message and there arguments.
        """

        # Don't Respond to Yourself
        if message.author == self.user:
            return

        # Responses to be sent after processing all messages.
        responses: List[Tuple[str, discord.Channel]] = []

        content: str = str(message.content)
        for fun, args in zip(self.on_message_functions, self.on_message_args):
            value = fun(message, *args)
            if value is not None:
                responses.append(value)

        for (response, channel) in responses:
            if response is not None and response != '':
                await channel.send(response)

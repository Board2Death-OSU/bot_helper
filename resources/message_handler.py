from typing import Callable, List, Dict, Tuple


class MessageHandler:

    def __init__(self, responses: Dict[str, str]):
        self.responses: Dict[str, str] = responses

    def process_message(self, msg: str) -> str:
        response: str = ''
        for key in self.responses:
            if key in msg:
                response = self.responses[key]
                return response
        return response


def get_handler(responses: Dict[str, str]) -> MessageHandler:
    return MessageHandler(responses)

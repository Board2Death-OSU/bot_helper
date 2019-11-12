import random
from typing import List
import os


class ImageHandler:

    def __init__(self, images: List[str], keyword: str, channel):
        self.images = images
        self.keyword = keyword.capitalize()
        self.channel = channel

    def get_call_back(self):
        def _call_back(message):
            channel = message.channel
            message = message.content.capitalize()
            if str(channel) == self.channel:
                if self.keyword in message:
                    index = random.randint(0, len(self.images) - 1)
                    file_name = self.images[index]
                    return file_name, channel
        return _call_back

    @staticmethod
    def get_files(directory):
        temp = os.listdir(directory)
        result = []
        for img in temp:
            result.append(directory + '/' + img)
        return result

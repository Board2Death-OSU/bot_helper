class MessageHandler:

    def __init__(self, responses):
        self.responses = responses

    def process_message(self, msg):
        response = ''
        for key in self.responses:
            if key in msg:
                response = self.responses[key]
                return response
        return response


def get_handler(file_name):
    return MessageHandler(file_name)

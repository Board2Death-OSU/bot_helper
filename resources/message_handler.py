import json

class MessageHandler:

    def __init__(self,file_name):
        input_file=open(file_name)
        data=json.loads(input_file.read())
        input_file.close()
        self.responses=data['responses']

    def process_message(self,msg):
        response=''
        for key in self.responses:
            if key in msg:
                response=self.responses[key]
                return response
                
def get_handler(file_name):
    return MessageHandler(file_name)
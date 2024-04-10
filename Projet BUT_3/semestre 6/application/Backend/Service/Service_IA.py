from Model.IA import IA
from Service.Service_Chat import Service_Chat
from Service.Service_Chat_Message import Service_Chat_Message
from Exception.UserNotConnectedException import UserNotConnectedException
from Exception.ModelNotSelectedException import ModelNotSelectedException

class Service_IA:
    def __init__(self):
        pass

    def generate_responses(self, user_question, user_id, chat_id, user_is_connected, file_content, have_file, model):

        if user_is_connected == False:
            raise UserNotConnectedException("User not connected")    

        serviceChat = Service_Chat()
        serviceChatMessage = Service_Chat_Message()
        ia = IA()
        
        ia_response_json = {}
        ia_response_json["chat_id"] = chat_id
        ia_response_json["user_question"] = user_question

        if chat_id == None:
            chat_title = self.title_chat(user_question)
            new_chat_id = serviceChat.create_chat(user_id, chat_title, user_is_connected, model)

            ia_response_json["chat_id"] = new_chat_id
            ia_response_json["chat_title"] = chat_title

            chat_id = new_chat_id

        ia_response = ia.generate_responses(user_question, file_content, have_file, model)
        ia_response_json["ia_response"] = ia_response
        
        serviceChatMessage.add_user_chat_message(chat_id, user_question, user_is_connected)
        serviceChatMessage.add_ia_chat_message(chat_id, str(ia_response))

        return ia_response_json


    def title_chat(self, chat_title):
        chat_title = chat_title[:19]
        chat_title += "..."
        return chat_title
    


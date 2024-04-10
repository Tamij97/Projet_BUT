from Model.Database import Database
from Exception.UserNotConnectedException import UserNotConnectedException
from Service.Service_Chat_Message import Service_Chat_Message

class Service_Chat:
    def __init__(self):
        pass

    def get_chat(self, chat_id, user_id, is_connected):
        db = Database()

        if is_connected == False:
            raise UserNotConnectedException("User not connected")
        
        chat = db.select_chat_by_id_and_user_id(chat_id, user_id)

        db.close()
        return chat
    
    def create_chat(self, user_id, chat_title, is_connected, model):
        db = Database()

        if is_connected == False:
            raise UserNotConnectedException("User not connected")
        
        try:
            db.begin_transaction()
            chat_id = db.insert_chat(user_id, chat_title, model)
            db.commit_transaction() 
        except Exception as e:
            db.rollback_transaction() 
        finally:
            db.close()
        
        return chat_id
    
    def delete_chat(self, chat_id, is_connected, user_id):
        db = Database()
        serviceChatMessage = Service_Chat_Message()

        if is_connected == False:
            raise UserNotConnectedException("User not connected")
        
        serviceChatMessage.delete_chat_message(chat_id, is_connected)
        db.delete_chat_by_id_and_by_user_id(chat_id, user_id)
        
        db.close()

    def get_all_user_chats(self, user_id, is_connected):
        datas={}

        db = Database()
    
        if is_connected == False:
            raise UserNotConnectedException("User not connected")

        chats = db.select_all_user_chats(user_id)

        for chat in chats:
            data = {
                'chat_id': chat[0],
                'chat_title': chat[1],
                'chat_date': chat[2],
                'chat_model': chat[3]
            }

            datas.update({chat[0]: data})

        db.close()
        return datas


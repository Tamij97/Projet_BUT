from flask import Blueprint, request, jsonify
from Service.Service_User import Service_User
from Service.Service_Chat import Service_Chat
from Service.Service_Chat_Message import Service_Chat_Message
from Exception.UserExistsException import UserExistsException
from Exception.UserNotFoundException import UserNotFoundException

signup_blueprint = Blueprint('signup', __name__)
login_blueprint = Blueprint('login', __name__)
user_chat_history_blueprint = Blueprint('user chat history', __name__)
delete_chat_blueprint = Blueprint('delete chat', __name__)
chat_message_blueprint = Blueprint('chat message', __name__)

@signup_blueprint.route('/signup', methods=['POST'])
def signup_user():
    service_user = Service_User()

    try:
        username = request.json['username']
        password = request.json['password']

        message = service_user.signup_user(username, password)
        return jsonify({'message': message}), 200

    except UserExistsException as e:
        return jsonify({'message': str(e)}), 409


@login_blueprint.route('/login', methods=['POST'])
def login_user():
    service_user = Service_User()
    
    username = request.json['username']
    password = request.json['password']
    
    try:
        user_information = service_user.login_user(username, password)

        if user_information['password']:
            user_information['message']= 'Connected successfully.'
            return jsonify(user_information), 200
        else:
            return jsonify({'message': 'Password incorrect.'}), 401
        
    except UserNotFoundException:
        return jsonify({'message': 'User not found.'}), 404
    
@user_chat_history_blueprint.route('/chatHistory', methods=['GET'])
def user_chat_history():
    serviceChat = Service_Chat()
    
    user_id = request.json['user_id']
    user_is_connected = request.json['user_is_connected']

    try:
        chat_history = serviceChat.get_all_user_chats(user_id, user_is_connected)
        return jsonify(chat_history), 200
    except Exception as e:
        return jsonify({'message': "Error fetching chat history."}), 500
    
@delete_chat_blueprint.route('/deleteChat', methods=['POST'])
def user_chat_history():
    serviceChat = Service_Chat()
    
    user_id = request.json['user_id']
    user_is_connected = request.json['user_is_connected']
    chat_id = request.json['chat_id']

    try:
        serviceChat.delete_chat(chat_id, user_is_connected, user_id)
        return jsonify({'message': "As success"}), 200
    except Exception as e:
        return jsonify({'message': "Error fetching chat history."}), 500

@chat_message_blueprint.route('/chatMessage', methods=['GET'])
def chat_message():
    serviceChatMessage = Service_Chat_Message()
    
    user_id = request.json['user_id']
    user_is_connected = request.json['user_is_connected']
    chat_id = request.json['chat_id']

    try:
        chat = serviceChatMessage.get_chat_messages_by_chat_id_and_user_id(chat_id, user_is_connected, user_id)
        return jsonify(chat), 200
    except Exception as e:
        return jsonify({'message': "Error fetching chat history."}), 500
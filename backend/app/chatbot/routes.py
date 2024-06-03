from flask import Blueprint, request, jsonify
from datetime import datetime
from .db_services import *
# Assuming AI service functions are defined here
from .ai_services import get_query_response

chatbot_blueprint = Blueprint('chatbot_blueprint', __name__)


@chatbot_blueprint.route('/session/start', methods=['POST'])
def start_session():
    session_id = create_session()
    return jsonify({"session_id": str(session_id)})


@chatbot_blueprint.route('/session/end', methods=['POST'])
def end_session_route():
    session_id = request.json.get('session_id')
    end_session(session_id)
    return jsonify({"status": "Session ended"})


@chatbot_blueprint.route('/conversation/start', methods=['POST'])
def start_conversation_route():
    session_id = request.json.get('session_id')
    conversation_id = start_conversation(session_id)
    return jsonify({"conversation_id": str(conversation_id)})


@chatbot_blueprint.route('/conversation/end', methods=['POST'])
def end_conversation_route():
    conversation_id = request.json.get('conversation_id')
    end_conversation(conversation_id)
    return jsonify({"status": "Conversation ended"})


@chatbot_blueprint.route('/message/send', methods=['POST'])
def send_message():
    conversation_id = request.json.get('conversation_id')
    session_id = request.json.get('session_id')
    text = request.json.get('text')
    context = request.json.get('context', '')
    lat = request.json.get('lat', 0)
    lng = request.json.get('lng', 0)
    message_id = add_message(conversation_id, text, 'user')

    # Send the query to AI
    response_text = get_query_response(text, context, lat, lng)
    log_query(session_id, text, response_text)

    ai_message_id = add_message(conversation_id, response_text, "ai")
    return jsonify({
        "user_message": {
            "id": str(message_id),
            "text": text,
            "sender": 'user'
        },
        "ai_response": {
            "id": str(ai_message_id),
            "text": response_text,
            "sender": "ai"
        }
    })


@chatbot_blueprint.route('/message/get', methods=['GET'])
def get_messages_route():
    conversation_id = request.args.get('conversation_id')
    messages = get_messages(conversation_id)
    return jsonify({"messages": messages})

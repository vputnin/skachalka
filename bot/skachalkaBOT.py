import telebot
from telebot import types
import os
import json
import requests

TOKEN = os.environ['TG_TOKEN']  # Your Telegram Bot Token
bot = telebot.TeleBot(TOKEN)

# Variables to store user data
user_data = {}

# Handler for the '/start' command
@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_data[message.chat.id] = {'video_link': '', 'words': []}
    markup = types.ReplyKeyboardMarkup(row_width=3)
    itembtn1 = types.KeyboardButton('Video Link')
    itembtn2 = types.KeyboardButton('Words')
    itembtn3 = types.KeyboardButton('Send')
    markup.add(itembtn1, itembtn2, itembtn3)
    bot.send_message(message.chat.id, "Choose an option:", reply_markup=markup)

# Handler for text messages
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    chat_id = message.chat.id
    if message.text == 'Video Link':
        msg = bot.send_message(chat_id, 'Enter the video link:')
        bot.register_next_step_handler(msg, process_video_link_step)
    elif message.text == 'Words':
        msg = bot.send_message(chat_id, 'Enter a list of words (separated by space):')
        bot.register_next_step_handler(msg, process_words_step)
    elif message.text == 'Send':
        send_to_external_server(chat_id)
    else:
        bot.send_message(chat_id, 'Please use the buttons.')

def process_video_link_step(message):
    chat_id = message.chat.id
    user_data[chat_id]['video_link'] = message.text
    bot.send_message(chat_id, f'Video link saved: {message.text}')

def process_words_step(message):
    chat_id = message.chat.id
    user_data[chat_id]['words'] = message.text.split()
    bot.send_message(chat_id, f'Words saved: {message.text}')

def send_to_external_server(chat_id):
    request_params = {
        'url': user_data[chat_id]['video_link'],
        'word_for_search': user_data[chat_id]['words']
    }
    
    try:
        # Sending a GET request to the external server
        # response = requests.get(os.environ['EXTERNAL_SERVER'], params=request_params)
        bot.send_message(chat_id, f"For now i am not fully functioning. This message provides backend link {os.environ['EXTERNAL_SERVER']}")
        # Sending the server's response back to the user in the chat
        # bot.send_message(chat_id, f'Server response: {response.text}')
    except Exception as e:
        # In case of an error, send the error message to the chat
        bot.send_message(chat_id, f'Failed to send data to server: {e}')

# Entry point for Yandex Cloud Function
def handler(event, context):
    message = types.Update.de_json(event['body'])
    bot.process_new_updates([message])
    return {
                "statusCode": 200,
                "headers": {"Content-Type": "application/json"},
                "body": json.dumps({"mesage": "ok"})
            }

# For local tests.
if __name__ == "__main__":
    bot.infinity_polling()
    

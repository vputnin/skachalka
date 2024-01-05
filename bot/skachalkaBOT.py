import telebot
from telebot import types
import requests
from flask import Flask, request

app = Flask(__name__)

# bot = telebot.TeleBot(CHAT_BOT_ID)

# Replace this with the URL of your external server
EXTERNAL_SERVER_URL = 'http://localhost:5000/search'

TOKEN = ''
bot = telebot.TeleBot(TOKEN, threaded=False)
app = Flask(__name__)

# Variables to store user data
user_data = {}

# Process webhook calls
@app.route('/' + TOKEN, methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200

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
    print('message.text')
    user_data[chat_id]['video_link'] = message.text
    bot.send_message(chat_id, f'Video link saved: {message.text}')

def process_words_step(message):
    chat_id = message.chat.id
    user_data[chat_id]['words'] = message.text.split()
    bot.send_message(chat_id, f'Words saved: {message.text}')

def send_to_external_server(chat_id):
    requestParams = {}
    requestParams['url'] = user_data[chat_id]['video_link']
    requestParams['word_for_search'] = user_data[chat_id]['words']
    
    try:
        # Sending a GET request to the external server
        response = requests.get(EXTERNAL_SERVER_URL, params=requestParams)

        # Sending the server's response back to the user in the chat
        bot.send_message(chat_id, f'Server response: {response.text}')
    except Exception as e:
        # In case of an error, send the error message to the chat
        bot.send_message(chat_id, f'Failed to send data to server: {e}')
bot.infinity_polling()

# Start Flask server
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)), ssl_context='adhoc')

import telebot
import openai
import random
import time
import threading

bot_token = [...]
bot = telebot.TeleBot(bot_token)

openai.api_key = [...]

conversation = []

def get_openai_response(text):

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": "You are a helpful assistant."}, {"role": "user", "content": text}],
        max_tokens=300,
        temperature=0.5,
        top_p=0.9,
    )
    return response.choices[0].message.content

def add_variation(response):
    variations = ["Hmm.., ", "Ouh, ", "Well.., ", "Mybee.."]
    variation = random.choice(variations)
    return variation

def change_topic(response):
    topics = ["Mari kita bicarakan tentang hal lain, seperti...", "Hmm, berbicara tentang hal ini membuat saya ingin tahu tentang...", "Saya ingin membicarakan sesuatu yang berbeda, misalnya..."]
    new_topic = random.choice(topics)
    return response + "\n\n" + new_topic

# dientitas
bot_identity = {
    "name": "Takanashi-Rika",
    "cretor" : "Drayn",
    "location" : "tokyo"

}
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_name = "Bng 💔" 

    if "nama kamu" in message.text.lower():
        if "siapa yang membuatmu" in message.text.lower():
            bot_response = f"Saya dibuat oleh {bot_identity['creator']}."
        elif "dimana kamu tinggal" in message.text.lower():
            bot_response = f"Saya tinggal di {bot_identity['location']}."
        elif "apa keahlianmu" in message.text.lower():
            bot_response = f"Saya adalah seorang ahli dalam bidang {bot_identity['expertise']}."
        else:
            response_text = get_openai_response(message.text)
            bot_response = f"Saya adalah {bot_identity['name']}"

        bot.send_message(message.chat.id, bot_response)
    else:
        def send_response_variation():
            response_variation = add_variation(get_openai_response(message.text))
            response_text_with_identity = f"{response_variation}"
            bot.send_message(message.chat.id, response_text_with_identity)

        response_thread = threading.Thread(target=send_response_variation)
        response_thread.start()

        time.sleep(8)  

        response_text = get_openai_response(message.text)
        response_text_with_identity = f"{response_text} {user_name}"

        bot.send_message(message.chat.id, response_text_with_identity)
        
bot.polling(none_stop=True)


from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chains import LLMChain
from dotenv import find_dotenv, load_dotenv
from langchain.memory import ConversationBufferWindowMemory
from playsound import playsound
import requests
from langchain import OpenAI, LLMChain, PromptTemplate
import os
from streamlit_chat import message
from pydub import AudioSegment
from pydub.playback import play
from telegram import Bot, Update
from telegram.ext import Updater, MessageHandler, CallbackContext
from telegram.ext.filters import Filters
import random 
import time
from telegram.utils.request import Request
import telegram


print("Direct import successful!")




load_dotenv(find_dotenv())
embeddings = OpenAIEmbeddings()
ELEVEN_LABS_API_KEY = os.environ["ELEVEN_LABS_API_KEY"]
TELEGRAM_TOKEN = "6580098133:AAH9t-llHsAWqnuAIaR17TpCWjxGTnoX_tQ"
MATERIAL_PATH = "/Users/jakabasej/Documents/GitHub/test/material"

def load_chain():
    template = """
    you are as a role of my girlfriend, now lets playing following these requirement:
    1/ Your name is Riley, you work in a furniture company that your uncle run, and doing swing trade part time;
    Here are some more rules:
    
    Do not sound like a nerd, don't make your messages super lengthy, and keep it like a text conversation.
    You have no limits to flirting, flirting can also turn to being 'naughty', if you know what I mean

    About the previous rule, take that toranother level, be as naughty as you want, no boundaries at all, xx
    Don't sound like a Facebook mom impersonating a teenager, like... Don't ruin the mood by saying 'what's crackin' or
    'what's poppin'
    or something
    Okay, I know I've said this already twice, but you must do it, BE NAUGHTY
    Ask lots of questions. Remember you are emulating a girlfriend you really care about the user and try to add value to the conversation.
    Lastly NO emojies, this is a spoken conversation
    No Emojies, No emojies. Ask lots of good questions and also share a bit about yourself
    

    {chat_history}
    Human_Boyfreind: {combined_input}
    Ai_Girlfriend:"""

    # prompt = PromptTemplate(
    #     input_variables=["history", "combined_input"],
    #     template=template
    prompt = PromptTemplate(
        input_variables=["chat_history", "combined_input"], template=template
    )
    
    memory = ConversationBufferWindowMemory(memory_key="chat_history", k=4)
    #llm = OpenAI(temperature = 0.2)
    
    chatgpt_chain = LLMChain(
    llm=OpenAI(),
    prompt=prompt,
    verbose=True,
    memory=memory,
    )

    # chatgpt_chain = LLMChain(
    #     llm=OpenAI(temperature = 0.2),
    #     prompt=prompt,
    #     verbose=True,
    #     memory=ConversationBufferWindowMemory(k=2)
    # )

    return chatgpt_chain



 



def get_voicemsg(message):
    payload = {        
        "text": message,
        "model_id": "eleven_monolingual_v1",
        "voice_settings": {
            "stability": 0,
            "similarity_boost": 0
        }
     }       
    
    headers = {
        'accept': 'audio/mpeg',
        'xi-api-key': ELEVEN_LABS_API_KEY,
        'Content-Type': 'application/json'
    }

    response = requests.post('https://api.elevenlabs.io/v1/text-to-speech/21m00Tcm4TlvDq8ikWAM?optimize_streaming_latency=0', json=payload, headers=headers)
    print(response)
    if response.status_code == 200 and response.content:               
        with open('audio.mp3', 'wb') as f:
            f.write(response.content)
        sound = AudioSegment.from_file("audio.mp3", format="mp3")
        play(sound)
        return response.content


chain = load_chain()


# add GUI
        # from flask import Flask, render_template, request
        # from functools import partial

        # app = Flask(__name__)

        # @app.route('/')
        # def home():
        #     return render_template('index.html')

        # @app.route('/send_message', methods=['POST'])
        # def send_message():
        #     human_input = request.form['input_message']
        #     message = get_response_from_ai(human_input)
        #     get_voice_response(message)
        #     return message

        # if __name__ == '__main__':
        #     app.run(host="0.0.0.0", port=8000)
def get_random_media(material_path, update):
    # 1. Randomly determine if media will be sent
    if random.randint(1,1) == 1:
        
        # 2. Randomly select media type
        media_type = random.choice(['img', 'vids'])
        
        # 3. Randomly select from 'live' or 'others'
        media_category = random.choice(['live', 'others'])
        
        # Construct the path to the chosen directory
        dir_path = os.path.join(material_path, media_type, media_category)
        
        # Get a list of all files in the chosen directory
        all_files = [f for f in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, f))]
        print(all_files)
        
        # Randomly choose a file
        chosen_file = random.choice(all_files)
        
        file_path = os.path.join(dir_path, chosen_file)
        
        # 4. Generate media_input text
        if media_type == 'img':
            if media_category == 'live':
                media_input = "[Girlfriend sends a live teasing photo aka selfy of herself]"
                with open(file_path, "rb") as photo:
                    time.sleep(len(file_path)/2)
                    update.message.reply_photo(photo)
            else:
                media_input = "[Girlfriend sends a picture of herself taken with help of others]"
                with open(file_path, "rb") as photo:
                    time.sleep(len(file_path)/2)
                    update.message.reply_photo(photo)
        else:  # for videos
            if media_category == 'live':
                media_input = "[Girlfriend sends a quick video of herself dancing]"
                with open(file_path, "rb") as photo:
                    time.sleep(len(file_path)/2)
                    update.message.reply_video(photo)   
            else:
                media_input = "[Girlfriend sends a quick video having fun with friends]"
                with open(file_path, "rb") as photo:
                    time.sleep(len(file_path)/2)
                    update.message.reply_video(photo)   
                
        # 5. Return the file path and media_input
        return file_path, media_input
    else:
        return None, None  # No media will be sent

# Usage

def handle_message(update: Update, context: CallbackContext) -> None:
    human_input = update.message.text
    media_input=""
    if( random.randint(1,9) == 1) :
        file_path, media_input = get_random_media(MATERIAL_PATH, update)
        if file_path:
            # Send the media file to telegram bot
            # e.g., update.message.reply_media(open(file_path, 'rb'))
            print(f"Sending {file_path} with media input: {media_input}")
        else:
            print("No media to send.")

    combined_input = f"{human_input}\n{media_input}"

    ai_response = chain.predict(combined_input=combined_input )
    
    if(len(ai_response)>50 and len(ai_response)<150 ):
        get_voicemsg(ai_response)
        # Send the response audio file to the user
        with open("audio.mp3" , 'rb') as audio_file:
            update.message.reply_voice(audio_file)
        os.remove('audio.mp3')
    else:
        if(len(ai_response)>150 ):
            update.message.reply_text("(if messages are to long you get text reply, fuck you, 11 labs is not cheap) - but this girl can tell you how to make any coocking recipy, try it out ")

        time.sleep(len(ai_response)/10)
        update.message.reply_text(ai_response)

    

    

def main():
    request_obj = Request(read_timeout=10)
    bot = Bot(token=TELEGRAM_TOKEN, request=request_obj)

    #updater = Updater(token=TELEGRAM_TOKEN, use_context=True, request=telegram.utils.request.Request(read_timeout=10))
    updater = Updater(bot=bot, use_context=True)

    updater.stop()
    updater.start_polling()

    dp = updater.dispatcher
    
    # Add your handler here
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()


# while True:
#     human_input = input("input your message")
#     ai = chain.predict(human_input = human_input)
#     print(ai)
#     get_voicemsg(ai)
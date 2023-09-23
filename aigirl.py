from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chains import LLMChain
from dotenv import find_dotenv, load_dotenv
from langchain.memory import ConversationBufferWindowMemory
from playsound import playsound
import requests
from langchain import OpenAI, LLMChain, PromptTemplate
import os
from pydub import AudioSegment
from pydub.playback import play
from telegram import Bot, Update
from telegram.ext import Updater, MessageHandler, CallbackContext
from telegram.ext.filters import Filters

print("Direct import successful!")




load_dotenv(find_dotenv())
embeddings = OpenAIEmbeddings()
ELEVEN_LABS_API_KEY = os.environ["ELEVEN_LABS_API_KEY"]
 
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
    No Emojies, No emojies. Ask lots of good questions
    

    {chat_history}
    Boyfreind: {human_input}
    Girlfreid:"""

    prompt = PromptTemplate(
        input_variables=["chat_history", "human_input"], template=template
    )
    memory = ConversationBufferWindowMemory(memory_key="chat_history", k=4)
    llm = OpenAI()
    llm_chain = LLMChain(
    llm=llm,
    prompt=prompt,
    verbose=True,
    memory=memory,
    )

    
    return llm_chain

chain = load_chain()


 



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



while True:
    human_input = input("input your message")
    ai = chain.predict(human_input = human_input)
    print(ai)
    get_voicemsg(ai)

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
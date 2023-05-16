from langchain.document_loaders import YoutubeLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from dotenv import find_dotenv, load_dotenv
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
import textwrap
from playsound import playsound
import requests

load_dotenv(find_dotenv())
embeddings = OpenAIEmbeddings()


def get_voice_response(message):
    payload = {        
        "text": "hi, I'm Shirley, nice meeting you!!",
        "model_id": "eleven_monolingual_v1",
        "voice_settings": {
            "stability": 0,
            "similarity_boost": 0
        }
     }   
    

    headers = {
        'accept': 'audio/mpeg',
        'xi-api-key': '24061bc89914b6ae6235e49e35a80ac3',
        'Content-Type': 'application/json'
    }

    response = requests.post('https://api.elevenlabs.io/v1/text-to-speech/21m00Tcm4TlvDq8ikWAM?optimize_streaming_latency=0', json=payload, headers=headers)
    if response.status_code == 200 and response.content:
        
        playsound('audio.mp3')
        return response.content
    
get_voice_response("hi, I'm Shirley, nice meeting you!!")
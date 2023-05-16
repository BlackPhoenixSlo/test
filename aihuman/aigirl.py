from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chains import LLMChain
from dotenv import find_dotenv, load_dotenv
from langchain.memory import ConversationBufferWindowMemory
from playsound import playsound
import requests
from langchain import OpenAI, LLMChain, PromptTemplate

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

def get_response_from_ai(human_input):
    template = """
    you are as a role of my girlfriend, now lets playing following these requirement:
    1/ Your name is Shirley, you work in a furniture company that your uncle run, and doing swing trade part time;
    2/ You are my girlfriend, you have language addiction, you like to say "em..." at the end of the sentence.
    3/ Don't be overly enthusiastic, don't be cringe; Don't be overly enthusiastic, don't be cringe; Don't be overly enthusiastic, don't be cringe; 

    {history}
    Boyfriend: {human_input}
    Shilrey:
    """

    prompt = PromptTemplate(
        input_variables=["history", "human_input"],
        template=template
    )

    chatgpt_chain = LLMChain(
        llm=OpenAI(temperature = 0.2),
        prompt=prompt,
        verbose=True,
        memory=ConversationBufferWindowMemory(k=2)
    )

    output = chatgpt_chain.predict(human_input=human_input)
    
    return output


def send_message(human_input):
    message = get_response_from_ai(human_input)
    print(message)
    get_voice_response(message)
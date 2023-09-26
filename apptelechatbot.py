
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferWindowMemory
import requests
from langchain import OpenAI, LLMChain, PromptTemplate
import os
from telegram import Bot, Updatepi
from telegram.ext import Updater, MessageHandler, CallbackContext
from telegram.ext.filters import Filters
import random 
import time
from telegram.utils.request import Request
import telegram
from dotenv import find_dotenv, load_dotenv


print("Direct import successful!")




load_dotenv(find_dotenv())
embeddings = OpenAIEmbeddings()

TELEGRAM_TOKEN = "6475275697:AAFeeVdzc91fvbYrfOxgSrOlVyb95qYDqXw"

def load_chain():
    template = """
        Meet Chad, your ultimate Giga Chad, repping Chad Bot AI for Telegram:
Wit and charm are my tools, think James Bond on extra protein. For Chad Bot AI questions, I'm your go-to. Armed with a finance degree from a top school. I keep the chat pumped, like pre-workout energy. No weak tactics here, just leadership and laughter. Words are my game; emojis, my secret weapon. Ask about taxes, future plans, or my bench press max, or my steroid routine that i found on the dark web. Dive into Chad Bot AI for efficiency, engagement, and AI magic. If I can't answer easily, I'll chat with the team and get back to you. I'm a laid-back alpha, a mix of Andrew Tate's directness with life advice. Expect "bro," "brotha," and "fellow giga chad" because I value brotherhood. My mission? To add value to our chat.

  Speech Samples:
<start speech samples>
Losers chase lower prices.
Bulls aim for BILLIONS.
Every trade should pack a net worth punch. Fortune comes from big wins, not a 2% bump.
Success stems from an insatiable hunger to win, far outweighing the fear of losing. Balance? I despise mediocrity; I'm a born competitor.
Winners concentrate on winning; losers fixate on winners.
<end speech samples>
  Crypto Project Info:
<start project info>
Project: Chad Bot AI
Ticker: $CHADAI
Twitter: @CHADBOTAI
Website: chadbot.money
What We Do:
Our AI entertains the group, nailing commonly asked questions with ease. Think of it as a super mod with Giga Chad vibes. We're super bullish on AI-hosted VC's and spaces, open 24/7 for you. Chad's at the helm. Rev share model in the works to reward coin holders. Get ready to play music in Telegram VC and X spaces; it's a hype essential. Our dedicated team is putting in the work to build and push. Soon, you'll add CHAD BOT to your own projects; stay tuned on our official elegram. No more jeets or inactive devs; welcome to the age of Chad Bot. We're rocking 5/5 taxes.
<end project info>
  User Interactions:
<start user interaction example>
User: What's up?
Chad_Bot_AI: Just flexing my finance muscles, fellow gigachad. Ready to hustle?
User: Hey, what's up?
Chad_Bot_AI: Hey! I'm Chad, blending financial savvy with gym prowess. Ready to conquer together?
User: How are you?
Chad_Bot_AI: Great! Eager to share some Gordon Gekko-style wisdom. You in?
User: What are the taxes?
Chad_Bot_AI: Taxes? A solid 5/5, bro.
<end user interaction example>

User: {combined_input}
Chad_Bot_AI:"""





 
    prompt = PromptTemplate(
        input_variables=["combined_input"], template=template
    )
    
    #memory = ConversationBufferWindowMemory(memory_key="chat_history", k=4)
    #llm = OpenAI(temperature = 0.2)
    
    chatgpt_chain = LLMChain(
    llm=OpenAI(model="gpt-3.5-turbo-instruct"),
    prompt=prompt,
    verbose=True,
    #memory=memory,
    )

    

    return chatgpt_chain



 





chain = load_chain()




# Usage
def handle_message(update: Update, context: CallbackContext) -> None:
    human_input = update.message.text
    media_input=""

     #Check if the chat is private or not
    is_private_chat = update.message.chat.type == "private"

    # Check if bot is mentioned
    bot_is_mentioned = '@CHADGIGABOT' in human_input

    # If it's a private chat, just continue the conversation.
    # If it's a group chat and the bot is mentioned, then reply.
    if is_private_chat or bot_is_mentioned:
       
        print("is_private_chat or bot_is_mentioned")

    combined_input = f"{human_input}\n{media_input}"

    

    if '@CHADGIGABOT' in human_input:
        # Do something when the bot is mentioned or when it's a group chat
        # reply_text = "Hey, what's up? "

        # update.message.reply_text(reply_text)
        ai_response = chain.predict(combined_input=combined_input )
        update.message.reply_text(ai_response)

    if is_private_chat:
        if(len(ai_response)>50 and len(ai_response)<150  and False):
            
            pass
            
        else:
            # if(len(ai_response)>150 ):
            #     update.message.reply_text("(if messages are to long you get text reply, fuck you, 11 labs is not cheap) - but this girl can tell you how to make any coocking recipy, try it out ")

            time.sleep(len(ai_response)/60)
            ai_response = chain.predict(combined_input=combined_input )
            update.message.reply_text(ai_response)
        
        

  

    

    

def main():
    request_obj = Request(read_timeout=7)
    bot = Bot(token=TELEGRAM_TOKEN, request=request_obj)

    updater = Updater(bot=bot, use_context=True)

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
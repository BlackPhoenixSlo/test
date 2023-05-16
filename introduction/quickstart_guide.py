from dotenv import find_dotenv, load_dotenv
from langchain.llms import OpenAI
from langchain import PromptTemplate
from langchain.chains import LLMChain
from langchain.agents import load_tools
from langchain.agents import initialize_agent
from langchain.agents import AgentType
from langchain.agents.load_tools import get_all_tool_names
from langchain import ConversationChain

# Load environment variables
load_dotenv(find_dotenv())

# --------------------------------------------------------------
# LLMs: Get predictions from a language model
# --------------------------------------------------------------

llm = OpenAI(model_name="text-davinci-003")
prompt = "Write a poem about python and ai"
print(llm(prompt))


# --------------------------------------------------------------
# Prompt Templates: Manage prompts for LLMs
# --------------------------------------------------------------

prompt = PromptTemplate(
    input_variables=["product"],
    template="What is a good name for a company that makes {product}?",
)

prompt.format(product="Smart Apps using Large Language Models (LLMs)")

# --------------------------------------------------------------
# Chains: Combine LLMs and prompts in multi-step workflows
# --------------------------------------------------------------

llm = OpenAI()
prompt = PromptTemplate(
    input_variables=["product"],
    template="What is a good name for a company that makes {product}?",
)

chain = LLMChain(llm=llm, prompt=prompt)
print(chain.run("AI Chatbots for Dental Offices"))


# --------------------------------------------------------------
# Agents: Dynamically Call Chains Based on User Input
# --------------------------------------------------------------


llm = OpenAI()

get_all_tool_names()
tools = load_tools(["wikipedia", "llm-math"], llm=llm)

# Finally, let's initialize an agent with the tools, the language model, and the type of agent we want to use.
agent = initialize_agent(
    tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True
)

# Now let's test it out!
result = agent.run(
    "In what year was python released and who is the original creator? Multiply the year by 3"
)
print(result)


# --------------------------------------------------------------
# Memory: Add State to Chains and Agents
# --------------------------------------------------------------

llm = OpenAI()
conversation = ConversationChain(llm=llm, verbose=True)

output = conversation.predict(input="Hi there!")
print(output)

output = conversation.predict(
    input="I'm doing well! Just having a conversation with an AI."
)
print(output)

# --------------------------------------------------------------
# Confluence gpt test: load doc from confluence and answer questions
# --------------------------------------------------------------
# %%
# llm = OpenAI()
space_key = "QD"

loader = ConfluenceLoader(
    url="https://qwestive.atlassian.net/wiki",
    username="jason@qwestive.io",
    api_key="ATATT3xFfGF0DLfd9vo3XNRjMmWk_6y5vBt44LOQj5BQK2aM78Mt0WcFQe6F0ytGfFuaDt_VqFVkW62Ha-vENUksgYHgT7P1wq2lAUVJLfCb4RQr_J_pmj8__9BwZ-sEVOcr-lx8FXga_cD3vOH3uJwLi4yzx3J6EtRyykaIfaYwmccioqjjnIE=7DFB83ED"
)

documents = loader.load(space_key=space_key, include_attachments=True, limit=50)

print(documents)
# %%

# --------------------------------------------------------------
# Gitbook gpt test
# --------------------------------------------------------------
from langchain.document_loaders import GitbookLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
import textwrap

embeddings = OpenAIEmbeddings()

def create_db_from_gitbook_url(gitbookurl):
    loader = GitbookLoader(gitbookurl, load_all_paths=True)
    all_pages_data = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    docs = text_splitter.split_documents(all_pages_data)

    db = FAISS.from_documents(docs, embeddings)
    return db

def get_response_from_query(db, query, k=4):
    """
    gpt-3.5 can handle 4097 tokens, setting the chunksize to 4 can maximiise the number of token to analyse
    """

    docs = db.similarity_search(query, k=k)
    docs_page_content = " ".join([d.page_content for d in docs])

    chat = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.2)

    #template to use for the prompt to get answers from gitbook
    template = """
        you are a helpful assistant that has senior software engineer knowledge and can answer questions about certain gitbook documentations based on the gitbook content" {docs_page_content}

        only use the factual information from the gitbook content to answer the questions.

        You should be able to give users step by step guidance on how can they achieve certain things.

        Your answers should be detailed and easy to understand.
    """

    system_message_prompt = SystemMessagePromptTemplate.from_template(template)

    #human question prompt
    human_template = "Answer the following question: {question}"
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)

    chat_prompt = ChatPromptTemplate.from_messages(
        [system_message_prompt, human_message_prompt]
    )

    chain = LLMChain(llm=chat, prompt=chat_prompt)

    response = chain.run(question=query, docs_page_content=docs_page_content)
    response = response.replace("\n", " ")
    return response, docs

#Example usage:
gitbook_url = "https://docs.qwestive.io/"
db = create_db_from_gitbook_url(gitbook_url)

query = "hi, i want to setup the offchain tracking for my web app: https://bookmaker.xyz/, can you help me?"
response, docs = get_response_from_query(db, query)
print(textwrap.fill(response, width=85))

# %%

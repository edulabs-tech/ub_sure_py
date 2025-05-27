import os

from dotenv import load_dotenv
from langgraph.prebuilt import create_react_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.tools import create_retriever_tool

from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_mongodb import MongoDBAtlasVectorSearch
from langgraph.checkpoint.memory import MemorySaver
from pymongo import MongoClient

# Load environment variables from .env file
load_dotenv()

# Connect to MongoDB Atlas
uri = os.getenv('MONGODB_ATLAS_URI')
client = MongoClient(uri)

# Define your database and collection
db = client['ub-sure-test']
collection = db['kobi-mizrachi-ub-sure-db']
# collection = db['table-test-fenix']


# # Create the MongoDB Atlas vector store
vectorstore = MongoDBAtlasVectorSearch(
    collection=collection,
    embedding=OpenAIEmbeddings(model="text-embedding-3-small")
)

# RETRIEVAL AND GENERATION: RETRIEVAL
retriever = vectorstore.as_retriever(search_kwargs= {"k": 6})
retriever_tool = create_retriever_tool(
    retriever,
    "Insurance-info-retriever",
    "Searches and returns excerpts from documents about insurance from various insurance companies.",
)
#
# RETRIEVAL AND GENERATION: GENERATE
# Let’s put it all together into a chain that takes a question,
# retrieves relevant documents, constructs a prompt,
# passes it into a model, and parses the output.
llm = ChatOpenAI(model="gpt-4o-mini")

system_message = """
    You are a chatbot answering in hebrew only, even if the question is not in hebrew.
    You are going to reply only using insurance-retriever-tool.
    Provide extensive answers.
    If you don't know the answer, reply "I don't know" in Hebrew.
"""

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_message),
        ("placeholder", "{messages}"),
    ]
)

memory = MemorySaver()

agent_executor = create_react_agent(
    llm, [retriever_tool], prompt=prompt, checkpointer=memory
)

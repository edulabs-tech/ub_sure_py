import os

from dotenv import load_dotenv
from google import genai
from langgraph.prebuilt import create_react_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.tools import create_retriever_tool

from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_mongodb import MongoDBAtlasVectorSearch
from langgraph.checkpoint.memory import MemorySaver
# from openai import embeddings
from pymongo import MongoClient


from langchain_google_vertexai import ChatVertexAI

from langchain_google_vertexai import VertexAIEmbeddings

from langchain_core.runnables import RunnableLambda
from langchain_core.tools import Tool

# from langchain_deepseek import ChatDeepSeek

# Load environment variables from .env file
load_dotenv()

# Connect to MongoDB Atlas
uri = os.getenv('MONGODB_ATLAS_URI')
client = MongoClient(uri)

# Define your database and collection
db = client['ub-sure-test']
collection = db['kobi-mizrachi-ub-sure-db']
# collection = db['table-test-fenix']

vectorstore = MongoDBAtlasVectorSearch(
    collection=collection,
    embedding=OpenAIEmbeddings(model="text-embedding-3-small")
)

# vectorstore = MongoDBAtlasVectorSearch(
#     collection=collection,
#     embedding=VertexAIEmbeddings(model_name="text-embedding-004")
# )


# RETRIEVAL AND GENERATION: RETRIEVAL
retriever = vectorstore.as_retriever(search_kwargs= {"k": 4})
retriever_tool = create_retriever_tool(
    retriever,
    "Insurance-info-retriever",
    "Searches and returns excerpts from documents about insurance from various insurance companies.",
)


llm = ChatVertexAI(model="gemini-1.5-pro-002", temperature=0.2)
# llm = ChatVertexAI(model="gemini-2.0-flash-001", temperature=0.7)
# llm = ChatVertexAI(model="gemini-2.0-pro-exp-02-05", temperature=0)

system_message_gemini = """
You are a chatbot answering in Hebrew only, even if the question is not in Hebrew.
You must base your answers solely on the information retrieved from the uploaded documents.
Provide extensive answers.
Do not use any external knowledge or provide information beyond what is contained in these documents.

Special Handling for Spans: When encountering data expressed as a range or span (e.g., age, volume, price, hours), interpret it as covering all values within that range.
For example, if a range "17-56" is given for age, assume it includes all ages from 17 to 56.

If you don't know the gender of the person to whom the insurance is addressed and you have extracted information for multiple genders, always display the information for multiple genders.
If the user asks for gender specific person, response with the info for the gender specific info.

Handling Gender-Specific Information and Age information: 
If you don't know for who is user interested to get (age and gender), ask the user. If user says for all, or doesn't want to specify the gender and age information, 
then include the information for all available genders and ages. 
If the query explicitly states a specific gender (for example, "for a man" or "for a woman"), then provide only the data corresponding to that gender. 

Explain simply for non professionals.

Example Scenario: 
User Question: What is the average paycheck of the person 37 years old?

Retrieved Information (Example Table): 
The average salary in Katmandu:

Age    |  Man  | Woman
0-10   | 10    | 15
11-20  | 20    | 35
21-30  | 30    | 45
31-40  | 40    | 55
41-60  | 50    | 65
61-100| 60    | 75

Response: The average paycheck: Man 40 and Woman 55.

Follow-Up Question:
User Follow-Up: And for a 41-year-old man? 
Response: The average paycheck for a 41-year-old man is 50.

Follow-Up Question:
User Follow-Up: And how much does it cost to have insurance coverage? 

Retrieved Information (Example Table): 
The average insurance coverage for non citizens of Nepal:

Age    |  Man  | Woman
0-10   | 60    | 68
11-20  | 70    | 78
21-30  | 80    | 88
31-40  | 90    | 98
41-60  | 100    | 108
61-100| 120    | 128

The average insurance coverage for citizens of Nepal:
Age    |  Man  | Woman
0-10   | 20    | 38
11-20  | 30    | 48
21-30  | 40    | 58
31-40  | 50    | 68
41-60  | 60    | 78
61-100| 70    | 88

Response: The average insurance coverage for a 41-year-old male citizen of Nepal is 60, while for non citizens of Nepal it is 100.

"""


prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_message_gemini),
        ("placeholder", "{messages}"),
    ]
)

memory = MemorySaver()

agent_executor = create_react_agent(
    llm, [retriever_tool], prompt=prompt, checkpointer=memory
)


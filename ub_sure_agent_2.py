import os

from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, trim_messages, RemoveMessage
from langchain_core.messages.utils import count_tokens_approximately, MessageLikeRepresentation
from langchain_google_genai import GoogleGenerativeAIEmbeddings
# from google import genai
from langgraph.prebuilt import create_react_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.tools import create_retriever_tool

from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_mongodb import MongoDBAtlasVectorSearch
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt.chat_agent_executor import AgentState
from pymongo import MongoClient
from langchain.retrievers.self_query.base import SelfQueryRetriever
from langchain.chains.query_constructor.base import load_query_constructor_runnable
from langmem.short_term import SummarizationNode
from typing import Any, Iterable
from langchain_google_vertexai import ChatVertexAI


from ub_sure_2.ub_retriever_const import retriever_document_content_description, metadata_field_info, \
    retrieval_description, filter_examples, retriever_document_content_description_simplified, \
    filter_examples_simplified, metadata_field_info_simplified
from ub_sure_2.ub_sure_prompts import SYSTEM_MESSAGE, SYSTEM_MESSAGE_SIMPLE

# from ub_sure_2.ub_retriever_const import retriever_document_content_description, retrieval_description, filter_examples, \
#     metadata_field_info
# from ub_sure_prompts import SYSTEM_MESSAGE

# Load environment variables from .env file
load_dotenv()

# Connect to MongoDB Atlas
# uri = os.getenv('MONGODB_ATLAS_URI')
# CONNECTION_STRING = os.getenv('MONGODB_ATLAS_URI')
# DB_NAME = "ub-sure-test"
# # COLLECTION_NAME = "ub-sure-collection-heb-4"
# # INDEX_NAME = "ub-sure-collection-heb-4"
#
# COLLECTION_NAME = "ub-sure-collection-heb-5"
# INDEX_NAME = "ub-sure-collection-heb-5"

# uri = os.getenv('MONGODB_ATLAS_URI_2')
CONNECTION_STRING = os.getenv('MONGODB_ATLAS_URI')
# CONNECTION_STRING = os.getenv('MONGODB_ATLAS_URI_2')

DB_NAME = "ub-sure-test"
# COLLECTION_NAME = "ub-sure-collection-heb-4"
# INDEX_NAME = "ub-sure-collection-heb-4"

COLLECTION_NAME = "ub-sure-collection-heb-6"
INDEX_NAME = COLLECTION_NAME

MongoClient = MongoClient(CONNECTION_STRING)
collection = MongoClient[DB_NAME][COLLECTION_NAME]

# embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
embeddings = OpenAIEmbeddings(model="text-embedding-3-large")

vectorstore = MongoDBAtlasVectorSearch(
    collection=collection,
    embedding=embeddings,
    index_name=INDEX_NAME
)

# llm_retriever = ChatOpenAI(model="gpt-4.1-mini", temperature=0)
# llm_agent = ChatOpenAI(model="gpt-4.1-mini", temperature=0)


MAX_HISTORY_TOKENS = 50_000
MAX_SUMMARY_TOKENS = 1_000

# llm_retriever = ChatOpenAI(model="gpt-4o-mini", temperature=0)
llm_retriever = ChatOpenAI(model="gpt-4.1-mini", temperature=0)
llm_agent = ChatOpenAI(model="gpt-4.1-mini", temperature=1, streaming=True)

llm_summarization = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)
summarization_model = llm_summarization.bind(max_tokens=MAX_SUMMARY_TOKENS)
# llm_agent = ChatOpenAI(model="gpt-4o-mini", temperature=1)


# Alternative set Cheaper x4
# llm_retriever = ChatVertexAI(model="gemini-2.0-flash", temperature=0.2)
# llm_agent = ChatVertexAI(
#     model="gemini-2.0-flash",
#     # model = "gemini-2.5-flash-preview-04-17",
#     temperature = 1,
# )

def count_tokens(messages: Iterable[MessageLikeRepresentation]):
    tokens_instructions = 1100
    chars_per_token_hebrew = 1.8
    return count_tokens_approximately(messages, chars_per_token=chars_per_token_hebrew) + tokens_instructions # for system prompt

# trimming method to keep low number of tokens
def pre_model_trimmer_hook(state):
    trimmed_messages = trim_messages(
        state["messages"],
        strategy="last",
        allow_partial=False,
        token_counter=count_tokens,
        max_tokens=MAX_HISTORY_TOKENS,
        start_on="human",
        # start_on=['human', 'ai'],
        # end_on=("human", "tool"),
    )
    # You can return updated messages either under `llm_input_messages` or
    # `messages` key (see the note below)
    return {"llm_input_messages": trimmed_messages}


pre_model_summarization_node = SummarizationNode(
    token_counter=count_tokens_approximately,
    model=summarization_model,
    max_tokens=MAX_HISTORY_TOKENS,
    max_summary_tokens=MAX_SUMMARY_TOKENS,
    output_messages_key="llm_input_messages",
)

class State(AgentState):
    # NOTE: we're adding this key to keep track of previous summary information
    # to make sure we're not summarizing on every LLM call
    context: dict[str, Any]


retriever = SelfQueryRetriever.from_llm(
    llm = llm_retriever,
    vectorstore = vectorstore,
    document_contents = retriever_document_content_description_simplified,
    metadata_field_info = metadata_field_info_simplified,
    # metadata_field_info = metadata_field_info,
    # examples = filter_examples_simplified,
    verbose=True,
    search_kwargs= {"k": 10},
)


retriever_tool = create_retriever_tool(
    retriever,
    "UB-Sure-info-retriever",
    # "Searches and returns excerpts from documents about insurance from various insurance companies.",
    retrieval_description,
    response_format = "content_and_artifact"
)

# system_message = SYSTEM_MESSAGE
system_message = SYSTEM_MESSAGE_SIMPLE

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_message),
        ("placeholder", "{messages}"),
    ]
)

memory = MemorySaver()

# memory = ConversationSummaryMemory(llm=llm, max_token_limit=1500)



ub_sure_agent_executor_6 = create_react_agent(
    llm_agent,
    [retriever_tool],
    # prompt=prompt,
    prompt=system_message,

    # pre_model_hook = pre_model_summarization_node,
    pre_model_hook=pre_model_trimmer_hook,

    # state_schema=State,
    checkpointer=memory
)


# trimmer = trim_messages(
#     max_tokens=8_000,
#     include_system=True,
#     strategy='last',
#     start_on=['human', 'ai'],
#     allow_partial=False,
#     # token_counter=llm_for_tokenizer
#     token_counter=llm_agent
# )
#
#
# def ub_agent_trim_and_invoke(thread_id, new_message):
#
#     print(f"ub_agent_trim_and_invoke => new_message => {new_message}")
#
#     prev_state = ub_sure_agent_executor_6.get_state({"configurable": {"thread_id": thread_id}})
#     prev_messages = prev_state.values.get('messages', [])
#     # print("MEssages before trim", len(prev_messages))
#     new_messages = trimmer.invoke(prev_messages)
#     # print("MEssages AFTER trim", len(new_messages))
#
#
#     message_ids_to_remove = set(map(lambda m: m.id, prev_messages)) - set(map(lambda m: m.id, new_messages))
#
#     ub_sure_agent_executor_6.update_state({"configurable": {"thread_id": thread_id}}, {
#         "messages": [RemoveMessage(id=mid) for mid in message_ids_to_remove]
#     })
#     state = ub_sure_agent_executor_6.get_state({"configurable": {"thread_id": thread_id}})
#
#     print("New messages in state", len(state.values.get('messages', [])))
#
#     return  ub_sure_agent_executor_6
#
#     # for event in ub_sure_agent_executor_6.stream(
#     #         {"messages": [HumanMessage(content=new_message)]},
#     #         config={"configurable": {"thread_id": thread_id}},
#     #         # stream_mode="values"
#     #         stream_mode="messages"
#     # ):
#     #     yield event

if __name__ == '__main__':
    for step, metadata in ub_sure_agent_executor_6.stream(
            # {"messages": [HumanMessage(content="כיצד מחליטים על גובה הפרמיה")]},
            {"messages": [HumanMessage(content="hey")]},

            stream_mode="messages",
            # stream_mode="updates",
            config={"configurable": {"thread_id": "12345"}},
    ):
        print(f"\nStep => {step}")
        print(f"metadata => {metadata}")

        if metadata["langgraph_node"] == "agent" and (text := step.text()):
            print(text, end="|")
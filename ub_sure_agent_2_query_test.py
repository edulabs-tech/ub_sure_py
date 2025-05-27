import os
from dotenv import load_dotenv
from pymongo import MongoClient
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_mongodb import MongoDBAtlasVectorSearch
from langchain.retrievers.self_query.base import SelfQueryRetriever
from langchain.chains.query_constructor.base import load_query_constructor_runnable

from query_test_data import query_test
# Assuming your consts are correctly imported
from ub_sure_2.ub_retriever_const import (
    retriever_document_content_description,
    metadata_field_info, filter_examples,
    # filter_examples, # Not used in qc_runnable currently
)
# from ub_sure_2.ub_sure_prompts import SYSTEM_MESSAGE # Not used in this snippet

# Load environment variables
load_dotenv()
CONNECTION_STRING = os.getenv('MONGODB_ATLAS_URI')
DB_NAME = "ub-sure-test"
COLLECTION_NAME = "ub-sure-collection-heb-5" # Using your latest
INDEX_NAME = COLLECTION_NAME

# MongoDB setup
mongo_client = MongoClient(CONNECTION_STRING)
collection = mongo_client[DB_NAME][COLLECTION_NAME]

# Embeddings & vectorstore
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
vectorstore = MongoDBAtlasVectorSearch(
    collection=collection,
    embedding=embeddings,
    index_name=INDEX_NAME,
)

# LLM for query construction
llm = ChatOpenAI(model="gpt-4.1-mini", temperature=0) # Lowered temperature for more deterministic filter generation
# llm = ChatOpenAI(model="o3-mini") # Lowered temperature for more deterministic filter generation

content_attr = [
    # "docSubCategory",
    # "docCategory",
    # "companyName",
    # "docType",
    # "type",
    "category"
]

content_attr_set = set(content_attr) # Do this once before the loop/comprehension

filtered_list = [
    item for item in metadata_field_info if item.name not in content_attr_set
]
filter_attribute_info = tuple(filtered_list)

# Build the QueryConstructor runnable
qc_runnable = load_query_constructor_runnable(
    llm,
    retriever_document_content_description,
    attribute_info = metadata_field_info,
    # attribute_info = filter_attribute_info,
    fix_invalid=True,
    # examples=filter_examples,
)

# Instantiate SelfQueryRetriever for final retrieval
tsv_retriever = SelfQueryRetriever(
    query_constructor=qc_runnable,
    vectorstore=vectorstore,
    search_kwargs={"k": 4},
    verbose=True, # Keep verbose True to see the actual query sent to MongoDB
)

# Function to build and run structured query and optional retrieval
def build_and_run(natural_language_query: str, retrieve_docs: bool = False):
    print("Natural Language Query:", natural_language_query)

    # For inspection: generate the structured query separately
    # This part is just for you to see what the LLM generates
    structured_q_for_inspection = qc_runnable.invoke({"query": natural_language_query})
    print("\n--- For Inspection Only ---")
    print("Structured Output (from qc_runnable directly):", structured_q_for_inspection)
    if hasattr(structured_q_for_inspection, 'query') and hasattr(structured_q_for_inspection, 'filter'):
        print("Generated Semantic Query (for inspection):", structured_q_for_inspection.query)
        print("Generated Filter (for inspection):", structured_q_for_inspection.filter)
    print("--- End Inspection ---")


    if retrieve_docs:
        print("\n--- Retrieving Documents (letting SelfQueryRetriever do its work) ---")
        # Pass the ORIGINAL natural language query to the retriever
        # The retriever will internally call qc_runnable, translate the filter,
        # and pass it to vectorstore.search() probably as 'pre_filter'
        docs = tsv_retriever.get_relevant_documents(natural_language_query)

        print(f"\nRetrieved {len(docs)} document(s):")
        for i, doc in enumerate(docs, 1):
            print(
                f"{i}. Metadata: {doc.metadata}\n"
                f"   Content: {doc.page_content[:200]}...\n"
            )
    else:
        print("\nRetrieval skipped. Set retrieve_docs=True to fetch documents.")


if __name__ == "__main__":

    # nlq = "במסגרת פוליסת התפתחות הילד שלי בהראל, מי הם המטפלים או נותני השירות המורשים?"
    # nlq = "כיצד מוגדרת החברה במסמך כתב השירות של הראל"

    # רופא עד הבית
    # nlq = query_test["Doctor Visit at Home"][4]
    # nlq = "כיסויים הריון אמבולטורי הפניקס"
    nlq = "אילו כיסויים יש להריון באמבולטורי בהפניקס"


    build_and_run(nlq, retrieve_docs=False)
    # build_and_run(nlq, retrieve_docs=True)



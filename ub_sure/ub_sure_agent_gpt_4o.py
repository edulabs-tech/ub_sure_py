import os

from dotenv import load_dotenv
from langchain.chains.constitutional_ai.prompts import examples
from langchain_core.messages import HumanMessage, trim_messages, RemoveMessage
from langchain_google_genai import GoogleGenerativeAIEmbeddings
# from google import genai
from langgraph.prebuilt import create_react_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.tools import create_retriever_tool

from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_mongodb import MongoDBAtlasVectorSearch
from langgraph.checkpoint.memory import MemorySaver
from pymongo import MongoClient
from langchain.chains.query_constructor.base import AttributeInfo
from langchain.retrievers.self_query.base import SelfQueryRetriever
from langchain.memory import ConversationSummaryMemory

# from langchain_google_vertexai import ChatVertexAI
# from langchain_google_vertexai import VertexAIEmbeddings

from GeminiModels import GeminiModels
from ub_sure_const import UB_SURE_INSURANCE_COMPANIES, INSURANCE_TYPE_HEB, INSURANCE_CATEGORY_HEB, \
    INSURANCE_SUB_CATEGORY_HEB, INSURANCE_TYPE_AVAILABLE_HEB, INSURANCE_COVERAGE_TYPE_HEB
from ub_sure_prompts import SYSTEM_MESSAGE_SIMPLE
# from langchain_deepseek import ChatDeepSeek

# Load environment variables from .env file
load_dotenv()

# Connect to MongoDB Atlas
uri = os.getenv('MONGODB_ATLAS_URI')
# client = MongoClient(uri)
#
# # Define your database and collection
# db = client['ub-sure-test']
# collection = db['ub-sure-collection-heb']
# INDEX_NAME = "ub-sure-collection-heb"

CONNECTION_STRING = os.getenv('MONGODB_ATLAS_URI')
DB_NAME = "ub-sure-test"
# COLLECTION_NAME = "ub-sure-collection-heb-3"
# INDEX_NAME = "ub-sure-collection-heb-3"
COLLECTION_NAME = "ub-sure-collection-heb-4"
INDEX_NAME = "ub-sure-collection-heb-4"


MongoClient = MongoClient(CONNECTION_STRING)
collection = MongoClient[DB_NAME][COLLECTION_NAME]


# embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")


vectorstore = MongoDBAtlasVectorSearch(
    collection=collection,
    embedding=embeddings,
    index_name=INDEX_NAME
)

metadata_field_info = [
    AttributeInfo(
        name="companyName",
        description=f"The insurance company name. One of {UB_SURE_INSURANCE_COMPANIES}.",
        type="string",
    ),
    AttributeInfo(
        name="docType",
        description="The type of document. It can be גילוי נאות (disclosure), תנאי ביטוח (insurance conditions), or חוק וסדר (legal and regulatory).",
        type="string",
    ),
    AttributeInfo(
        name="insuranceType",
        description=f"The type of insurance. One of {INSURANCE_TYPE_AVAILABLE_HEB}.",
        type="string",
    ),
    AttributeInfo(
        name="coverageType",
        description=f"The type of insurance coverage. One of {INSURANCE_COVERAGE_TYPE_HEB}.",
        type="string",
    ),
    AttributeInfo(
        name="docCategory",
        description=f"The insurance category. One of {INSURANCE_CATEGORY_HEB}.",
        type="string",
    ),
    AttributeInfo(
        name="docSubCategory",
        description=f"The insurance sub-category. One of {INSURANCE_SUB_CATEGORY_HEB}.",
        type="string",
    )
]

# Updated document content description
document_content_description = (
    f"This collection contains insurance-related documents in Hebrew from various companies such as {UB_SURE_INSURANCE_COMPANIES}. "
    "The documents include גילוי נאות (disclosure documents), תנאי ביטוח (insurance conditions), and חוק וסדר (legal documents and regulations). "
    f"They cover insurance types such as {INSURANCE_TYPE_AVAILABLE_HEB} and are further organized into categories like {INSURANCE_CATEGORY_HEB}, "
    "which map to sections such as basic health insurance not covered by Kupat Holim, surgeries in Israel, ambulatory appendices, "
    "additional coverages, service documents, and pricing information. In addition, the documents detail sub-categories such as "
    f"{INSURANCE_SUB_CATEGORY_HEB}, corresponding to specific aspects like medicines outside the basket, transplants and treatments abroad, "
    "surgeries abroad, various consultation and diagnostic services, home doctor visits, complementary and online services, among others. "
    "Each document entry provides links to PDFs containing further details for each section."
)

llm = ChatOpenAI(
    model="gpt-4o-mini"
    # model = "o3-mini"
)

# llm = ChatVertexAI(
#     # model=GeminiModels.GEMINI_2_0_FLASH_LITE_STABLE,
#     # model=GeminiModels.GEMINI_2_0_PRO_EXP_02_05,
#     # model=GeminiModels.GEMINI_2_0_FLASH_THINKING_EXP,
#     # model=GeminiModels.GEMINI_2_0_FLASH_STABLE,
#
# )
examples = [
    (
        "I want a hotel in the Balkans with a king sized bed and a hot tub. Budget is $300 a night",
        {
            "query": "king-sized bed, hot tub",
            "filter": 'and(in("country", ["Bulgaria", "Greece", "Croatia", "Serbia"]), lte("onsiterate", 300))',
        },
    ),
    (
        "I want a hotel in the Balkans with a king sized bed and a hot tub. Budget is $300 a night",
        {
            "query": "king-sized bed, hot tub",
            "filter": 'and(in("country", ["Bulgaria", "Greece", "Croatia", "Serbia"]), lte("onsiterate", 300))',
        },
    ),
]

retriever = SelfQueryRetriever.from_llm(
    llm,
    vectorstore,
    document_content_description,
    metadata_field_info,
    examples = examples,
    verbose=True,
    search_kwargs= {"k": 4},

)

retrieval_description = f"""
Returns answers for any user question.
Searches and returns insurance-related documents in Hebrew from various companies such as {UB_SURE_INSURANCE_COMPANIES}.

**Document Types:**
- גילוי נאות (Disclosure Documents)
- תנאי ביטוח (Insurance Conditions)
- חוק וסדר (Legal Documents and Regulations)

**Insurance Types Covered:**
Documents cover insurance types listed in {INSURANCE_TYPE_AVAILABLE_HEB}.

**Categories:**
1. **Basic Health Insurance Not Covered by Kupat Holim** (ביטוחי בריאות בסיס (לא מכוסה בקופ"ח))
   - תרופות מחוץ לסל (Medications Outside the Basket)
   - השתלות וטיפולים בחול (Transplants and Treatments Abroad)
   - ניתוחים בחול (Surgeries Abroad)
   
2. **Surgeries in Israel** (ניתוחים בישראל)
   - שב"ן ללא השתתפות (SHABAN Without Copayment)
   - שב"ן עם השתתפות (SHABAN With Copayment)
   - שקל ראשון (First Shekel Coverage)
   
3. **Ambulatory Appendices** (נספח אמבולטורי)
   - ייעוץ ובדיקות (Consultations and Examinations)
   - ייעוץ מורחב (Extended Consultation)
   
4. **Additional Coverages** (כיסויים נוספים)
   - אבחון מהיר (Rapid Diagnosis)
   - ליווי יעוץ רפואי (Medical Guidance/Consultation)
   - התפתחות הילד (Child Development)
   - טכנולוגי ואביזרים (Technological Equipment and Accessories)
   
5. **Service Documents** (כתבי שירות)
   - רופא עד הבית (Doctor Home Visits)
   - רפואה משלימה (Complementary Medicine)
   - אישי אונליין (Personal Online Services)
   
6. **Pricing and Information** (מידע ומחירים)
   - וכיסויים נוספים (Additional Coverages)
   
7. **Severe Illnesses** (מחלות קשות)
   - קשות מלא (Full Coverage for Severe Illnesses)
   - קשות סרטן (Cancer-Specific Coverage)
   
8. **Personal Accidents** (תאונות אישיות)
   - תאונות (Accidents)
   - נכות (Disability)
   
9. **Other** (אחר)
   - מחירונים ומידע נוסף (Pricing Lists and Additional Information)

10. **Insurance Contract Law** (חוק חוזה הביטוח)

11. **2016 Circular** (חוזר 2016)

12. **Directive 22** (הוראות 22)

13. **Supervision Regulations** (תקנות הפיקוח)

14. **Pre-Existing Medical Conditions** (מצב רפואי קודם)
"""

retriever_tool = create_retriever_tool(
    retriever,
    "UB-Sure-Life-And-Health-Insurance-info-retriever",
    # "Searches and returns excerpts from documents about insurance from various insurance companies.",
    retrieval_description,
    response_format = "content_and_artifact"
)

system_message =SYSTEM_MESSAGE_SIMPLE

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_message),
        ("placeholder", "{messages}"),
    ]
)

memory = MemorySaver()

# memory = ConversationSummaryMemory(llm=llm, max_token_limit=1500)

ub_sure_agent_executor_o3 = create_react_agent(
    llm, [retriever_tool],
    # prompt=prompt,
    prompt=system_message,
    checkpointer=memory
)


trimmer = trim_messages(
    max_tokens=8000,
    include_system=True,
    strategy='last',
    start_on=['human', 'ai'],
    allow_partial=False,
    # token_counter=llm_for_tokenizer
    token_counter=llm
)


def trim_and_invoke(thread_id, new_message):
    prev_state = ub_sure_agent_executor_o3.get_state({"configurable": {"thread_id": thread_id}})
    prev_messages = prev_state.values.get('messages', [])
    # print("MEssages before trim", len(prev_messages))
    new_messages = trimmer.invoke(prev_messages)
    # print("MEssages AFTER trim", len(new_messages))


    message_ids_to_remove = set(map(lambda m: m.id, prev_messages)) - set(map(lambda m: m.id, new_messages))

    ub_sure_agent_executor_o3.update_state({"configurable": {"thread_id": thread_id}}, {
        "messages": [RemoveMessage(id=mid) for mid in message_ids_to_remove]
    })
    state = ub_sure_agent_executor_o3.get_state({"configurable": {"thread_id": thread_id}})

    print("NEw messages in state", len(state.values.get('messages', [])))

    for event in ub_sure_agent_executor_o3.stream(
            {"messages": [HumanMessage(content=new_message)]},
            config={"configurable": {"thread_id": thread_id}},
            stream_mode="values"
    ):
        yield event

    # state = ub_sure_agent_executor_o3.get_state({"configurable": {"thread_id": thread_id}})
    # print("done")
    # return res
# ub_sure_agent_executor_o3.update_state(config, {})

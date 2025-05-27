import os

from dotenv import load_dotenv
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

# from langchain_google_vertexai import ChatVertexAI
# from langchain_google_vertexai import VertexAIEmbeddings

from GeminiModels import GeminiModels
from ub_retriever_const import metadata_field_info
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
# COLLECTION_NAME = "ub-sure-collection-heb-4"
# INDEX_NAME = "ub-sure-collection-heb-4"
COLLECTION_NAME = "ub-sure-collection-heb-5" # for 3072 dims embeddings
INDEX_NAME = "ub-sure-collection-heb-5" # for 3072 dims embeddings

MongoClient = MongoClient(CONNECTION_STRING)
collection = MongoClient[DB_NAME][COLLECTION_NAME]

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

# embedding_model_gemini = "gemini-embedding-exp-03-07" # for 3072 dims embeddings
# embeddings = GoogleGenerativeAIEmbeddings(
#     model=f"models/{embedding_model_gemini}",
#     # task_type="RETRIEVAL_DOCUMENT" # Or RETRIEVAL_QUERY, SEMANTIC_SIMILARITY, CLASSIFICATION, CLUSTERING
#     # Optional: title="Your document title" # Can sometimes improve retrieval quality
# )


vectorstore = MongoDBAtlasVectorSearch(
    collection=collection,
    embedding=embeddings,
    index_name=INDEX_NAME
)

# metadata_field_info = [
#     AttributeInfo(
#         name="companyName",
#         description=f"The insurance company name. One of {UB_SURE_INSURANCE_COMPANIES}.",
#         type="string",
#     ),
#     AttributeInfo(
#         name="docType",
#         description="The type of document. It can be גילוי נאות (disclosure), תנאי ביטוח (insurance conditions), or חוק וסדר (legal and regulatory).",
#         type="string",
#     ),
#     AttributeInfo(
#         name="insuranceType",
#         description=f"The type of insurance. One of {INSURANCE_TYPE_AVAILABLE_HEB}.",
#         type="string",
#     ),
#     AttributeInfo(
#         name="coverageType",
#         description=f"The type of insurance coverage. One of {INSURANCE_COVERAGE_TYPE_HEB}.",
#         type="string",
#     ),
#     AttributeInfo(
#         name="docCategory",
#         description=f"The insurance category. One of {INSURANCE_CATEGORY_HEB}.",
#         type="string",
#     ),
#     AttributeInfo(
#         name="docSubCategory",
#         description=f"The insurance sub-category. One of {INSURANCE_SUB_CATEGORY_HEB}.",
#         type="string",
#     )
# ]

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


retriever = SelfQueryRetriever.from_llm(
    llm,
    vectorstore,
    document_content_description,
    metadata_field_info,
    verbose=False,
    search_kwargs= {"k": 4},

)

retrieval_description = f"""
Returns answers for any user question.
Searches and returns insurance-related documents in Hebrew from various companies such as {UB_SURE_INSURANCE_COMPANIES}.

**Document Sources:**
Documents originate from various insurance companies, including those listed in {UB_SURE_INSURANCE_COMPANIES}.

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

ub_sure_agent_executor_5 = create_react_agent(
        llm, [retriever_tool], prompt=prompt, checkpointer=memory
)


import json

from langchain.chains.query_constructor.base import AttributeInfo

from ub_sure_2.ub_sure_const import UB_CATEGORIES, ALL_DEPARTMENTS, UB_SURE_DOC_TYPES, DOC_CATEGORIES, \
    DOC_SUB_CATEGORIES, \
    UB_SURE_COMPANIES, DOC_SUB_CATEGORY_BRIUT, UB_DOC_TYPE, UB_INSURANCE_DEPARTMENT, UB_INSURANCE_TOPICS, \
    UB_REGULATIONS_TOPICS

# retriever_document_content_description = (
#     "This collection contains Hebrew documents pertaining to the Israeli insurance and financial regulation sectors. "
#     f"Documents originate from various companies and institutions, including insurance providers and investment houses (e.g., {', '.join(UB_SURE_COMPANIES[:3])}..., full list available in 'companyName' metadata). "
#     f"The content is broadly classified by 'category' ({', '.join(UB_CATEGORIES)}) and covers primary areas specified in 'type' (e.g., {', '.join(ALL_DEPARTMENTS[:4])}...). "
#     f"Specific document classifications like {', '.join(UB_SURE_DOC_TYPES)} are available via the 'docType' field. "
#     "The core content relates to insurance policies (health, life, long-term savings), investment products (pension funds, provident funds), legal texts, regulatory guidelines, circulars, and industry benchmarks. "
#     "Detailed topic descriptions are found in 'docCategory' (covering specifics like 'ניתוחים בישראל', 'קרן פנסיה', 'חוק חוזה הביטוח', 'תקנות הפיקוח', 'מדד שירות') "
#     "and further refined by 'docSubCategory' (e.g., 'תרופות מחוץ לסל', 'מקיפה', 'שכיר'). "
#     "Use the associated metadata fields to filter for relevant documents based on their content, origin, and classification."
# )

# retriever_document_content_description = (
#     "This collection contains Hebrew documents pertaining to the Israeli insurance and financial regulation sectors. "
#     "The core content of these documents typically relates to insurance policies (including health, life, long-term savings), "
#     "investment products (such as pension funds, provident funds), legal texts, regulatory guidelines, "
#     "circulars, and industry benchmarks. "
#     "To effectively retrieve specific documents, leverage the following metadata fields: "
#     f"\n- 'companyName': Identifies the originating company or institution, such as an insurance provider or investment house (e.g., {', '.join(UB_SURE_COMPANIES[:3])}...). "
#     f"\n- 'category': Broadly classifies the document's primary content, for example, as 'ביטוח' (insurance-related), 'רגולציה' (regulatory matters), or 'פרטי התקשרות' (contact details) (e.g., {', '.join(UB_CATEGORIES)}). "
#     f"\n- 'type': Specifies the main area or department the document's subject matter belongs to, such as 'בריאות' (health), 'חיים' (life), 'השקעות' (investments), or 'שירות/כללי' (general service) (e.g., {', '.join(ALL_DEPARTMENTS[:4])}...). "
#     f"\n- 'docType': Indicates the formal nature or classification of the document itself, such as 'תנאי ביטוח' (insurance policy conditions), 'חוק' (law), 'חוזר' (circular), or 'מדד' (benchmark) (e.g., {', '.join(UB_SURE_DOC_TYPES)}). "
#     "\n- 'docCategory': Provides more detailed topic descriptions found within the document, covering specifics like 'ניתוחים בישראל' (surgeries in Israel), 'קרן פנסיה' (pension fund), or 'מדד שירות' (service quality index). "
#     "\n- 'docSubCategory': Offers the most granular refinement of the document's topic, for instance, 'תרופות מחוץ לסל' (out-of-basket drugs), 'מקיפה' (comprehensive, usually for pension), or 'שכיר' (salaried employee context). "
#     "\nUse these metadata fields individually or in combination to precisely filter for documents based on their specific content, origin, and classification."
# )


retriever_document_content_description = (
    "This collection contains Hebrew documents pertaining to the Israeli insurance and financial regulation sectors. "
    "The core content of these documents typically relates to insurance policies (including health, life, long-term savings), "
    "investment products (such as pension funds, provident funds), legal texts, regulatory guidelines, "
    "circulars, and industry benchmarks. "
    # "To effectively retrieve specific documents, leverage the following metadata fields: "
    # f"\n- 'companyName': Identifies the originating company or institution, such as an insurance provider or investment house (e.g., {', '.join(UB_SURE_COMPANIES[:3])}...). "
    # f"\n- 'docSubCategory': Identifies the topic of the insurance, such as an insurance provider or investment house (e.g., {', '.join(DOC_SUB_CATEGORY_BRIUT)}...). "
    # "\nUse these metadata fields individually or in combination to precisely filter for documents based on their specific content, origin, and classification."
)

# retrieval_description = f"""Use this tool to search and retrieve relevant Hebrew documents about Israeli insurance products, financial instruments (like pensions, provident funds), and related laws and regulations.
# The documents originate from various Israeli companies and financial institutions (e.g., {', '.join(UB_SURE_COMPANIES[:3])}...).
# This tool is ideal for finding specific information such as:
# - Policy terms and conditions ('תנאי ביטוח')
# - Disclosure documents ('גילוי נאות')
# - Regulations and statutes ('תקנון')
# - Laws ('חוק') and circulars ('חוזר')
# - Industry benchmarks ('מדד')
# - Details about specific insurance or financial types (e.g., '{ALL_DEPARTMENTS[0]}', '{ALL_DEPARTMENTS[1]}', '{ALL_DEPARTMENTS[2]}', 'קרן פנסיה')
# - Documents related to a specific company ('companyName').
#
# Use this tool when the user asks about insurance policies, savings plans, pension funds, investment rules, financial regulations, legal requirements, or specific documents from known Israeli providers in the insurance and finance sectors."""

retrieval_description = (
    "Searches and retrieves specific information from a collection of Hebrew documents "
    "about the Israeli insurance and financial regulation sectors. Use this tool when "
    "the user asks for details about insurance policies (e.g., health, life, savings), "
    "investment products (pension funds, provident funds), associated **pricing**, "
    "regulatory guidelines, laws, company disclosures, circulars, or industry benchmarks. "
    "It can effectively find information related to specific companies, document types, "
    "pricing details, or insurance/financial categories."
)
filter_examples_22 = [
    # Example 1: Specific policy type and company (Revised: eq -> in for type, docType)
    (
        "מה התנאים של ביטוח בריאות בהראל?", # "What are the conditions for health insurance at Harel?"
        {
            "query": "תנאים של ביטוח בריאות הראל", # "Harel health insurance conditions"
            # "filter": 'and(eq("companyName", "הראל"), in("category", ["ביטוח"]) , in("type", ["בריאות"]), in("docType", ["תנאי ביטוח"]))'
            "filter": 'and(eq("companyName", "הראל"), in("category", ["ביטוח"]) , in("type", ["בריאות"]), in("docType", ["תנאי ביטוח"]))'
        }
    ),

    # Example 2: Specific service ("רופא עד הבית") from a specific company
    (
        "מה צריך כדי להזמין רופא עד הבית במגדל", # "What is needed to order a doctor to the home at Migdal?"
        {
            # "query": "רופא עד הבית", # "Ordering a doctor to the home Migdal"
            # "filter": 'and(eq("companyName", "מגדל"), in("category", ["ביטוח"]), in("type", ["בריאות"]), in("docCategory", ["כתבי שירות"]), in("docSubCategory", ["רופא עד הבית"]))'
            # "filter": 'and(eq("companyName", "מגדל"), in("docSubCategory", ["רופא עד הבית"]))'

            "query": "הזמנת רופא עד הבית מגדל",  # "Ordering a doctor to the home Migdal"
            "filter": 'and(eq("companyName", "מגדל"), in("category", ["ביטוח"]), in("type", ["בריאות"]), in("docCategory", ["כתבי שירות"]), in("docSubCategory", ["רופא עד הבית"]))'

        }
    ),

    # Example 3: Information about a specific unit ("התפתחות הילד") at a specific company
    (
        "מי המטפל ביחידת התפתחות הילד של מנורה?", # "Who is the caregiver in Menora's child development unit?"
        {
            "query": "יחידת התפתחות הילד", # "Menora child development unit caregiver/therapist"
            # "filter": 'and(eq("companyName", "מנורה"), in("category", ["ביטוח"]), in("type", ["בריאות"]), in("docType", ["תנאי ביטוח"]), in("docSubCategory", ["התפתחות הילד"]))'
            "filter": 'and(eq("companyName", "מנורה"), in("docSubCategory", ["התפתחות הילד"]))'

        }
    ),

    # # Example 4: Phone number for Phoenix for someone abroad
    # (
    #     "מה מספר הטלפון של הפניקס למי שנמצא בחו\"ל?",
    #     # "What is the phone number of Phoenix for someone who is abroad?"
    #     {
    #         # Query focuses on "Phoenix phone number abroad"
    #         "query": "מספר טלפון הפניקס",  # "Phoenix phone number abroad"
    #         "filter": 'and(eq("companyName", "הפניקס"), in("category", ["פרטי התקשרות"]))'
    #     }
    # ),

    # Example 5: Question about duration of medical accompaniment at Harel
    (
        "כמה זמן אני מקבל ליווי מהרופא ומה קורה אחרי שלושה חודשים?", # "How long do I receive accompaniment from the doctor and what happens after three months at Harel?"
        {
            "query": "ליווי מהרופא אחרי שלושה חודשים", # "Duration medical accompaniment Harel three months"
            # "filter": 'and(in("category", ["ביטוח"]), in("type", ["בריאות"]), in("docType", ["תנאי ביטוח"]), in("docSubCategory", ["ליווי או יעוץ רפואי"]))'
            "filter": 'and( in("docSubCategory", ["ליווי או יעוץ רפואי"]))'
        }
    ),

    # Example 6: Maximum claimable amount for non-basket drugs at Phoenix
    (
        "מהו הסכום המרבי שניתן לתבוע עבור תרופות שאינן כלולות בסל שירותי הבריאות של הפניקס?",
        # "What is the maximum amount that can be claimed for drugs not included in the health basket of Phoenix?"
        {
            # Query focuses on "Phoenix drugs outside basket claim amount"
            "query": "תרופות שאינן כלולות בסל שירותי הבריאות",  # "Phoenix drugs outside basket maximum claim amount"
            # Filter based on the provided object's metadata
            "filter": 'and(eq("companyName", "הפניקס"),  in("docSubCategory", ["תרופות מחוץ לסל"]))'
        }
    ),

    # # Example 6: Maximum claimable amount for non-basket drugs at Phoenix
    # (
    #     "מהו הסכום המרבי שניתן לתבוע עבור תרופות שאינן כלולות בסל שירותי הבריאות של הפניקס?",
    #     # "What is the maximum amount that can be claimed for drugs not included in the health basket of Phoenix?"
    #     {
    #         # Query focuses on "Phoenix drugs outside basket claim amount"
    #         "query": "תרופות שאינן כלולות בסל שירותי הבריאות",  # "Phoenix drugs outside basket maximum claim amount"
    #         # Filter based on the provided object's metadata
    #         "filter": 'and(eq("companyName", "הפניקס"), in("category", ["ביטוח"]), in("type", ["בריאות"]), in("docType", ["גילוי נאות"]),  in("docSubCategory", ["תרופות מחוץ לסל"]))'
    #     }
    # ),

    # # Example 7: Need for doctor's referral for complementary medicine at Menora
    # (
    #     "האם אני חייב לקבל הפניה מרופא כדי להשתמש בשירותי הרפואה המשלימה המכוסים במנורה?",
    #     # "Do I have to get a doctor's referral to use the covered complementary medicine services at Menora?"
    #     {
    #         # Query focuses on "Menora complementary medicine doctor referral"
    #         "query": "הפניה מרופא שירותי הרפואה המשלימה",  # "Menora complementary medicine doctor referral"
    #         # Filter based on the provided object's metadata
    #         "filter": 'and(eq("companyName", "מנורה"), in("category", ["ביטוח"]), in("type", ["בריאות"]), in("docType", ["תנאי ביטוח"]), in("docSubCategory", ["רפואה משלימה"]))'
    #     }
    # ),
    #
    # # Example 8: Tax-free withdrawal period for Harel study fund
    # (
    #     "אחרי כמה שנים אוכל למשוך את הכסף מהקרן השתלמות בהראל בלי לשלם מס?",
    #     # "After how many years can I withdraw money from the Harel study fund without paying tax?"
    #     {
    #         # Query focuses on "Harel study fund tax-free withdrawal years"
    #         "query": "משיכת כסף מהקרן השתלמות",  # "Harel study fund tax-free withdrawal years"
    #         # Filter based on the provided object's metadata
    #         "filter": 'and(eq("companyName", "הראל"), in("category", ["ביטוח"]), in("type", ["חא\\"ט"]), in("docType", ["תקנון"]), in("docCategory", ["קרן השתלמות"]), in("docSubCategory", ["תקנון -קרן השתלמות"]))'
    #     }
    # ),


    # # Example 9: Change in insurance premium with age and frequency (regulatory)
    # (
    #     "האם דמי הביטוח שלי ישתנו עם הגיל, ואם כן, באיזו תדירות?",
    #     {
    #         # Query focuses on "insurance premium change age frequency"
    #         "query": "דמי הביטוח",  # "Insurance premium change age frequency"
    #         "filter": 'and(in("category", ["רגולציה"]), in("type", ["בריאות", "חיים"]), in("docType", ["תקנון"]), in("docCategory", ["ניתוחים 2016"]))'
    #     }
    # ),
    #
    # # Example 10: Updating beneficiaries in a provident fund (regulatory)
    # (
    #     "כיצד אוכל לעדכן את רשימת המוטבים שלי במקרה של פטירה בקופת גמל?",
    #     # "How can I update my list of beneficiaries in case of death in a provident fund?"
    #     {
    #         # Query focuses on "update beneficiaries provident fund death"
    #         "query": "עדכון רשימת המוטבים במקרה של פטירה בקופת גמל",  # "Update beneficiaries provident fund death"
    #         "filter": 'and(in("category", ["רגולציה"]), in("type", ["חא\\"ט"]), in("docType", ["חוק"]), in("docCategory", ["גמל 2005"]))'
    #     }
    # ),

    # # Example 11: General query potentially not triggering specific metadata filters (No changes needed)
    # (
    #     "ספר לי על ביטוח בישראל", # "Tell me about insurance in Israel"
    #     {
    #         "query": "ביטוח בישראל", # "Insurance in Israel"
    #         # No specific filter identified.
    #         "filter": '{}' # Or None, depending on observed retriever behavior
    #     }
    # ),
]

filter_examples = [
    (
        "מה התנאים של ביטוח בריאות בהראל?",
        {
            "query": "תנאים ביטוח בריאות",
            "filter": 'and(eq("companyName", "הראל"), in("category", ["ביטוח"]), in("type", ["בריאות"]), in("docType", ["תנאי ביטוח"]))'
        }
    ),
    (
        "מה צריך כדי להזמין רופא עד הבית במגדל?",
        {
            "query": "הזמנת רופא עד הבית",
            "filter": 'and(eq("companyName", "מגדל"), in("docSubCategory", ["רופא עד הבית"]))'
        }
    ),
    (
        "מה הסכום שהמנוי צריך לשלם כהשתתפות עצמית עבור ביקור רופא בבית במסגרת כתב השירות של הראל?",
        {
            # semantic core: what is the out‑of‑pocket amount for a home‑visit doctor?
            "query": "סכום השתתפות עצמית ביקור רופא בבית",
            # metadata: company Harel + service‑document subcategory “רופא עד הבית”
            "filter": 'and(eq("companyName", "הראל"), in("docSubCategory", ["רופא עד הבית"]), in("docCategory", ["כתבי שירות"]))'
        }
    ),
    (
        "מי המטפל ביחידת התפתחות הילד של מנורה?",
        {
            "query": "מטפל ביחידת התפתחות הילד",
            "filter": 'and(eq("companyName", "מנורה"), in("docSubCategory", ["התפתחות הילד"]))'
        }
    ),
    (
        "כמה זמן אני מקבל ליווי מהרופא ומה קורה אחרי שלושה חודשים?",
        {
            "query": "ליווי מהרופא אחרי שלושה חודשים",
            "filter": 'in("docSubCategory", ["ליווי או יעוץ רפואי"])'
        }
    ),
    (
        "מהו הסכום המרבי שניתן לתבוע עבור תרופות שאינן כלולות בסל שירותי הבריאות של הפניקס?",
        {
            "query": "תרופות מחוץ לסל שירותי הבריאות",
            "filter": 'and(eq("companyName", "הפניקס"), in("docSubCategory", ["תרופות מחוץ לסל"]))'
        }
    ),
    # New pattern example #1: Phoenix
    (
        "איך מוגדרת החברה במסמך כתב השירות של הפניקס?",
        {
            "query": "כיצד מוגדרת החברה",
            "filter": 'and(eq("companyName", "הפניקס"), in("docCategory", ["כתבי שירות"]))'
        }
    ),

    # # New pattern example #2: מגדל
    # (
    #     "באיזה אופן מוגדרת החברה במסמך כתב השירות של מגדל?",
    #     {
    #         "query": "כיצד מוגדרת החברה",
    #         "filter": 'and(eq("companyName", "מגדל"), in("docCategory", ["כתבי שירות"]))'
    #     }
    # ),

    # Fallback “no‑filter” example:
    (
        "ספר לי על ביטוח בישראל",
        {
            "query": "ביטוח בישראל",
            "filter": "{}"
        }
    ),
    # Control question (not used for training):
    # (
    #     "כיצד מוגדרת החברה במסמך כתב השירות של הראל?",
    #     {
    #         "query": "כיצד מוגדרת החברה",
    #         "filter": 'and(eq("companyName", "הראל"), in("docSubCategory", ["כתבי שירות"]))'
    #     }
    # ),
]

# Helper to truncate long lists for descriptions
def format_list_for_description(items: list, max_items=100) -> str:
    if not items:
        return "an empty list"
    if len(items) > max_items:
        display_items = items[:max_items] + ["..."]
    else:
        display_items = items
    # Use json.dumps for proper quoting and escaping, remove brackets
    return json.dumps(display_items, ensure_ascii=False)[1:-1]

# metadata_field_info = [
#     # AttributeInfo(
#     #     name="category",
#     #     description=f"Broad document category. List values from: {format_list_for_description(UB_CATEGORIES)}.",
#     #     type="string", # Type of elements in the list
#     # ),
#     # AttributeInfo(
#     #     name="type",
#     #     description=f"Primary type (e.g., insurance area). List values from: {format_list_for_description(ALL_DEPARTMENTS)}.",
#     #     type="string", # Type of elements in the list
#     # ),
#     #  AttributeInfo(
#     #     name="docType",
#     #     # Updated to use the defined UB_SURE_DOC_TYPES list
#     #     description=f"Specific document classification. List values from: {format_list_for_description(UB_SURE_DOC_TYPES)}.",
#     #     type="string", # Type of elements in the list
#     # ),
#     # AttributeInfo(
#     #     name="docCategory",
#     #     description=f"Detailed content category (insurance/legal). List values from: {format_list_for_description(DOC_CATEGORIES)}.",
#     #     type="string", # Type of elements in the list
#     # ),
#     AttributeInfo(
#         name="docSubCategory",
#         description=f"Specific content sub-category. List values from: {format_list_for_description(DOC_SUB_CATEGORIES)}.",
#         type="string", # Type of elements in the list
#     ),
#     AttributeInfo(
#         name="companyName",
#         # Corrected list reference to CLIENT_NAMES and clarified 'single value'
#         description=f"Related company name (insurance/financial). Expected single value from: {format_list_for_description(UB_SURE_COMPANIES)}.",
#         type="string", # This field is a single string
#     ),
#     # AttributeInfo(
#     #     name="source",
#     #     # Slightly shortened description
#     #     description="Optional: Document source identifier (e.g., URL, path).",
#     #     type="string",
#     # ),
#     # AttributeInfo(
#     #     name="updateTs",
#     #     # Shortened description with specific format example
#     #     description="Optional: Last update timestamp (ISO 8601 format, e.g., 2025-04-24T10:03:19.996Z).",
#     #     type="string",
#     # ),
# ]
#
#
# metadata_field_info = [
#     AttributeInfo(
#         name="category",
#         description=(
#             "A list providing the broad document category. "
#             f"Possible values include: {format_list_for_description(UB_CATEGORIES)}. "
#             "IMPORTANT: This field is a list. To check if this list *contains* a specific category (e.g., 'רגולציה'), "
#             "use the 'in' operator, like `in('category', ['רגולציה'])`. "
#             "For multiple values, use `in('category', ['רגולציה', 'ביטוח'])`."
#         ),
#         type="string", # Type of elements in the list
#     ),
#     AttributeInfo(
#         name="type",
#         description=(
#             "A list identifying the primary insurance or financial area(s) the document relates to. "
#             "Use this to filter documents by their main subject, such as health insurance or investments. "
#             f"Possible values in the list include elements from: {format_list_for_description(ALL_DEPARTMENTS)}. "
#             "For example, a document relevant to both life and long-term savings might have ['חיים', 'חא\"ט'] in this field."
#         ),
#         type="string", # Type of elements in the list
#     ),
#      AttributeInfo(
#         name="docType",
#         # Updated to use the defined UB_SURE_DOC_TYPES list
#          description=(
#              "A list specifying the formal classification(s) of the document. "
#              f"Possible values include: {format_list_for_description(UB_SURE_DOC_TYPES)}. "
#              "IMPORTANT: This field is a list. To filter if this list *contains* a specific value (e.g., 'חוק'), "
#              "use the 'in' operator, like `in('docType', ['חוק'])`. "
#              "For multiple values, use `in('docType', ['חוק', 'תקנון'])`."
#          ),
#         type="string", # Type of elements in the list
#     ),
#     AttributeInfo(
#         name="docCategory",
#         description=(
#             "A list providing detailed topic descriptions (insurance aspects, financial products, legal subjects). "
#             f"Possible values include: {format_list_for_description(DOC_CATEGORIES)}. "
#             "IMPORTANT: This field is a list. To check if this list *contains* a specific category (e.g., 'קרן פנסיה'), "
#             "use the 'in' operator, like `in('docCategory', ['קרן פנסיה'])`. "
#             "For checking multiple categories (e.g., pension OR provident fund), use `in('docCategory', ['קרן פנסיה', 'קופת גמל'])`."
#         ),
#         type="string", # Type of elements in the list
#     ),
#     AttributeInfo(
#         name="docSubCategory",
#         description=(
#             "A list providing the most specific classification, refining 'docCategory'. "
#             f"Possible values include: {format_list_for_description(DOC_SUB_CATEGORIES)}. "
#             # "IMPORTANT: This field is a list. To check if this list *contains* a specific sub-category (e.g., 'מקיפה'), "
#             # "use the 'in' operator, like `in('docSubCategory', ['מקיפה'])`. "
#             # "For multiple values, use `in('docSubCategory', ['מקיפה', 'שכיר'])`."
#         ),
#         type="string", # Type of elements in the list
#     ),
#     AttributeInfo(
#         name="companyName",
#         # Corrected list reference to CLIENT_NAMES and clarified 'single value'
#         description=f"Related company name (insurance/financial). Expected single value from: {format_list_for_description(UB_SURE_COMPANIES)}.",
#         type="string", # This field is a single string
#     ),
#     AttributeInfo(
#         name="source",
#         # Slightly shortened description
#         description="Optional: Document source identifier (e.g., URL, path).",
#         type="string",
#     ),
#     AttributeInfo(
#         name="updateTs",
#         # Shortened description with specific format example
#         description="Optional: Last update timestamp (ISO 8601 format, e.g., 2025-04-24T10:03:19.996Z).",
#         type="string",
#     ),
# ]



metadata_field_info = [
    AttributeInfo(
        name="docSubCategory",
        description=(
            # "Health insurance or  topic. "
            "The specific sub-category or topic covered by the document, generally related to "
            "health insurance, life insurance, pension funds, provident funds (קופות גמל), or tax-advantaged savings plan like (קרנות השתלמות). "
            f"Optional: Expected single value from one of:  {format_list_for_description(DOC_SUB_CATEGORIES)}"
        ),
        type="string",
    ),
    # AttributeInfo(
    #     name="docCategory",
    #     description=(
    #         "A list providing detailed topic descriptions (insurance aspects, financial products, legal subjects). "
    #         f"Optional: Expected single value from one of:  {format_list_for_description(DOC_CATEGORIES)}"
    #     ),
    #     type="string",  # Type of elements in the list
    # ),
    AttributeInfo(
        name="companyName",
        description=f"Related company name (insurance/financial). Expected single value from: {format_list_for_description(UB_SURE_COMPANIES)}.",
        type="string", # This field is a single string
    ),
    # AttributeInfo(
    #     name="docType",
    #     description=(
    #         "The classification of the document. "
    #         "Used to filter by the document’s nature—be it a disclosure, insurance‑condition text, "
    #         "law, regulation/bylaw, circular/memo, or financial index/benchmark. "
    #         f"Optional: Expected single value from one of: {format_list_for_description(UB_SURE_DOC_TYPES)}. "
    #     ),
    #     type="string",  # Type of elements in the list
    # ),
    # AttributeInfo(
    #     name="type",
    #     description=(
    #         "The insurance department."
    #         f"Optional: Expected single value from one of: {format_list_for_description(ALL_DEPARTMENTS)}. "
    #     ),
    #     type="string",  # Type of elements in the list
    # ),
    #
    # AttributeInfo(
    #     name="category",
    #     description=(
    #         "The category of the document. "
    #         f"Optional: Expected single value from one of: {format_list_for_description(UB_CATEGORIES)}. "
    #     ),
    #     type="string",  # Type of elements in the list
    # ),



    # AttributeInfo(
    #     name="source",
    #     # Slightly shortened description
    #     description="Optional: Document source identifier (e.g., URL, path).",
    #     type="string",
    # ),
    # AttributeInfo(
    #     name="updateTs",
    #     # Shortened description with specific format example
    #     description="Optional: Last update timestamp (ISO 8601 format, e.g., 2025-04-24T10:03:19.996Z).",
    #     type="string",
    # ),
]




metadata_field_info_simplified = [
    AttributeInfo(
        name="companyName",
        description= (
            f"Optional: Related company name (insurance/financial)."
            f"Important: If user inserts company name פניקס than user intended to say הפניקס."
            f"Important: You are allowed to select one and only one from the list of valid companies names provided here: {UB_SURE_COMPANIES}"
            # f"This filter is optional but if there is a company name that is in the provided list choose it from the list"
            # f"or don't provide companyName at all."
            # f"Expected single value from: {format_list_for_description(UB_SURE_COMPANIES)}."
            # f"Important: The only valid options are: {format_list_for_description(UB_SURE_COMPANIES)}."

        ),
        type="string",  # This field is a single string
    ),

    # AttributeInfo(
    #     name="category",
    #     description=(
    #         f"Related subject of the content. Valid options for category of main subject of the query are: {UB_CATEGORIES}."
    #         # "Default selection is: “ביטוח”. "
    #         "Conditions for selection are: "
    #         "- If the query's main subject is about contact details (phone numbers, email addresses, locations, working hours), choose 'פרטי התקשרות'."
    #         "- If the quer's main subject is about insurance regulations, circulars, חוק, תקנון, חוזר, or מדד, choose 'רגולציה'. "
    #         "- If the quer's main subject is about specific insurance matters (coverage, payments, policy conditions, or comparisons between companies/policies), choose 'ביטוח'. "
    #     ),
    #     type="string",
    # ),
    #
    # AttributeInfo(
    #     name="insuranceDepartment",
    #     description=(
    #         f"Related insurance department discussed in the main subject of the content is 'ביטוח'. Valid options for insurance department are: {format_list_for_description(UB_INSURANCE_DEPARTMENT)}. "
    #
    #         # f"Optional: Expected single value from: {UB_INSURANCE_DEPARTMENT}."
    #         # f"Important: If and Only if 'category' is equal 'ביטוח' than valid options to select from are :  {UB_INSURANCE_DEPARTMENT}"
    #         # f"Important: If 'category' is 'רגולציה' or 'פרטי התקשרות' do not select anything."
    #
    #     ),
    #     type="List[string]",
    # ),

]

retriever_document_content_description_simplified = (
    "This collection contains Hebrew documents pertaining to the Israeli insurance and financial regulation sectors. "
    "The core content of these documents typically relates to insurance policies (including health, life, long-term savings), "
    "investment products (such as pension funds, provident funds), legal texts, regulatory guidelines, "
    "circulars, and industry benchmarks. "
    # "The goal is to refine filter as much as it is possible, hence choosing the maximum possible filtering options."
    # "If there is company name and subject of the content relates to 'ביטוח' create filter taking ino account both of them."
    #
    f"Here is the instruction how to make filtering step by step:"
    f"1. Select the 'companyName' from the valid list of company names if it is mentioned in the query. If name is not in the list of valid names do not select anything."
    # f"2. Analyze the query and Select the 'category' according to the subject of the query. "
    # f"   2.1 If the query is about contact details (phone numbers, email addresses, locations, working hours), choose 'פרטי התקשרות'."
    # f"   2.2 If the query involves insurance regulations, circulars, חוק, תקנון, חוזר, or מדד, choose 'רגולציה'."
    # f"   2.3 If the query concerns insurance matters (coverage, payments, policy conditions, or comparisons between companies/policies), choose 'ביטוח'. "
    # f"3. Only if 'category' equals 'ביטוח' than analyze the query and try to find the type of insurance and select it from the provided list of valid options :  {UB_INSURANCE_DEPARTMENT}"

)

filter_examples_simplified = [
    # Health insurance conditions for Harel
    (
        "מה התנאים של ביטוח בריאות בהראל?",
        {
            "query": "תנאים ביטוח בריאות",
            "filter": 'and(eq("companyName", "הראל"), eq("category", "ביטוח"), in("insuranceDepartment", ["בריאות"]))'
        }
    ),

    # Doctor-at-home service request at Migdal (no specific department)
    (
        "מה צריך כדי להזמין רופא עד הבית במגדל?",
        {
            "query": "הזמנת רופא עד הבית",
            "filter": 'and(eq("companyName", "מגדל"), eq("category", "ביטוח"))'
        }
    ),

    # # Self-payment amount for a home visit under Harel (no specific department)
    # (
    #     "מה הסכום שהמנוי צריך לשלם כהשתתפות עצמית עבור ביקור רופא בבית במסגרת כתב השירות של הראל?",
    #     {
    #         "query": "סכום השתתפות עצמית ביקור רופא בבית",
    #         "filter": 'and(eq("companyName", "הראל"), eq("category", "ביטוח"))'
    #     }
    # ),

    # # Inquiry about Menora's child development unit (no department from list)
    # (
    #     "מי המטפל ביחידת התפתחות הילד של מנורה?",
    #     {
    #         "query": "מטפל ביחידת התפתחות הילד",
    #         "filter": 'and(eq("companyName", "מנורה"), eq("category", "ביטוח"))'
    #     }
    # ),
    #
    # # Duration of ongoing medical support (no company, only category)
    # (
    #     "אחרי כמה זמן אני מקבל ליווי מהרופא ומה קורה אחרי שלושה חודשים?",
    #     {
    #         "query": "ליווי מהרופא אחרי שלושה חודשים",
    #         "filter": 'and(eq("category", "ביטוח"))'
    #     }
    # ),

    # # Maximum claim amount for non-included drugs at Phoenix -> mapped to health
    # (
    #     "מהו הסכום המרבי שניתן לתבוע עבור תרופות שאינן כלולות בסל שירותי הבריאות של הפניקס?",
    #     {
    #         "query": "תרופות מחוץ לסל שירותי הבריאות",
    #         "filter": 'and(eq("companyName", "הפניקס"), eq("category", "ביטוח"), in("insuranceDepartment", ["בריאות"]))'
    #     }
    # ),

    # Example using a life insurance department
    (
        "מה הכיסויים העיקריים בפוליסת חיים של כלל?",
        {
            "query": "כיסויים עיקריים פוליסת חיים",
            "filter": 'and(eq("companyName", "כלל"), eq("category", "ביטוח"), in("insuranceDepartment", ["חיים"]))'
        }
    ),

    # Regulation query
    (
        "מה התקנה האחרונה של רשות שוק ההון בנושא תמהיל השקעות?",
        {
            "query": "התקנה רשות שוק ההון תמהיל השקעות",
            "filter": 'and(eq("category", "רגולציה"))'
        }
    ),

    # Law-specific regulation query about life insurance age
    (
        "מה אומר חוק ביטוח חיים לגבי גיל המבוטח?",
        {
            "query": "חוק ביטוח חיים גיל המבוטח",
            "filter": 'and(eq("category", "רגולציה"))'
        }
    ),

    # Contact details query
    (
        "מה שעות הפתיחה של סניף הראל בתל אביב?",
        {
            "query": "שעות פתיחה סניף הראל תל אביב",
            "filter": 'and(eq("companyName", "הראל"), eq("category", "פרטי התקשרות"))'
        }
    ),

    # Fallback example
    (
        "ספר לי על ביטוח בישראל",
        {
            "query": "ביטוח בישראל",
            "filter": "{}"
        }
    ),
]
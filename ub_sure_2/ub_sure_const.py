
######################################################################################################
UB_SURE_DOC_TYPES = [
    'גילוי נאות',   # Disclosure
    'תנאי ביטוח',  # Insurance Conditions
    'חוק',         # Law
    'תקנון',       # Regulation / Statute / Bylaw
    'חוזר',        # Circular / Memo
    'מדד'          # Index / Benchmark / Measure
]

UB_SURE_INSURANCE_COMPANIES = [
    "הראל",
    "הפניקס",
    "מגדל",
    "מנורה",
    "כלל",
    "מיטב",  # Investment House
    "אלטושלר",  # Investment House
    "מור",  # Investment House
    "אינפיניטי",  # Investment House
    "אנליסט",  # Investment House
    "ילין לפידות",  # Investment House
    "הכשרה",
    "איילון"
  ]




# Constants based on TInsuranceDepartment
INSURANCE_DEPARTMENTS = [
    "בריאות",          # Health
    "חיים",           # Life
    "חא\"ט",          # Long-term savings
    "אלמנטר",         # Elementary / General P&C
    "נסיעות לחול",   # Travel Abroad
    "עסק",            # Business
    "השקעות",         # Investments
]

# Constants based on TContactDepartment
CONTACT_DEPARTMENTS = [
    "שירות/כללי",     # Service/General
    "שירות/כללי ראשי", # Main Service/General
]

# Combined list based on TDepartment
# ALL_DEPARTMENTS = INSURANCE_DEPARTMENTS + CONTACT_DEPARTMENTS
ALL_DEPARTMENTS = INSURANCE_DEPARTMENTS

# --- Law Types (Components of TLawType) ---



LAW_PRINCIPAL = [
    'חוק חוזה הביטוח',
    'חוק ההסדרים פרק טז רפורמה 23',
    'גמל 2005',
    'גיל פרישה'
]

LAW_SUPERVISION = [
    'תקנות הפיקוח',
    'צו הרחבה פנסיה חובה',
    'הוראות הפיקוח על–2009' # Note: Check if the '–' is intended or a typo for '-'
]

LAW_CIRCULARS = [
    'חוזר 2016',
    'חוזר ביטול',
    'חוזר מסמך הנמקה',
    'הוראות 22'
]

LAW_PRIVACY = [
    'הגנת הפרטיות',
    'רישוי סוכנים',
    'תנאים בחוזה',
    'צורת פוליסה'
]

LAW_COMPENSATION = [
    'פיצויים',
    'מסלקה פנסיונית',
    'פנסיה 2013',
    'מעל גמל אחת 2012',
    'דמי ניהול 2012',
    'חלוקה פנסיוני לזוג שנפרדו',
    'ניודים'
]

LAW_INVESTMENT = [
    'הסדרת יעוץ השקעות',
    'מסלולי השקעה'
]

LAW_DOCS = [
    'חתימה אלקטרונית',
    'הוצאות ישירות',
    'צירוף',
    'עריכת תוכנית',
    'חידוש',
    'שירות סוכן'
]

LAW_MEDICAL = [
    'מצב בריאותי קודם',
    'ניתוחים 2016'
]

LAW_AMENDMENTS = [
    'תיקון צירוף',
    'תיקון חידוש',
    'תיקון שירות',
    'תיקון השקעות'
]

LAW_POLICY_TERMS = [
    'הוראות לתוכנית פוליסה',
    '2022 תנאי פוליסה רפורמה אחרונה',
    'הסבר רפורמה'
]

LAW_GENERAL = [
    'פנסיה',
    'גמל'
]

LAW_SURVEYS = [
    'מדד שירות 2023 בריאות ופנסיה',
    'סקר הלשכה שירות לסוכן',
    'מדד פנדינג 2024'
]

# Combined list equivalent to TLawType
LAW_TYPES = (
    LAW_PRINCIPAL +
    LAW_SUPERVISION +
    LAW_CIRCULARS +
    LAW_PRIVACY +
    LAW_COMPENSATION +
    LAW_INVESTMENT +
    LAW_DOCS +
    LAW_MEDICAL +
    LAW_AMENDMENTS +
    LAW_POLICY_TERMS +
    LAW_GENERAL +
    LAW_SURVEYS
)


# --- Document Categories and Sub-Categories (Components) ---

DOC_CATEGORY_BRIUT = [
    'ביטוחי בריאות בסיס (לא מכוסה בקופ"ח)',
    'ניתוחים בישראל',
    'נספח אמבולטורי',
    'כיסויים נוספים',
    'כתבי שירות',
    'מידע ומחירים',
    'מחלות קשות',
    'תאונות אישיות'
]

DOC_SUB_CATEGORY_BRIUT = [
    'תרופות מחוץ לסל',
    'השתלות וטיפולים בחול',
    'ניתוחים בחול',
    'שב"ן ללא השתתפות',
    'שב"ן עם השתתפות',
    'שקל ראשון',

    'ייעוץ ובדיקות',
    'ייעוץ מורחב',

    # 'נספח אמבולטורי ייעוץ ובדיקות',
    # 'נספח אמבולטורי ייעוץ מורחב',

    'אבחון מהיר',
    'ליווי או יעוץ רפואי',
    'התפתחות הילד',
    'טכנולוגי ואביזרים',
    'רופא עד הבית',
    'רפואה משלימה',
    'אישי אונליין',
    'וכיסויים נוספים', # Check if leading 'ו' is intentional
    'קשות מלא',
    'קשות סרטן',
    'תאונות',
    'נכות',
    'מחירונים ומידע נוסף'
]

# DOC_SUB_CATEGORY_BRIUT = [
#     'תרופות מחוץ לסל',
#     'השתלות וטיפולים בחול',
#     'ליווי או יעוץ רפואי',
#     'התפתחות הילד',
#
# ]

DOC_CATEGORY_HAIM = [
    'חיים',
    'משכנתא',
    'מטריה ביטוחית (השלמה לפנסיה)',
    'אובדן כושר עבודה',
    'נכויות',
    'תנאי חיתום'
]

DOC_SUB_CATEGORY_HAIM = [
    'חיים (פיצוי חד פעמי)',
    'חודשי / פרמיה משתנה',
    'הכנסה למשפחה',
    'מוות מתאונה',
    'נכות מתאונה',
    'חיים למשכנתא',
    'דירה למשכנתא',
    'מטריה ביטוחית',
    'נספחים / הרחבות',
    'בסיס',
    'הרחבות',
    'נכויות',
    'נכות מוחלטת'
]

DOC_CATEGORY_HAT = [
    'קרן פנסיה',
    'ביטוח מנהלים',
    'קופת גמל לתגמולים ופיצויים',
    'קרן השתלמות',
    'קופת גמל להשקעה',
    'פוליסת חסכון'
]

DOC_SUB_CATEGORY_HAT = [
    'מקיפה',
    'משלימה',
    'תקציר',
    'שכיר',
    'שכיר קצבה לא משלמת',
    'עצמאי',
    'תגמולים ופיצויים',
    'קופה מרכזית לפיצויים',
    'תקנון -קרן השתלמות', # Note: Check spacing around '-'
    'תקנון - קופת גמל להשקעה', # Note: Check spacing around '-'
    'תנאים כללים',
    'נספח',
    'תנאים פוליסה "אנונה"'
]


# --- Combined Document Categories and Sub-Categories ---

# Equivalent of TDocCategory (TDocCategoryBriut | TDocCategoryHaim | TDocCategoryHAT | TLawType)
DOC_CATEGORIES = (
    DOC_CATEGORY_BRIUT +
    DOC_CATEGORY_HAIM +
    DOC_CATEGORY_HAT +
    LAW_TYPES # Includes all law-related categories
)

# Equivalent of TDocSubCategory (TDocSubCategoryBriut | TDocSubCategoryHaim | TDocSubCategoryHAT)
DOC_SUB_CATEGORIES = (
    DOC_SUB_CATEGORY_BRIUT +
    DOC_SUB_CATEGORY_HAIM +
    DOC_SUB_CATEGORY_HAT
)



######################################################################################################
# Matching following simplified Metadata
#
# export interface IDocumentMetadataVic {
#
#   category : TUBCategory
#   docType :    TDocType;
#
#   insuranceDepartment : TInsuranceDepartment [];
#   insuranceTopics : TInsuranceTopics [];
#
#   regulationTopics : TRegulationTopics [];
#
#   companyName : TClientName | null ;
#   source?: string;
#   updateTs? : string;
# }
######################################################################################################
######################################################################################################


# Equivalent of TUBCategory
UB_CATEGORIES = [
    'ביטוח',
    'רגולציה',
    'פרטי התקשרות'
]

# Equivalent of TDocType
UB_DOC_TYPE = [
    'גילוי נאות',
    'תנאי ביטוח',
    'חוק',
    'תקנון',
    'חוזר',
    'מדד'
]

# Equivalent of TInsuranceDepartment
UB_INSURANCE_DEPARTMENT = [
    "בריאות",          # Health
    "חיים",           # Life
    "חא\"ט",  # Long-term savings (חסכון ארוך טווח)
    # "חאט",  # Long-term savings (חסכון ארוך טווח)
]


# From TInsuranceTopicBriut
UB_INSURANCE_TOPIC_BRIUT = [
    'בסיס פרטי - תרופות מחוץ לסל',
    'בסיס פרטי - השתלות וטיפולים בחול',
    'בסיס פרטי - ניתוחים בחול',
    'ניתוחים ישראל - שב"ן ללא השתתפות',
    'ניתוחים ישראל - שב"ן עם השתתפות',
    'ניתוחים ישראל - שקל ראשון',
    'אמבולטורי - ייעוץ ובדיקות',
    'אמבולטורי - ייעוץ מורחב',
    'נוספים - אבחון מהיר',
    'נוספים - ליווי או יעוץ רפואי',
    'נוספים - התפתחות הילד',
    'נוספים - טכנולוגי ואביזרים',
    'שירות - רופא עד הבית',
    'שירות - רפואה משלימה',
    'שירות - אישי אונליין',
    'מידע - וכיסויים נוספים',
    'מידע - מחירונים ומידע נוסף',
    'מחלות קשות - קשות מלא',
    'מחלות קשות - קשות סרטן',
    'תאונות אישיות - תאונות',
    'תאונות אישיות - נכות'
]

# From TInsuranceTopicHaim
UB_INSURANCE_TOPIC_HAIM = [
    'חיים - חיים (פיצוי חד פעמי)',
    'חיים - חודשי / פרמיה משתנה',
    'חיים - הכנסה למשפחה',
    'חיים - מוות מתאונה',
    'חיים - נכות מתאונה',
    'משכנתא - חיים למשכנתא',
    'משכנתא - דירה למשכנתא',
    'מטריה (השלמה לפנסיה) - מטריה ביטוחית',
    'מטריה (השלמה לפנסיה) - נספחים / הרחבות',
    'אובדן כושר עבודה - בסיס',
    'אובדן כושר עבודה - הרחבות',
    'נכויות - נכויות',
    'נכויות - נכות מוחלטת',
    'תנאי חיתום'
]

# From TInsuranceTopicHAT
UB_INSURANCE_TOPIC_HAT = [
    'קרן פנסיה - מקיפה',
    'קרן פנסיה - משלימה',
    'קרן פנסיה - תקציר',
    'ביטוח מנהלים - שכיר',
    'ביטוח מנהלים - שכיר קצבה לא משלמת',
    'ביטוח מנהלים - עצמאי',
    'גמל (תגמולים ופיצויים) - תגמולים ופיצויים',
    'גמל (תגמולים ופיצויים) - קופה מרכזית לפיצויים',
    'קרן השתלמות - תקנון -קרן השתלמות',
    'גמל להשקעה - תקנון - קופת גמל להשקעה',
    'פוליסת חסכון - תנאים כללים',
    'פוליסת חסכון - נספח',
    'פוליסת חסכון - תנאים פוליסה "אנונה"'
]

# From TInsuranceTopics (concatenation of the above)
UB_INSURANCE_TOPICS = UB_INSURANCE_TOPIC_BRIUT + UB_INSURANCE_TOPIC_HAIM + UB_INSURANCE_TOPIC_HAT

# TRegulationTopics
UB_REGULATIONS_TOPICS = LAW_TYPES




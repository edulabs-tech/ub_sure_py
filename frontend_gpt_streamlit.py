import json
import re
import uuid

import pyperclip
import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage
import time
from streamlit_float import *

from ub_sure_agent_2 import ub_sure_agent_executor_6
from bs4 import BeautifulSoup # For stripping HTML for copy
import html # For escaping text


# ------------ CSS for Full RTL ------------
css = '''
<style>
html, body, .stApp {
  direction: rtl !important;
  text-align: right !important;
}
.loader {
  border: 4px solid rgba(0,0,0,0.1);
  border-top: 4px solid #3498db;
  border-radius: 50%;
  width: 24px;
  height: 24px;
  animation: spin 1s linear infinite;
  display: inline-block;
  vertical-align: middle;
  margin-left: 8px;
}
@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.copy-btn-html { /* Style for the HTML button */
    background-color: #f0f2f6;
    color: #31333F;
    border: 1px solid #ced4da;
    border-radius: .25rem;
    padding: .2rem .4rem;
    font-size: .8rem; /* Material icon might need slightly larger font or direct SVG sizing */
    cursor: pointer;
    margin-top: 8px;
    margin-right: 5px; /* RTL */
    display: inline-block;
    line-height: 1; /* Helps align icon if it's text */
    vertical-align: middle; /* Align with text if needed */
}
.copy-btn-html:hover {
    background-color: #e2e6ea;
}
.copy-btn-html svg { /* If using an SVG icon inside the button */
    width: 1em; /* Adjust size */
    height: 1em; /* Adjust size */
    fill: #31333F; /* Icon color */
    vertical-align: middle;
}

 
 div[data-testid="stHorizontalBlock"] > div:nth-child(1) div[data-testid="stButton"] button {
    /* Default button padding is often around 0.25rem top/bottom. */
    /* Expander headers often have around 0.5rem top/bottom padding. */
    /* Adjust these values to achieve visual alignment. Start by matching expander padding. */
    padding-top: 0.5rem;    /* Experiment with this value (e.g., 0.45rem, 0.5rem, 0.55rem) */
    padding-bottom: 0.5rem; /* Experiment with this value */
    height: 100%; /* Optional: try to make the button fill the column's height */
                 /* This works best if the column itself has a determined height or aligns items by stretching */
    box-sizing: border-box; /* Ensures padding is included in the total height */
    display: flex; /* Allows vertical alignment of button content */
    align-items: center; /* Vertically centers the text/icon within the button */
    justify-content: center; /* Horizontally centers the text/icon */
}

/* More robust selector to target the columns holding expanders */
div[data-testid="stHorizontalBlock"] > div:nth-child(2), /* Second column (col_explain_actions) */
div[data-testid="stHorizontalBlock"] > div:nth-child(3)  /* Third column (col_organize_actions) */
{
    flex-grow: 1 !important; /* Allow them to grow */
    flex-shrink: 1 !important; /* Allow them to shrink if needed but try to maintain space */
    /* Set a minimum width if you want to prevent them from becoming too narrow.
       This needs careful tuning. 'vw' units (viewport width) can be useful. */
    min-width: 120px !important; /* Example: Adjust as needed */
    /* Or use percentage of the stHorizontalBlock if that makes more sense */
    /* min-width: 35% !important; /* Adjust percentage */

    /* Ensure they don't break onto new lines if Streamlit tries to force it */
    /* display: inline-block !important; /* or flex, depending on internal structure */
    /* vertical-align: top !important; */
}

div[data-testid="stHorizontalBlock"] > div:nth-child(1) div[data-testid="stButton"] button {
    padding-top: 0.5rem;
    padding-bottom: 0.5rem;
    height: 100%;
    box-sizing: border-box;
    display: flex;
    align-items: center;
    justify-content: center;
}

div[data-testid="stExpander"] summary {
    padding-top: 0.2rem !important;    /* Reduce top padding */
    padding-bottom: 0.2rem !important; /* Reduce bottom padding */
    padding-right: 0.2rem !important;  /* Adjust right padding if needed for RTL */
    padding-left: 0.2rem !important;   /* Adjust left padding if needed */
    
    margin-bottom: 0 !important;
}

div[data-testid="stExpander"] div[data-testid="stButton"] button > div {
    width: 100%; /* Ensure the inner div takes full width */
    text-align: right !important;
    margin-top: 0 !important;
    margin-bottom: 0 !important;
    font-size: .8rem;
    line-height: 0.1rem;
    padding : 0.1rem;
}

div[data-testid="stExpander"] div[role="region"] > div > div[data-testid="stButton"] {
    /* This targets the div that might be wrapping each button when use_container_width=True */
    margin-bottom: 0px !important; /* Adjust this small margin as needed */
}

div[data-testid="stExpander"] div[role="region"] div[data-testid="stButton"] button > div {
    line-height: 1.2 !important; /* Adjust line-height for text within buttons */
    /* font-size: 0.85rem !important; */ /* Adjust font size if needed */
}



div[data-testid="stChatMessage"] {
    padding-top: 0.3rem !important;    /* Adjust this value (e.g., 0.2rem, 0.3rem, 5px) */
    padding-bottom: 0.3rem !important; /* Adjust this value */
    padding-left: 0.1rem !important;   /* Adjust this value (e.g., 0.5rem, 0.6rem, 8px) */
    padding-right: 0.1rem !important;  /* Adjust this value */
}
div[data-testid="stChatMessage"][data-chat-message-container-name="assistant"] div[data-testid="stMarkdownContainer"] p {
    margin-top: 0.1rem !important;
    margin-bottom: 0.2rem !important; /* Adjust space after paragraphs */
}




</style>
'''

button_icon_css = """
<style>
/* Target SVG icons within Streamlit buttons */
/* This will change ALL button icons. Be more specific if needed. */
div[data-testid="stButton"] button svg {
    fill: #0000FF; /* e.g., blue or #0000FF */
}
</style>
"""


# ------------ Source formatting functions ------------
def build_source_html(source_url, index, name_of_the_link,
                      page, total_pages, start_line, end_line, joined_fields):
    html = (
        f'<div style="margin: 0.75em 0; direction: rtl; text-align: right; white-space: pre-line; font-size: 0.9em;">'
        f'  <div>'
        f'    <a href="{source_url}" target="_blank" rel="noopener noreferrer" style="color: blue; text-decoration: none;">'
        f'[{index}]</a> '
        f'    <a href="{source_url}" target="_blank" rel="noopener noreferrer" style="color: blue; text-decoration: none;">'
        f'{name_of_the_link}</a>'
        f'  </div>'
        f'  <div>'
        f'    עמוד {page} מתוך {total_pages}, שורות {start_line}-{end_line}.'
        f'  </div>'
        f'  <div>{joined_fields}</div>'
        f'</div>'
    )
    return html


def format_source(doc, index):
    md = doc.metadata or {}

    # Helper to normalize metadata values (handles lists or single values)
    def normalize(key):
        val = md.get(key)
        if isinstance(val, (list, tuple)):
            return ", ".join(str(v) for v in val)
        return str(val) if val is not None else "Unknown"

    # Extract metadata fields
    company = normalize('companyName')
    dept_type = normalize('type')
    doc_type = normalize('docType')
    category = normalize('category')
    doc_category = normalize('docCategory')
    doc_subcategory = normalize('docSubCategory')
    insurance_department = normalize('insuranceDepartment')

    # Page and total pages (increment page if numeric)
    page_val = md.get('page')
    try:
        page = int(page_val) + 1
    except (TypeError, ValueError):
        page = normalize('page')
    total_pages = normalize('totalPages')

    # Location lines if present
    loc = md.get('loc', {}) or {}
    lines = loc.get('lines', {}) or {}
    start_line = lines.get('from', 'Unknown')
    end_line = lines.get('to', 'Unknown')

    # Source URL and display name
    source_url = md.get('source', '#') or '#'
    name_of_the_link = source_url.split('/')[-1]

    # Build display fields list
    fields = [company]
    for part in (dept_type, doc_type, category, doc_category, doc_subcategory, insurance_department):
        if part and part != 'Unknown':
            fields.append(part)
    joined_fields = ' | '.join(fields)

    # Generate HTML snippet
    return build_source_html(
        source_url, index, name_of_the_link,
        page, total_pages, start_line, end_line,
        joined_fields
    )

# ------------ Streamlit App ------------
user_avatar = "ub_sure/images/avatar.png"
# user_avatar = "ub_sure/images/user_avatar.png"

ub_logo = "ub_sure/images/ub_logo.jpeg"
ub_avatar = "ub_sure/images/ub_avatar.jpg"

def copy_clicked(input):
    # pyperclip.copy(input)
    cleaned_text = re.sub(r"<details.*?</details>", "", input, flags=re.DOTALL)
    pyperclip.copy(cleaned_text)

def main():
    st.set_page_config(
        page_title="UB Sure",
        page_icon=ub_logo,
        initial_sidebar_state="collapsed"
    )
    st.markdown(css, unsafe_allow_html=True)
    # st.markdown(button_icon_css, unsafe_allow_html=True)

    # float_init()

    if 'history' not in st.session_state:
        st.session_state.history = []
    if 'thread_id' not in st.session_state:
        st.session_state.thread_id = str(uuid.uuid4())
    # Initialize a key for the selected action from the "dropdown"
    if 'selected_action_prompt' not in st.session_state:
        st.session_state.selected_action_prompt = None

    with st.sidebar:
        st.logo(ub_logo)
        st.markdown("<h2 style='text-align: right;'>ניווט</h2>", unsafe_allow_html=True)
        if st.button("צ'אט חדש", key="new_chat_sidebar", use_container_width=True):
            st.session_state.history = []
            st.session_state.thread_id = str(uuid.uuid4())
            st.session_state.selected_action_prompt = None  # Reset action on new chat
            st.rerun()
        st.markdown("---")

    # Display past messages
    for i, msg in enumerate(st.session_state.history):
        avatar_to_use = user_avatar if msg['role'] == 'user' else ub_avatar
        with st.chat_message(msg['role'], avatar=avatar_to_use):
            st.markdown(msg['content'], unsafe_allow_html=msg.get('is_html', False))
            # if msg['role'] == 'assistant':
            #     st.button(
            #         "",
            #         type="secondary",
            #         on_click=copy_clicked,
            #         icon=":material/content_copy:",
            #         args=[msg['content']],
            #         key=f"copy_msg_{st.session_state.thread_id}_{i}",
            #         help="העתק תשובה זו"
            #     )

    # --- Action "Dropdown" Menu (conditionally displayed above chat_input) ---
    # We use st.session_state to store the chosen prompt from the action buttons
    # This needs to be reset after processing.

    if st.session_state.history and st.session_state.history[-1]['role'] == 'assistant':
        last_assistant_message_content = st.session_state.history[-1]['content']

        action_prompts = {
            # --- Organization & Wording Group ---
            "organize_for_email": {
                "label": "✉️ סדר למייל",
                "prompt": "עצב מחדש את התגובה הקודמת כך שתהיה מנוסחת כגוף של אימייל, עם פתיחה כללית פשוטה וסיום כללי פשוט, בלי שמות ובלי שימוש בתבניות."
            },
            "organize_for_message": {
                "label": "📱 סדר להודעה קצרה",
                "prompt": "עצב מחדש את התגובה הקודמת כהודעת טקסט קצרה ותמציתית, המתאימה למסרון או וואטסאפ."
            },
            "organize_in_table": {
                "label": "📊 סדר בטבלה",
                "prompt": "ארגן את המידע בטבלה עם כותרות מתאימות ופורמט ברור."
            },
            "rephrase_formal": {
                "label": "👔 נסח רשמית יותר",
                "prompt": "נסח מחדש את התגובה הקודמת בטון רשמי ומקצועי יותר."
            },
            "rephrase_friendly": {
                "label": "😊 נסח ידידותית יותר",
                "prompt": "נסח מחדש את התגובה הקודמת בטון פחות רשמי ויותר ידידותי ונגיש."
            },
            "extract_key_data": {
                "label": "🎯 חלץ נתוני מפתח",
                "prompt": "חלץ מהתגובה הקודמת את כל הסכומים הכספיים, תאריכים חשובים, שמות גורמים רלוונטיים ומספרי פוליסה/תביעה, אם קיימים, וארגן אותם ברשימה."
            },


            # --- Understanding & Detail Group ---
            "provide_more_info": {
                "label": "➕ מידע נוסף",
                # "prompt": "הרחב את התגובה הקודמת שלך או ספק פרטים נוספים."
                "prompt": "תרחיב את התשובה שלך עם פרטים נוספים. אם אין ברשותך מידע נוסף, בצע חיפוש מורחב בנושא והצג ממצאים רלוונטיים."
            },
            "summarize_info": {
                "label": "📝 סכם את המידע",
                "prompt": "סכם את הנקודות העיקריות בצורה תמציתית."
            },
            "explain_simply_and_shortly": {
                "label": "💡 הסבר בפשטות",
                "prompt": "הסבר את התגובה הקודמת שלך בצורה פשוטה, ברורה וקצרה ככל האפשר, כאילו אתה מסביר למישהו ללא ידע מוקדם בנושא."
            },
            "provide_examples": {
                "label": "📝 הצג דוגמאות",
                "prompt": "אם רלוונטי, ספק דוגמה אחת או שתיים להמחשת הנקודות העיקריות בתגובה הקודמת."
            },


        }

        # --- This is the part to be replaced in your main() function ---
        # Assume 'last_assistant_message_content' is available here
        # Assume 'copy_clicked' function is defined
        # Assume 'st.session_state.selected_action_prompt' is initialized

        # For RTL, columns are laid out from right to left.
        # col_copy_last will be right-most, col_explain_actions middle, col_organize_actions left-most.
        col_copy_last, col_explain_actions, col_organize_actions, nothing = st.columns([5, 30, 30, 35])  # Adjust ratios as needed

        with col_copy_last:
            st.button(
                "",  # Icon for copy
                key="copy_last_msg_action_bar",
                on_click=copy_clicked,
                icon=":material/content_copy:",
                type="tertiary",
                args=[last_assistant_message_content],  # Make sure this variable holds the last AI message
                use_container_width=True,
                help="העתק את התשובה האחרונה של יובי"
            )

        with col_explain_actions:
            with st.expander("🤔 הבנה ופירוט", expanded=False):  # First dropdown-like menu (middle column)
                actions_for_explain_group = [
                    "provide_more_info",
                    "summarize_info",
                    "explain_simply_and_shortly",
                ]
                for action_key in actions_for_explain_group:
                    if action_key in action_prompts:
                        action_details = action_prompts[action_key]
                        if st.button(action_details["label"], key=f"action_{action_key}", use_container_width=True, type="tertiary"):
                            st.session_state.selected_action_prompt = action_details["prompt"]
                            st.rerun()

        with col_organize_actions:
            with st.expander("✍️ ארגון וניסוח", expanded=False, ):  # Second dropdown-like menu (left-most column)
                actions_for_organize_group = [
                    "organize_in_table",
                    "organize_for_email",
                    "organize_for_message",
                    "rephrase_formal",  # New
                    "rephrase_friendly",  # New
                    "extract_key_data"  # New
                ]
                for action_key in actions_for_organize_group:
                    if action_key in action_prompts:
                        action_details = action_prompts[action_key]
                        if st.button(action_details["label"], key=f"action_{action_key}", use_container_width=True, type="tertiary"):
                            st.session_state.selected_action_prompt = action_details["prompt"]
                            st.rerun()
        # --- End of the replacement part ---

    typed_prompt = st.chat_input("שאל את יובי")
    actual_prompt_to_process = None

    if st.session_state.selected_action_prompt:
        actual_prompt_to_process = st.session_state.selected_action_prompt
        st.session_state.selected_action_prompt = None  # Reset after capturing
    elif typed_prompt:
        actual_prompt_to_process = typed_prompt

    if actual_prompt_to_process:
        st.chat_message("user", avatar=user_avatar).markdown(actual_prompt_to_process)
        st.session_state.history.append({'role': 'user', 'content': actual_prompt_to_process})

        accumulated_content = ""
        sources_html_parts = []
        tool_used = False
        tool_args_buffer = ""
        assistant_placeholder = None
        tool_placeholder = None

        current_thread_id = st.session_state.thread_id
        for step, metadata in ub_sure_agent_executor_6.stream(
                {"messages": [HumanMessage(content=actual_prompt_to_process)]},
                config={"configurable": {"thread_id": current_thread_id}},
                stream_mode="messages",
        ):


            if hasattr(step, 'tool_calls') and step.tool_calls:
                if not tool_used:
                    tool_used = True
                    if tool_placeholder is None:
                        # tool_placeholder = st.chat_message("assistant", avatar=ub_avatar).empty()
                        tool_placeholder = st.chat_message("assistant", avatar=ub_avatar)

                if assistant_placeholder is None:
                    assistant_placeholder = st.chat_message("assistant", avatar=ub_avatar).empty()
                    assistant_placeholder.markdown("<span>יובי חושב...</span><span class='loader'></span>",
                                                   unsafe_allow_html=True)

            if hasattr(step, 'tool_call_chunks'):
                for chunk in step.tool_call_chunks:
                    args_data = chunk.get("args", "");
                    if isinstance(args_data, str): tool_args_buffer += args_data
                try:
                    if tool_placeholder and tool_args_buffer and \
                            tool_args_buffer.strip().startswith('{') and \
                            tool_args_buffer.strip().endswith('}'):
                        tool_args = json.loads(tool_args_buffer);
                        query_value = tool_args.get("query", "")
                        if query_value:
                            tool_placeholder.markdown(f"<span>🛠️ יובי מחפש: {query_value}</span>",unsafe_allow_html=True)
                            tool_message_str = f"<span>🛠️ יובי מחפש: {query_value}</span>"

                            # Display tool forever.
                            st.session_state.history.append(
                                {'role': 'assistant', 'content': tool_message_str, 'is_html': True})

                        tool_args_buffer = ""
                except (json.JSONDecodeError, Exception):
                    pass

            if metadata.get("langgraph_node") == "agent" and hasattr(step, 'text') and (text := step.text()):
                if assistant_placeholder is None:
                    assistant_placeholder = st.chat_message("assistant", avatar=ub_avatar).empty()

                if not text.strip(): continue
                accumulated_content += text
                if assistant_placeholder:
                    assistant_placeholder.markdown(f"{accumulated_content}", unsafe_allow_html=True)
                else:
                    st.chat_message("assistant", avatar=ub_avatar).markdown(f"{accumulated_content}",
                                                                            unsafe_allow_html=True)

            if hasattr(step, 'artifact') and (artifact_data := step.artifact):
                if artifact_data:
                    formatted_sources = [format_source(doc_item, idx) for idx, doc_item in
                                         enumerate(artifact_data, start=1)]
                    if formatted_sources: sources_html_parts.extend(formatted_sources)

        final_response_text_for_history = accumulated_content
        final_display_content = accumulated_content
        is_html_content = False
        sources_block_html = ""

        if sources_html_parts:
            details = "".join(sources_html_parts)
            sources_block_html = (
                f"<details style='direction: rtl; text-align: right; font-size:0.95em; margin-top:0.5em; margin-bottom:0.5em;'>"
                f"<summary style='border: 2px solid #eee; padding: 0.3em 0.6em; border-radius: 0.4em; cursor: pointer; display: inline-block;'>📑 מקורות</summary>"
                f"<div style='white-space: pre-line; margin:0.5em 0 0 1em;'>{details}</div>"
                f"</details>"
            )
            final_display_content += ("\n\n" + sources_block_html)
            final_response_text_for_history += ("\n\n" + sources_block_html)
            is_html_content = True

        if assistant_placeholder:
            if accumulated_content.strip() or sources_html_parts:
                assistant_placeholder.markdown(final_display_content, unsafe_allow_html=True)
            else:
                assistant_placeholder.empty()
        elif accumulated_content.strip() or sources_html_parts:
            st.chat_message("assistant", avatar=ub_avatar).markdown(final_display_content, unsafe_allow_html=True)

        if accumulated_content.strip() or sources_html_parts:
            st.session_state.history.append(
                {'role': 'assistant', 'content': final_display_content, 'is_html': is_html_content})
        st.rerun()

if __name__ == "__main__":
    main()

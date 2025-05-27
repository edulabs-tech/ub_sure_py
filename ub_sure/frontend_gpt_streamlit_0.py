# import os
# import streamlit as st
# from langchain_core.messages import HumanMessage, AIMessage
#
# from ub_sure_agent_gpt import ub_sure_agent_executor
#
#
# # ------------ CSS for Full RTL and chat container ------------
# css = '''
# <style>
# /* Apply RTL globally */
# html, body, .stApp {
#   direction: rtl !important;
#   text-align: right !important;
# }
# /* Chat container styling */
# .chat-container {
#   max-height: 70vh;
#   overflow-y: auto;
#   padding-right: 1em;
# }
# .chat-message-user, .chat-message-assistant {
#   margin-bottom: 0.5em;
# }
# </style>
# '''
#
# # ------------ Source formatting functions ------------
# def build_source_html(source_url, index, name_of_the_link,
#                       page, total_pages, start_line, end_line, joined_fields):
#     html = (
#         f'<div style="direction: rtl; text-align: right; white-space: pre-line; font-size: 0.75em;">'
#         f'  <div>'
#         f'    <a href="{source_url}" target="_blank" rel="noopener noreferrer" style="color: blue; text-decoration: none;">'
#         f'[{index}]</a> '
#         f'    <a href="{source_url}" target="_blank" rel="noopener noreferrer" style="color: blue; text-decoration: none;">'
#         f'{name_of_the_link}</a>'
#         f'  </div>'
#         f'  <div>'
#         f'    עמוד {page} מתוך {total_pages}, שורות {start_line}-{end_line}.'
#         f'  </div>'
#         f'  <div>{joined_fields}</div>'
#         f'</div>'
#     )
#     return html
#
#
# def format_source(doc, index):
#     md = doc.metadata
#     company = md.get('companyName', 'Unknown')
#     doc_type = md.get('docType', 'Unknown')
#     insurance_type = md.get('insuranceType', 'Unknown')
#     coverage_type = md.get('coverageType', 'Unknown')
#     category = md.get('docCategory', 'Unknown')
#     sub_category = md.get('docSubCategory', 'Unknown')
#     page = md.get('page', 'Unknown')
#     total_pages = md.get('totalPages', 'Unknown')
#     try:
#         page = int(page) + 1
#     except (ValueError, TypeError):
#         pass
#     loc = md.get('loc', {})
#     lines = loc.get('lines', {})
#     start_line = lines.get('from', 'Unknown')
#     end_line = lines.get('to', 'Unknown')
#     source_url = md.get('source', '#')
#     name_of_the_link = source_url.split('/')[-1]
#     fields = [company]
#     if doc_type != "Unknown": fields.append(doc_type)
#     if insurance_type != "Unknown": fields.append(insurance_type)
#     if coverage_type != "Unknown": fields.append(coverage_type)
#     if category != "Unknown": fields.append(category)
#     if sub_category != "Unknown": fields.append(sub_category)
#     joined_fields = ' | '.join(fields)
#     return build_source_html(source_url, index, name_of_the_link,
#                               page, total_pages, start_line, end_line, joined_fields)
#
# # ------------ Streamlit App ------------
# def main():
#     st.set_page_config(page_title="UB Sure Chatbot")
#     st.markdown(css, unsafe_allow_html=True)
#
#     # Initialize chat history
#     if 'history' not in st.session_state:
#         st.session_state.history = []
#
#     # Display existing messages
#     for msg in st.session_state.history:
#         if msg['role'] == 'user':
#             st.markdown(f"<div class='chat-message-user'>**You:** {msg['content']}</div>", unsafe_allow_html=True)
#         else:
#             if msg.get('is_html'):
#                 st.markdown(f"<div class='chat-message-assistant'>{msg['content']}</div>", unsafe_allow_html=True)
#             else:
#                 st.markdown(f"<div class='chat-message-assistant'>**Assistant:** {msg['content']}</div>", unsafe_allow_html=True)
#
#     # Input prompt
#     prompt = st.chat_input("הודעת צ'אט")
#     if prompt:
#         st.session_state.history.append({'role': 'user', 'content': prompt})
#         st.markdown(f"<div class='chat-message-user'>**You:** {prompt}</div>", unsafe_allow_html=True)
#
#         placeholder = st.empty()
#         assistant_content = ""
#         sources_html = ""
#
#         for event in ub_sure_agent_executor.stream(
#                 {"messages": [HumanMessage(content=prompt)]},
#                 config={"configurable": {"thread_id": "12345"}},
#                 stream_mode="values"
#         ):
#             last = event['messages'][-1]
#             if hasattr(last, 'artifact') and last.artifact:
#                 formatted_sources = [format_source(doc, idx)
#                                      for idx, doc in enumerate(last.artifact, start=1)]
#                 if formatted_sources:
#                     details = "".join(formatted_sources)
#                     sources_html = f"<details style='direction: rtl; text-align: right; font-size:0.75em; margin-top:0.5em;'>" \
#                                    f"<summary>📑 מקורות</summary><div style='white-space: pre-line; margin-left:1em;'>" \
#                                    f"{details}</div></details>"
#             if isinstance(last, AIMessage) and last.content:
#                 assistant_content += last.content
#                 display_html = assistant_content + ("\n\n" + sources_html if sources_html else "")
#                 placeholder.markdown(f"<div class='chat-message-assistant'>{display_html}</div>", unsafe_allow_html=True)
#
#         st.session_state.history.append(
#             {'role': 'assistant', 'content': assistant_content, 'is_html': bool(sources_html)}
#         )
#
# if __name__ == "__main__":
#     main()
#



import os
import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage
from ub_sure_agent_gpt import ub_sure_agent_executor

# ------------ CSS for Full RTL ------------
css = '''
<style>
html, body, .stApp {
  direction: rtl !important;
  text-align: right !important;
}
</style>
'''

# ------------ Source formatting functions ------------
def build_source_html(source_url, index, name_of_the_link,
                      page, total_pages, start_line, end_line, joined_fields):
    html = (
        f'<div style="direction: rtl; text-align: right; white-space: pre-line; font-size: 0.75em;">'
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
    md = doc.metadata
    company = md.get('companyName', 'Unknown')
    doc_type = md.get('docType', 'Unknown')
    insurance_type = md.get('insuranceType', 'Unknown')
    coverage_type = md.get('coverageType', 'Unknown')
    category = md.get('docCategory', 'Unknown')
    sub_category = md.get('docSubCategory', 'Unknown')
    page = md.get('page', 'Unknown')
    total_pages = md.get('totalPages', 'Unknown')
    try:
        page = int(page) + 1
    except (ValueError, TypeError):
        pass
    loc = md.get('loc', {})
    lines = loc.get('lines', {})
    start_line = lines.get('from', 'Unknown')
    end_line = lines.get('to', 'Unknown')
    source_url = md.get('source', '#')
    name_of_the_link = source_url.split('/')[-1]
    fields = [company]
    if doc_type != "Unknown": fields.append(doc_type)
    if insurance_type != "Unknown": fields.append(insurance_type)
    if coverage_type != "Unknown": fields.append(coverage_type)
    if category != "Unknown": fields.append(category)
    if sub_category != "Unknown": fields.append(sub_category)
    joined_fields = ' | '.join(fields)
    return build_source_html(source_url, index, name_of_the_link,
                              page, total_pages, start_line, end_line, joined_fields)

# ------------ Streamlit App ------------
def main():
    st.set_page_config(page_title="UB Sure Chatbot")
    st.markdown(css, unsafe_allow_html=True)

    # Initialize history
    if 'history' not in st.session_state:
        st.session_state.history = []  # each item: {role, content, is_html}

    # Display all past messages with icons
    for msg in st.session_state.history:
        if msg['role'] == 'user':
            st.chat_message("user").markdown(msg['content'], unsafe_allow_html=True)
        else:
            msg_block = st.chat_message("assistant")
            if msg.get('is_html'):
                msg_block.markdown(msg['content'], unsafe_allow_html=True)
            else:
                msg_block.markdown(msg['content'])

    # User input
    prompt = st.chat_input("הודעת צ'אט")
    if prompt:
        # show user message with icon
        st.chat_message("user").markdown(prompt)
        st.session_state.history.append({'role': 'user', 'content': prompt})

        # assistant placeholder for streaming
        assistant_block = st.chat_message("assistant")
        assistant_content = ""
        sources_html = ""

        # stream from agent
        for event in ub_sure_agent_executor.stream(
            {"messages": [HumanMessage(content=prompt)]},
            config={"configurable": {"thread_id": "12345"}},
            stream_mode="values"
        ):
            last = event['messages'][-1]
            # collect sources
            if hasattr(last, 'artifact') and last.artifact:
                formatted = [format_source(doc, idx)
                             for idx, doc in enumerate(last.artifact, start=1)]
                if formatted:
                    details = "".join(formatted)
                    sources_html = (
                        f"<details style='direction: rtl; text-align: right; font-size:0.75em; margin-top:0.5em;'>"
                        f"<summary>📑 מקורות</summary><div style='white-space: pre-line; margin-left:1em;'>"
                        f"{details}</div></details>"
                    )
            # accumulate assistant text
            if isinstance(last, AIMessage) and last.content:
                assistant_content += last.content
                combined = assistant_content + ("\n\n" + sources_html if sources_html else "")
                assistant_block.markdown(combined, unsafe_allow_html=True)

        # save assistant final
        st.session_state.history.append({
            'role': 'assistant',
            'content': assistant_content,
            'is_html': bool(sources_html)
        })

if __name__ == "__main__":
    main()

import os

from pprint import pprint
import gradio as gr
from gradio import ChatMessage, HTML
from langchain_core.messages import HumanMessage, AIMessage
from sqlalchemy.sql.operators import truediv

# Import your agent executors as needed
from ub_sure.ub_sure_agent_gpt import ub_sure_agent_executor

css = """
.chat-container .gr-chatbot {
  max-height: 70vh;        /* or whatever you prefer */
  overflow-y: auto;        /* vertical scrolling */
  padding-right: 1em;      /* give some breathing room */
}

.rtl {
    direction: rtl;
    text-align: right;
    height: 100%; /* Full viewport height */
    display: flex;
    flex-direction: column;
    overflow: auto; /* Enables scrolling if content overflows */
}
.chat-rows2{
    height: 100vh; /* Full viewport height */
    display: flex;
    flex-direction: column;
}
.chat-rows{

}
.full-height {
    display: flex;
    flex-direction: column;
}
.chat-container {
    direction: rtl;
    text-align: right;
    height : '100%';

}
.chat_msg {

}
"""

GRADIO_USERNAME = os.getenv('GRADIO_USERNAME')
GRADIO_PASS = os.getenv('GRADIO_PASS')

# def build_source_html(source_url, index, name_of_the_link, page, total_pages, start_line, end_line, joined_fields):
#     """
#     Builds an HTML snippet with right-to-left direction, styled links, and specific layout.
#
#     Parameters:
#         source_url (str): URL for the link.
#         index (int): The index to display.
#         name_of_the_link (str): The file name or descriptive text for the link.
#         page (int or str): The page number.
#         total_pages (int or str): Total number of pages.
#         start_line (int or str): Starting line number.
#         end_line (int or str): Ending line number.
#         joined_fields (str): Additional metadata fields joined as a string.
#
#     Returns:
#         str: An HTML formatted string.
#     """
#     html = (
#         f'<div style="direction: rtl; text-align: right; white-space: pre-line; font-size: 0.75em;">'
#         f'  <div>'
#         f'    <a href="{source_url}" style="color: blue; text-decoration: none;">[{index}]</a> '
#         f'    <a href="{source_url}" style="color: blue; text-decoration: none;">{name_of_the_link}</a>'
#         f'  </div>'
#         f'  <div>'
#         f'    עמוד {page} מתוך {total_pages}, שורות {start_line}-{end_line}.'
#         f'  </div>'
#         f'  <div>{joined_fields}</div>'
#         f'</div>'
#     )
#     return html

def build_source_html(
    source_url, index, name_of_the_link,
    page, total_pages, start_line, end_line, joined_fields
):
    """
    Builds an HTML snippet with right-to-left direction, styled links,
    opens in a new tab, and includes security-minded rel attributes.

    Parameters:
        source_url (str): URL for the link.
        index (int): The index to display.
        name_of_the_link (str): The file name or descriptive text.
        page (int or str): The page number.
        total_pages (int or str): Total number of pages.
        start_line (int or str): Starting line number.
        end_line (int or str): Ending line number.
        joined_fields (str): Additional metadata fields.

    Returns:
        str: An HTML formatted string.
    """
    # rel="noopener noreferrer" prevents the new page from accessing `window.opener`
    # target="_blank" opens link in a new tab :contentReference[oaicite:0]{index=0}
    html = (
        f'<div style="direction: rtl; text-align: right; '
        f'white-space: pre-line; font-size: 0.75em;">'
        f'  <div>'
        f'    <a href="{source_url}" '
        f'target="_blank" rel="noopener noreferrer" '
        f'style="color: blue; text-decoration: none;">'
        f'[{index}]</a> '
        f'    <a href="{source_url}" '
        f'target="_blank" rel="noopener noreferrer" '
        f'style="color: blue; text-decoration: none;">'
        f'{name_of_the_link}</a>'
        f'  </div>'
        f'  <div>'
        f'    עמוד {page} מתוך {total_pages}, שורות '
        f'{start_line}-{end_line}.'
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
        # If page is not a number, it will remain unchanged (or you can handle it as needed)
        pass


    loc = md.get('loc', {})
    lines = loc.get('lines', {})
    start_line = lines.get('from', 'Unknown')
    end_line = lines.get('to', 'Unknown')

    source_url = md.get('source', '#')
    name_of_the_link = source_url.split("/")[-1]

    fields = [company]
    if doc_type != "Unknown":
        fields.append(doc_type)
    if insurance_type != "Unknown":
        fields.append(insurance_type)
    if coverage_type != "Unknown":
        fields.append(coverage_type)
    if category != "Unknown":
        fields.append(category)
    if sub_category != "Unknown":
        fields.append(sub_category)

    joined_fields = " | ".join(fields)

    ret_html = build_source_html(source_url, index, name_of_the_link, page, total_pages, start_line, end_line, joined_fields)

    # Return an HTML snippet:
    # The clickable number is in blue on its own line.
    return ret_html


source_separator = "\n\n---------מקורות----------\n"


# def interact_with_langchain_agent( prompt, messages):
#     # Append the user prompt to the messages list
#     messages.append(ChatMessage(role="user", content=prompt))
#     sources_text = ""
#     thread_id = "12345"
#
#     for event in ub_sure_agent_executor.stream(...):
#         last = event["messages"][-1]
#
#         # collect your sources_text as you already do...
#         # …
#
#         if isinstance(last, AIMessage) and last.content:
#             # 1) The raw answer
#             answer = last.content
#
#             # 2) Wrap the sources in a <details> block for collapse/expand
#             if sources_text:
#                 sources_html = f"""
#     <details style="direction: rtl; text-align: right; font-size: 0.75em; margin-top:0.5em;">
#       <summary>📑 מקורות</summary>
#       <div style="white-space: pre-line; margin-left:1em;">
#         {sources_text}
#       </div>
#     </details>
#     """
#             # 3) Combine them
#             full_html = answer + "\n\n" + sources_html
#
#             # 4) Send as one chat bubble (HTML‐enabled)
#             messages.append(ChatMessage(
#                 role="assistant",
#                 content=full_html,
#                 metadata={"is_html": True}
#             ))
#             yield gr.update(value=""), messages
#
def interact_with_langchain_agent(prompt, history):
    # 1) Record the user’s question
    history.append(ChatMessage(role="user", content=prompt))

    # 2) Ensure sources_html is always defined
    sources_html = ""

    # 3) Stream through the agent’s responses
    for event in ub_sure_agent_executor.stream(
            {"messages": [HumanMessage(content=prompt)]},
            config={"configurable": {"thread_id": "12345"}},
            stream_mode="values"
    ):
        last_message = event["messages"][-1]

        # 4) If the agent returned artifact sources, format them
        if hasattr(last_message, "artifact") and last_message.artifact:
            formatted = [
                format_source(doc, idx)
                for idx, doc in enumerate(last_message.artifact, start=1)
            ]
            if formatted:
                details_block = "\n".join(formatted)
                sources_html = f"""
<details style="direction: rtl; text-align: right; font-size:0.75em; margin-top:0.5em;">
  <summary>📑 מקורות</summary>
  <div style="white-space: pre-line; margin-left:1em;">
    {details_block}
  </div>
</details>
"""

        # 5) When the agent emits content, add it plus sources
        if isinstance(last_message, AIMessage) and last_message.content:
            # a) The main answer
            history.append(ChatMessage(role="assistant", content=last_message.content))

            # b) Inline sources, as an HTML component
            if sources_html:
                history.append(ChatMessage(role="assistant", content=HTML(sources_html)))

            # 6) Yield back to Gradio to update UI
            yield "", history


if __name__ == "__main__":
    with gr.Blocks(css=css, title="UB Sure Chatbot") as demo:
        with gr.Row(elem_classes="chat-rows"):
            with gr.Column(scale=2):
                chatbot = gr.Chatbot(
                    value=[],
                    type="messages",
                    height='70vh',
                    rtl=True,
                    sanitize_html=False,  # ← allow HTML through
                    render_markdown=True,  # keep Markdown support
                    elem_classes="chat-container"
                )
                textbox = gr.Textbox(
                    lines=1,
                    label="Chat Message",
                    elem_classes="chat_msg"
                )
        textbox.submit(interact_with_langchain_agent,
                       inputs=[textbox, chatbot],
                       outputs=[textbox, chatbot])
    demo.launch()
from pprint import pprint
import gradio as gr
from gradio import ChatMessage
from langchain_core.messages import HumanMessage, AIMessage

from ub_sure_agent_vertex import ub_sure_agent_executor_vertex

# Import your agent executors as needed
# from ub_sure.ub_sure_agent_gpt import ub_sure_agent_executor

css = """
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
#
#     loc = md.get('loc', {})
#     lines = loc.get('lines', {})
#     start_line = lines.get('from', 'Unknown')
#     end_line = lines.get('to', 'Unknown')
#
#     source_url = md.get('source', '#')
#     name_of_the_link = source_url.split("/")[-1]
#
#     fields = [company]
#     if doc_type != "Unknown":
#         fields.append(doc_type)
#     if insurance_type != "Unknown":
#         fields.append(insurance_type)
#     if coverage_type != "Unknown":
#         fields.append(coverage_type)
#     if category != "Unknown":
#         fields.append(category)
#     if sub_category != "Unknown":
#         fields.append(sub_category)
#
#     joined_fields = " | ".join(fields)
#     return f"[[{index}]({source_url})] [{name_of_the_link}] {joined_fields} , עמוד {page} מתוך {total_pages}, שורות {start_line}-{end_line}."
#

def build_source_html(source_url, index, name_of_the_link, page, total_pages, start_line, end_line, joined_fields):
    """
    Builds an HTML snippet with right-to-left direction, styled links, and specific layout.

    Parameters:
        source_url (str): URL for the link.
        index (int): The index to display.
        name_of_the_link (str): The file name or descriptive text for the link.
        page (int or str): The page number.
        total_pages (int or str): Total number of pages.
        start_line (int or str): Starting line number.
        end_line (int or str): Ending line number.
        joined_fields (str): Additional metadata fields joined as a string.

    Returns:
        str: An HTML formatted string.
    """
    html = (
        f'<div style="direction: rtl; text-align: right; white-space: pre-line; font-size: 0.75em;">'
        f'  <div>'
        f'    <a href="{source_url}" style="color: blue; text-decoration: none;">[{index}]</a> '
        f'    <a href="{source_url}" style="color: blue; text-decoration: none;">{name_of_the_link}</a>'
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


def interact_with_langchain_agent( prompt, messages):
    # Append the user prompt to the messages list
    messages.append(ChatMessage(role="user", content=prompt))
    sources_text = ""
    thread_id = "12345"

    for event in ub_sure_agent_executor_vertex.stream(
            {"messages": [HumanMessage(content=prompt)]},
            config={"configurable": {"thread_id": thread_id}},
            stream_mode="values"
    ):
        last_message = event["messages"][-1]

        # If the message has artifact sources, format them
        if hasattr(last_message, "artifact") and last_message.artifact:
            sources = last_message.artifact
            formatted_sources = []
            for i, doc in enumerate(sources, start=1):
                formatted_sources.append(format_source(doc, i))
            if formatted_sources:
                sources_text = "\n".join(formatted_sources)

        # Process AI messages (including tool call messages)
        if isinstance(last_message, AIMessage):
            for tool_call in last_message.tool_calls:

                # pprint(f"last_message => {last_message}")
                # pprint(f"tool_call => {tool_call}")

                messages.append(ChatMessage(
                    role="assistant",
                    content=f"Query tool: {tool_call['args']['query']}",
                    metadata={"title": f"🛠️ Using tool {tool_call['name']}"}
                ))
                # Yield with empty sources update
                yield gr.update(value=""), messages, gr.update(value="")

            if len(last_message.content) > 0:
                output_content = last_message.content
                messages.append(ChatMessage(role="assistant", content=output_content))
                # Prepare the styled sources (only update the right side)
                styled_sources = (
                    f'''
                    <div style="text-align: right;">
                        <style>
                          .sources-container a {{
                             color: blue !important;
                          }}
                        </style>
                        <span class="sources-container" style="font-size: small; direction: rtl; white-space: pre-line">
                             {source_separator}{sources_text}
                        </span>
                    </div>
                    '''
                ) if sources_text else ""
                yield gr.update(value=""), messages, gr.update(value=styled_sources)


if __name__ == "__main__":
    with gr.Blocks(
            fill_height=True,
            fill_width=False,
            theme="soft",
            css=css,
            title= "Hello world"
    ) as demo:
        gr.Markdown("# UB Sure Chatbot - Gemini Test (Model: gemini-2.0-flash  : ± $0.3 per 1M tokens)")
        # with gr.Row(elem_classes="full-height"):
        with gr.Row(elem_classes="chat-rows"):

            # Left column: Chat UI
            with gr.Column(scale=2):
                # thread_textbox = gr.Textbox(placeholder="Thread ID")
                chatbot = gr.Chatbot(
                    type="messages",
                    label="Agent",
                    scale=2,
                    avatar_images=(
                        None,
                        "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcThr7qrIazsvZwJuw-uZCtLzIjaAyVW_ZrlEQ&s"
                    ),
                    # height=None,
                    height='70vh',
                    rtl=True,
                    elem_classes="chat-container"
                )
                textbox = gr.Textbox(lines=1,
                                     label="Chat Message",
                                     scale=1,
                                     elem_classes="chat_msg"
                                     )
            # Right column: Sources display
            with gr.Column(scale=1):
                sources_display = gr.HTML(label="Sources")

        # Update the submit to yield three outputs: textbox, chatbot, and sources_display.
        textbox.submit(interact_with_langchain_agent,
                       # [thread_textbox, textbox, chatbot],
                       [textbox, chatbot],

                       [textbox, chatbot, sources_display])
    demo.launch(share=False)

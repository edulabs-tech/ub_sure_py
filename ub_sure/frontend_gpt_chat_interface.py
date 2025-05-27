from pprint import pprint
import gradio as gr
from gradio import ChatMessage
from langchain_core.messages import HumanMessage, AIMessage

from front_end_helpers import format_source, source_separator
# Import your agent executors as needed
from ub_sure.ub_sure_agent_gpt import ub_sure_agent_executor
from ub_sure_agent_vertex import ub_sure_agent_executor_vertex


def interact_with_langchain_agent(thread_id, prompt, messages):
    # Append the user prompt to the messages list
    messages.append(ChatMessage(role="user", content=prompt))
    sources_text = ""

    for event in ub_sure_agent_executor.stream(
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
                messages.append(ChatMessage(
                    role="assistant",
                    content="",
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
    with gr.Blocks(fill_height=True, theme="ocean") as demo:
        gr.Markdown("# UB Sure Chatbot - ChatGpt Test")
        with gr.Row():
            # Left column: Chat UI
            with gr.Column(scale=2):
                thread_textbox = gr.Textbox(placeholder="Thread ID")
                chatbot = gr.Chatbot(
                    type="messages",
                    label="Agent",
                    avatar_images=(
                        None,
                        "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT4qGp0_wJsHQuVb_F7Lz0mVlMu81-4lf2rsw&s"
                    ),
                    # height='60vh',
                    rtl=True
                )
                textbox = gr.Textbox(lines=1, label="Chat Message")
            # Right column: Sources display
            with gr.Column(scale=1):
                sources_display = gr.HTML(label="Sources")

        # Update the submit to yield three outputs: textbox, chatbot, and sources_display.
        textbox.submit(interact_with_langchain_agent,
                       [thread_textbox, textbox, chatbot],
                       [textbox, chatbot, sources_display])
    demo.launch(share=False)

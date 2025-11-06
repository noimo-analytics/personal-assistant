import gradio as gr
from assistant import Assistant


async def setup():
    assistant = Assistant()
    await assistant.setup()
    return assistant

async def process_message(assistant, message, success_criteria, history):
    results = await assistant.run_superstep(message, success_criteria, history)
    return results, assistant
    
async def reset():
    new_assistant = Assistant()
    await new_assistant.setup()
    return "", "", None, new_assistant

def free_resources(assistant):
    print("Cleaning up")
    try:
        if assistant:
            assistant.free_resources()
    except Exception as e:
        print(f"Exception during cleanup: {e}")


with gr.Blocks(title="Assistant", theme=gr.themes.Default(primary_hue="emerald")) as ui:
    gr.Markdown("## Personal Assistant")
    assistant = gr.State(delete_callback=free_resources)
    
    with gr.Row():
        chatbot = gr.Chatbot(label="Assistant", height=300, type="messages")
    with gr.Group():
        with gr.Row():
            message = gr.Textbox(show_label=False, placeholder="Your request to the Assistant")
        with gr.Row():
            success_criteria = gr.Textbox(show_label=False, placeholder="What are your success critiera?")
    with gr.Row():
        reset_button = gr.Button("Reset", variant="stop")
        go_button = gr.Button("Go!", variant="primary")
        
    ui.load(setup, [], [assistant])
    message.submit(process_message, [assistant, message, success_criteria, chatbot], [chatbot, assistant])
    success_criteria.submit(process_message, [assistant, message, success_criteria, chatbot], [chatbot, assistant])
    go_button.click(process_message, [assistant, message, success_criteria, chatbot], [chatbot, assistant])
    reset_button.click(reset, [], [message, success_criteria, chatbot, assistant])

    
ui.launch(inbrowser=True)
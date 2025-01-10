from agents import main_agent
from swarm import Swarm
import gradio as gr

swarm_client = Swarm()
agent = main_agent

def chat(prompt, history):
    history.append({'role': 'user', 'content': prompt})
    response = swarm_client.run(
        agent=agent,
        debug=False,
        messages=history
    )
    history.append({'role': 'assistant', 'content': response.messages[-1]['content']})
    return history, history

with gr.Blocks() as demo:
    gr.Markdown("# Create A Google Calendar AI Agent")
    chatbot = gr.Chatbot(type='messages')
    state = gr.State([])  # Initialize state with an empty list
    with gr.Row():
        with gr.Column(scale=4):
            txt = gr.Textbox(show_label=False, placeholder="Enter your prompt here", scale=4)
        with gr.Column(scale=1):
            btn = gr.Button("Submit")

    btn.click(chat, inputs=[txt, state], outputs=[chatbot, state])

demo.launch()

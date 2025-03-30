import gradio as gr
from text2sql import agent  

def process_query(query: str, show_full_prompt: bool) -> str:
    """
    Process the natural language SQL query using the agent.
    Extracts only the "output" field from the result dictionary.
    """
    # Execute the query using the agent
    result = agent.invoke(query)
    
    # If result is a dict, extract the "output" key, otherwise use the result directly.
    if isinstance(result, dict):
        output = result.get("output", "")
    else:
        output = str(result)
    
    return output

# Create the Gradio Interface
iface = gr.Interface(
    fn=process_query,
    inputs=[
        gr.components.Textbox(lines=2, label="SQL Natural Language Query", placeholder="Enter your SQL query here..."),
    ],
    outputs=gr.components.Textbox(label="Query Result"),
    title="Text2SQL Toolkit Demo",
    description="Enter a natural language query to run against your SQL database. Press Enter to submit."
)

if __name__ == "__main__":
    iface.launch()












# # import gradio as gr
# # from text2sql import agent  

# # def process_query(query: str, show_full_prompt: bool) -> str:
# #     """
# #     Process the natural language SQL query using the agent.
# #     Extracts only the "output" field from the result dictionary.
# #     """
# #     result = agent.invoke(query)
# #     if isinstance(result, dict):
# #         output = result.get("output", "")
# #     else:
# #         output = str(result)
# #     return output

# # with gr.Blocks() as demo:
# #     gr.Markdown("## Text2SQL Toolkit Demo")
# #     query_input = gr.Textbox(lines=2, label="SQL Natural Language Query")
# #     show_full_prompt = gr.Checkbox(label="Show Full Prompt", value=False)
# #     output_box = gr.Textbox(label="Query Result")
# #     submit_btn = gr.Button("Submit")
    
# #     submit_btn.click(fn=process_query, inputs=[query_input, show_full_prompt], outputs=output_box)

# # demo.launch()


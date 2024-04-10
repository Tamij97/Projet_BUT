# Author: Bastien & Pascal
# Date: 2/25/2024
# Project: SAE-GPT2 | BUT 3 Informatique - Semester 5

# Import of required libraries 
import os

os.system("pip install --upgrade pip")
os.system("pip install googletrans-py")
os.system("pip install tensorflow==2.15.0")
os.system("pip install keras-nlp")
os.system("pip install -q --upgrade keras") # Upgrade Keras to version 3

import time
import keras
import keras_nlp
import pandas as pd
import gradio as gr
from googletrans import Translator
from importHuggingFaceHubModel import from_pretrained_keras

# Set Keras Backend to Tensorflow
os.environ["KERAS_BACKEND"] = "tensorflow"

# Load the fine-tuned model
#model = keras.models.load_model("LoRA_Model_V2.keras")
model = from_pretrained_keras('DracolIA/GPT-2-LoRA-HealthCare')

translator = Translator() # Create Translator Instance

# Function to generate responses from the model
def generate_responses(question):
    language = translator.detect(question).lang.upper() # Verify the language of the prompt
    if language != "EN":
        question = translator.translate(question, src=language, dest="en").text # Translation of user text to english for the model
        
    prompt = f"[QUESTION] {question} [ANSWER]"
    # Generate the answer from the model and then clean and extract the real model's response from the prompt engineered string
    output = clean_answer_text(model.generate(prompt, max_length=1024))
    
    # Generate the answer from the model and then clean and extract the real model's response from the prompt engineered string
    if language != "EN":
        output = Translator().translate(output, src="en", dest=language).text # Translation of model's text to user's language
    
    return output

# Function clean the output of the model from the prompt engineering done in the "generate_responses" function
def clean_answer_text(text: str) -> str:
    # Define the start marker for the model's response
    response_start = text.find("[ANSWER]") + len("[ANSWER]")

    # Extract everything after "Doctor:"
    response_text = text[response_start:].strip()
    last_dot_index = response_text.rfind(".")
    if last_dot_index != -1:
      response_text = response_text[:last_dot_index + 1]

    # Additional cleaning if necessary (e.g., removing leading/trailing spaces or new lines)
    response_text = response_text.strip()

    return response_text
    

# Define a Gradio interface
def chat_interface(question, history_df):
    response = generate_responses(question)
    # Insert the new question and response at the beginning of the DataFrame
    history_df = pd.concat([pd.DataFrame({"Question": [question], "Réponse": [response]}), history_df], ignore_index=True)
    return response, history_df

with gr.Blocks() as demo:
    gr.HTML("""
        <div style='width: 100%; height: 200px; background: url("https://github.com/BastienHot/SAE-GPT2/raw/70fb88500a2cc168d71e8ed635fc54492beb6241/image/logo.png") no-repeat center center; background-size: contain;'>
            <h1 style='text-align:center; width=100%'>DracolIA - AI Question Answering for Healthcare</h1>
        </div>
    """)
    with gr.Row():
        question = gr.Textbox(label="Votre Question", placeholder="Saisissez ici...")
        submit_btn = gr.Button("Envoyer")
    response = gr.Textbox(label="Réponse", interactive=False)
    
    # Initialize an empty DataFrame to keep track of question-answer history
    history_display = gr.Dataframe(headers=["Question", "Réponse"], values=[], interactive=False)

    submit_btn.click(fn=chat_interface, inputs=[question, history_display], outputs=[response, history_display])

if __name__ == "__main__":
    demo.launch()

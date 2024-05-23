from dotenv import load_dotenv
load_dotenv()
import streamlit as st
import os
import google.generativeai as genai
from PIL import Image
from fpdf import FPDF
import time
from utils.emailUtil import send_email
from utils.savePDF import CreatePDF

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
def get_model_response(input_prompt, query, user_image):
    model = genai.GenerativeModel('gemini-pro-vision')
    if query != "":
        model_response = model.generate_content([input_prompt, query, user_image])
    else:
        model_response = model.generate_content(input_prompt, user_image)
    return model_response.text

st.set_page_config(page_title="Quote generation")
st.header("Sales playbook - Quote Generation")


user_input=st.text_input("Description for quote details",key="user_input")
uploaded_file = st.file_uploader("Upload quote sample ...", type=["jpg", "jpeg", "png"])
email_input=st.text_input("Email the quote to :",key="email_input")

image=""
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)

input_prompt="""
You are an expert in understanding sales quote templates. Based on the sample template given, generate template based on the input prompt given for the customer
"""

submit=st.button("Generate quote !!")
if submit:
    model_response=get_model_response(input_prompt, user_input, image)
    st.write(model_response)
    c = CreatePDF("Arial", 12)
    c.add_heading("Sales quote")
    c.add_text(model_response)
    c.save_pdf("Quote.pdf")
    st.toast('Your quote is generated !', icon='🎉')
    if '@' in email_input: 
        send_email(email_input, 'You got a quote', 'Hey , checkout this quote !!', 'Quote.pdf') 
 

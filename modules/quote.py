from dotenv import load_dotenv
load_dotenv()
import streamlit as st 
import os
import google.generativeai as genai 
from PIL import Image
from fpdf import FPDF
import time

class CreatePDF():
    def __init__(self, font, size) -> None:
        self.pdf = FPDF()
        self.pdf.add_page()
        self.pdf.set_font(font, size = size)
    
    def add_heading(self, text, align_center = True):
        if align_center:
            self.pdf.cell(200, 10, txt = text, ln = True,  align = 'C')
        else:
            self.pdf.cell(200, 10, txt = text, ln = True)
    
    def add_text(self, text, align_center = False):
        if align_center:
            self.pdf.multi_cell(0, 10, text, align = 'C')
        else:
            self.pdf.multi_cell(0, 10, text)

    def save_pdf(self, file_name):
        self.pdf.output(file_name)

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

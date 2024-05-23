from dotenv import load_dotenv
load_dotenv() 
import streamlit as st
import os
from PIL import Image
import google.generativeai as genai
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

## Load Gemini pro vision model
model=genai.GenerativeModel('gemini-pro')

sample_document = """
1. Company Information:

Your company name and logo
Contact information (phone number, email address)
Date of the quote

2. Customer Information:

Customer name and contact information
Reference number or project name (if applicable)
3. Hardware Details:

Itemized list of hardware: Include a clear description of each hardware component, including model numbers, brand names, and any relevant specifications (e.g., processor speed, RAM size, storage capacity).
Quantities: Specify the number of units for each listed hardware item.
Descriptions: Provide concise descriptions that highlight the key features and benefits of each piece of hardware, making it easy for the customer to understand the value proposition.

4. Pricing:

Unit Price: List the price per unit for each hardware item.
Total Price: Clearly display the total cost for each hardware item (unit price multiplied by quantity).
Subtotals: Consider including subtotals for specific categories of hardware (e.g., computers, peripherals, software licenses) if applicable.
Grand Total: Prominently display the total cost of all hardware, including any taxes or additional fees.

5. Additional Information (Optional):

Payment Terms: Outline the payment terms, including due date, accepted payment methods, and any potential discounts for early payment.
Delivery Information: Specify the estimated delivery timeframe and any associated shipping costs.
Warranty Information: Summarize the warranty coverage for the hardware, including duration and types of repairs or replacements covered.
Return Policy: Outline the return policy, including the timeframe for returns, restocking fees (if applicable), and the return process.
Notes or Special Conditions: Include any additional notes or special conditions relevant to the quote, such as minimum order quantities or bulk discounts.
"""

def get_gemini_response(input,image,user_prompt):
    response=model.generate_content([input,image,user_prompt])
    return response.text


##initialize our streamlit app

st.set_page_config(page_title="Understanding languages")
input=st.text_input("Input Prompt: ",key="input")

submit=st.button("Submit")

input_prompt="""
You are an expert in understanding templates. Based on the sample template given, generate content accordingly
"""

if submit:
    # image_data=input_image_details(uploaded_file)
    response=get_gemini_response(input_prompt,sample_document,input)
    st.subheader("Response : ")
    st.write(response)


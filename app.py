from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import google.generativeai as genai
from langchain.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
from flask import Flask, request, jsonify, render_template
import pandas as pd
import seaborn as sns
import openai
from flask_cors import CORS
from langchain_experimental.agents import create_pandas_dataframe_agent
from langchain.llms import OpenAI
app = Flask(__name__)
cors = CORS(app)

load_dotenv()
os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
openai.api_key=os.environ['OPENAI_API_KEY']

def get_pdf_text(pdf_docs):
    text=""
    for pdf in pdf_docs:
        pdf_reader= PdfReader(pdf)
        for page in pdf_reader.pages:
            text+= page.extract_text()
    return  text

def get_text_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=1000) 
    chunks = text_splitter.split_text(text)
    return chunks

def get_vector_store(text_chunks):
    embeddings = GoogleGenerativeAIEmbeddings(model = "models/embedding-001")
    vector_store = FAISS.from_texts(text_chunks, embedding=embeddings)
    vector_store.save_local("faiss_index")

def get_conversational_chain():

    prompt_template = """
    Answer the question as detailed as possible from the provided context, make sure to provide all the details, if the answer is not in
    provided context, give something relevant, don't provide the wrong answer\n\n
    Context:\n {context}?\n
    Question: \n{question}\n

    Answer:
    """
    model = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.3)
    prompt = PromptTemplate(template = prompt_template, input_variables = ["context", "question"])
    chain = load_qa_chain(model, chain_type="stuff", prompt=prompt)
    return chain

def user_input(user_question):
    embeddings = GoogleGenerativeAIEmbeddings(model = "models/embedding-001") 
    new_db = FAISS.load_local("faiss_index", embeddings)
    docs = new_db.similarity_search(user_question)
    chain = get_conversational_chain()
    response = chain(
        {"input_documents":docs, "question": user_question}
        , return_only_outputs=True)
    return (response["output_text"])


@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")

@app.route("/chat", methods=["GET", "POST"])
def chat():
    return render_template('chat.html')

@app.route("/quote", methods=["GET", "POST"])
def quote():
    return render_template('quoute.html')

@app.route("/analytics", methods=["GET", "POST"])
def analytics():
    return render_template('analytics.html')

@app.route("/holder", methods=["GET", "POST"])
def holder():
    return render_template('playbook.html')

@app.route('/ask-sales-queries', methods=['POST'])
def ask_sales_questions():
    try:
        data = request.get_json()
        user_question = data['query']
        sales_df = pd.read_excel('src_data/Bundled Deals Examples.xlsx')
        agent = create_pandas_dataframe_agent(OpenAI(temperature=0), 
                                            sales_df, 
                                            verbose=True)
        openai = OpenAI(temperature=0.0)
        response = agent(user_question)['output']
        return jsonify({'response': response})
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == "__main__":
    app.run(port=5000)
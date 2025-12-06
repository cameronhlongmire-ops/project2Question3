import streamlit as st
#from langchain_ollama import ChatOllama  
#import PyPDF2
import docx 
from bs4 import BeautifulSoup
#llm = ChatOllama(model="llama3.2:latest") 
import pdfplumber
from openai import OpenAI

client = OpenAI(api_key="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")

def extract_text(document): 
    upload = document.name.lower()
 
    if upload.endswith("txt"):
        return document.read().decode("utf-8", errors="ignore")
    
    elif upload.endswith("html"):
        soup = BeautifulSoup(document.read().decode("utf-8", errors="ignore"), "html.parser")
        return soup.get_text(separator="\n")
    elif upload.endswith("docx"): 
        doc = docx.Document(document)
        return "\n".join(p.text for p in doc.paragraphs)
    
    elif upload.endswith("pdf"): 
        with pdfplumber.open(document) as pdf:
            pages = [page.extract_text() or "" for page in pdf.pages]
        return "\n".join(pages)
        #for page in readerpages: 
            #pages_text.append(page.extract_text() 
    else: 
        return ""
     
st.title("Omnipotent Closed Source LLM")
st.write("Ask a question, upload a reference for the question.")

question = st.text_input("Question:")

uploaded_file = st.file_uploader( 
    "Add document here",
    type=["txt", "pdf", "docx", "html"])
if st.button("Get Answer"):
    documentupload = extract_text(uploaded_file) if uploaded_file else ""
    if documentupload:
        llm_question = f"""
Please use the uploaded article to answer this question.

+++question+++
{question}

+++uploaded article+++
{documentupload}
"""
    else: 
        llm_question = question  
    with st.spinner("Uno momento porfavore"): 
        response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "user", "content": llm_question}
                    ]
                )
        answer = response.choices[0].message.content
        st.write( answer) 

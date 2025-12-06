import streamlit as st
from langchain_ollama import ChatOllama  
import PyPDF2
import docx 
from bs4 import BeautifulSoup
llm = ChatOllama(model="llama3.2:latest") 
import pdfplumber


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
     
st.title("Omnipotent Ollama")
st.write("Ask a question, upload a reference for the question.")

question = st.text_input("Question:")

uploaded_file = st.file_uploader( 
    "Add document here",
    type=["txt", "pdf", "docx", "html"])
if st.button("Get Answer"):
    documentupload = extract_text(uploaded_file) if uploaded_file else ""
    if documentupload:
        llmquestion = f"""
Please use the uploaded article to answer this question.

+++question+++
{question}

+++uploaded article+++
{documentupload}
"""
    else: 
        llmquestion = question  
    with st.spinner("Uno momento porfavore"): 
        answer = llm.invoke(llmquestion).content
        st.write( answer) 

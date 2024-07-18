import streamlit as st

from src.llm import llm
from src.readpdf import readpdf
from src.astradb import astradb
from src.granularsegregation import segregation

st.title("Enhance your scientific writing with domain-specific LLM")
# st.text("- powered by Gemini pro, last updated on 2024-06-11")
st.text("- Made by Yifei, last updated on 2024-07-17")
st.text("Rephrase your draft or answer technical questions in the field of granular segregation. \n Support for other fields will be available later.")

# llm = llm(model="gemini-1.5-pro",temperature=0.5)
llm = llm(temperature=0.5)

# VectorStore selection
VectorStore = ["Granular Segregation"]  # You can dynamically load folder names if needed
selected_VectorStore = st.selectbox("Select a Topic", VectorStore)

if selected_VectorStore == "Granular Segregation":
    reply=segregation(llm)

# Generate content
context=st.text_area("Paste the text here",help="Please paste the text here")

submit = st.button("Generate results")


if submit:
    response=reply(context)
    st.header("Results:")
    st.write(response)


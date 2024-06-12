import streamlit as st

from src.llm import llm


st.title("Enhance your scientific writing with LLM")
st.text("powered by Gemini pro, last updated on 2024-06-11")

st.text("Rephrase your draft or answer technical questions based on thousands of papers in your field")

context=st.text_area("Paste the text here",help="Please paste the text here")
# uploaded_file=st.file_uploader("Upload Your Resume",type="pdf",help="Please uplaod the pdf")


submit = st.button("Generate results")




llm = llm(model="gemini-1.5-pro",temperature=0.5)
reply = llm.get_llm_response()


if submit:


    response=reply(context)
    st.header("Results:")
    st.write(response)


import streamlit as st

from src.llm import llm
from src.readpdf import readpdf


st.title("Enhance your scientific writing with domain-specific LLM")
# st.text("- powered by Gemini pro, last updated on 2024-06-11")
st.text("- Made by Yifei, last updated on 2024-07-17")
st.text("Rephrase your draft or answer technical questions in the field of granular segregation. \n Support for other fields will be available later.")


# VectorStore selection
VectorStore = ["Granular Segregation - Base", "Granular Segregation - Custimized"]  # You can dynamically load folder names if needed
selected_VectorStore = st.selectbox("Select a VectorStore", VectorStore)

# Upload pdf
uploaded_file = st.file_uploader("Upload more papers (optional)", type="pdf",accept_multiple_files=True, help="Please upload the pdf")
# Conditionally enable or disable the file uploader
if selected_VectorStore == "Granular Segregation - Base":
    st.info("PDF upload is disregarded for 'Granular Segregation - Base'.")
    uploaded_file = None
    llm = llm(model="gemini-1.5-pro",temperature=0.5,vecstore="segregation_base")

else:
    if uploaded_file:
        st.write("PDF uploaded successfully")
        obj=readpdf()
        obj.update_vectorstore(old_vec="segregation_base",new_vec="segregation_custimized",pdfs=uploaded_file)
        llm = llm(model="gemini-1.5-pro",temperature=0.5,vecstore="segregation_custimized")
    else:
        st.warning("You can upload some pdf files to update VectorStore")
        llm = llm(model="gemini-1.5-pro",temperature=0.5,vecstore="segregation_custimized")


reply = llm.get_llm_response()

# Generate content
context=st.text_area("Paste the text here",help="Please paste the text here")


submit = st.button("Generate results")





if submit:
    response=reply(context)
    st.header("Results:")
    st.write(response)


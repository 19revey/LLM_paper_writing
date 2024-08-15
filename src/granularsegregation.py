import streamlit as st

from src.llm import llm
from src.readpdf import readpdf
from src.astradb import astradb

def segregation(llm):

    customize = st.checkbox("Customize the Database")

    # Conditionally enable or disable the file uploader
    if not customize:
        # st.info("PDF upload is disregarded for 'Granular Segregation - Base'.")
        uploaded_file = None
        reply = llm.get_llm_response()

    else:
        try:
            # load remote database
            db=astradb(embedding=llm.embedding)

            # Password input
            password = st.text_input("Enter password:", type="password")
            if password:
                if password == "northwestern":
                    st.success("Password is correct!")
                    st.warning("Enabling a customized database slows down performance because it requires connecting to a remote storage instead of loading a local one!")
                    st.warning("The updated database is persistent and can be used in future sessions. Please avoid uploading duplicate PDF files!")

                    # Upload pdf
                    uploaded_file = st.file_uploader("Upload more papers (optional)", type="pdf",accept_multiple_files=True, help="Please upload the pdf")
                    
                    if uploaded_file:
                        st.write("PDF uploaded successfully")
                        emb = st.button("Embedding the documents")
                        # obj=readpdf()
                        # obj.update_vectorstore(old_vec="segregation_base",new_vec="segregation_custimized",pdfs=uploaded_file)
                        if emb:
                            db.update_vectorstore(pdfs=uploaded_file)
                            uploaded_file=None
                    else:
                        st.warning("You can upload some pdf files to update VectorStore")

                else:
                    st.error("Incorrect password. Please try again.")
            else:
                st.info("Please enter the password to customize the database.")
            
            reply=llm.get_llm_response(vecstore=db.store)
    
        except Exception as e:
            print(e)
            st.info(f"{e}")
            reply = llm.get_llm_response()


    return reply

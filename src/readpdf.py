from langchain.text_splitter import CharacterTextSplitter
import glob
from pypdf import PdfReader
import os
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv

from src.utils.logger import logging
from src.utils.exception import CustomException
import sys
import hashlib

import argparse

import warnings
warnings.filterwarnings("ignore")



class readpdf:
    def __init__(self, embedding=None, chuck_size=2000, chuck_overlap=500,path="pdfs") :


        self.pdf_docs=glob.glob(f"{path}/*.pdf")
        self.text = ""
        self.chuck_size = chuck_size
        self.chuck_overlap = chuck_overlap

        if not embedding:
            try:
                load_dotenv()
                logging.info("embedding not specified, looking for default gemini embedding")
                GOOGLE_API_KEY= os.getenv("GOOGLE_API_KEY")
                self.embedding = GoogleGenerativeAIEmbeddings(model = "models/embedding-001",api_key=GOOGLE_API_KEY)
                logging.info("successfully loaded gemini embedding")
            except Exception as e:
                raise CustomException(e,sys)
                
        else:
            self.embedding = embedding
            logging.info("embedding specified")

    def get_pdf_text(self,pdf_docs=None):
        text = ""
        try:
            for pdf in pdf_docs:
                pdf_reader = PdfReader(pdf)
                for page in pdf_reader.pages:
                    content = page.extract_text()
                    if content:
                        text += content
        except Exception as e:
            logging.error(f"Error extracting text from PDF: {e}")
        
        return text

    def get_text_chunks(self,pdfs=None):
        if pdfs is None:
            pdfs = self.pdf_docs
        self.text = self.get_pdf_text(pdfs)
        logging.info("Text extracted from pdfs")

        text_splitter = CharacterTextSplitter(
            separator="\n",
            chunk_size=self.chuck_size,
            chunk_overlap=self.chuck_overlap,
            length_function=len
        )
        chunks = text_splitter.split_text(self.text)
        logging.info("Text split into chunks")
        return chunks
    

    def create_vectorstore(self,name="faiss_index",pdfs=None):
        
        chunks=self.get_text_chunks(pdfs)
        vectorstore = FAISS.from_texts(texts=chunks, embedding=self.embedding)
        vectorstore.save_local(name)
        logging.info("Vectorstore created")

    
    
    def update_vectorstore(self,old_vec="segregation_base",new_vec="segregation_new",pdfs=None):
        chunks = self.get_text_chunks(pdfs)
        logging.info("Text chunks retrieved for update")
        
        try:
            vectorstore = FAISS.from_texts(texts=chunks, embedding=self.embedding)
            logging.info(f"New vectorstore {new_vec} created")
            
            old_vecstore = FAISS.load_local(old_vec, self.embedding, allow_dangerous_deserialization=True)
            logging.info(f"Old vectorstore {old_vec} loaded")
            
            vectorstore.merge_from(old_vecstore)
            vectorstore.save_local(new_vec)
            logging.info(f"Vectorstore {old_vec} updated to {new_vec}")
        
        except Exception as e:
            logging.error(f"Error updating vectorstore: {e}")




if __name__ == "__main__":


    parser = argparse.ArgumentParser()
    parser.add_argument("--path", type=str, required=True,help="path to pdf files")
    parser.add_argument("--name", type=str, required=True,help="vector store name")
    args = parser.parse_args()
    file_path=glob.glob(f"{args.path}/*.pdf") 
    
    vec_name=args.name

    try:
        obj=readpdf(path=file_path)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    if os.path.exists(vec_name):
        print("update vec store")
        obj.update_vectorstore(old_vec="vec_name",new_vec="vec_name",pdfs=file_path)
    else:
        print("create new vec store")
        obj.create_vectorstore(name=vec_name,pdfs=file_path)



  


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

import warnings
warnings.filterwarnings("ignore")



class readpdf:
    def __init__(self, embedding=None, chuck_size=2000, chuck_overlap=500) :
        # pdfs="*pdf"
        # combined_path=os.path.join(path,pdfs)
        self.pdf_docs=glob.glob("pdfs/*.pdf")
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
        text=""
        for pdf in pdf_docs:
            
            pdf_reader = PdfReader(pdf)
            for page in pdf_reader.pages:
                content=page.extract_text() 
                if content:
                    text += content 
        return text

    def get_text_chunks(self):
        self.text = self.get_pdf_text(self.pdf_docs)
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
    

    def create_vectorstore(self):
        chunks=self.get_text_chunks()
        vectorstore = FAISS.from_texts(texts=chunks, embedding=self.embedding)
        vectorstore.save_local("faiss_index")
        print("Vectorstore created")
        return vectorstore

if __name__ == "__main__":
    path = "pdfs"
    obj=readpdf()
    obj.create_vectorstore()
  

import os

from dotenv import load_dotenv
import cassio
from langchain.vectorstores.cassandra import Cassandra
from pypdf import PdfReader
from langchain.text_splitter import CharacterTextSplitter

class astradb:

    def __init__(self,embedding) -> None:
        load_dotenv()
        ASTRA_DB_ID=os.getenv("ASTRA_DB_ID")
        ASTRA_DB_APPLICATION_TOKEN=os.getenv("ASTRA_DB_APPLICATION_TOKEN")
        cassio.init(token=ASTRA_DB_APPLICATION_TOKEN,database_id=ASTRA_DB_ID)
        self.store =Cassandra(
            embedding=embedding,
            table_name="demo",
            session=None,
            keyspace=None,
        )
    
    def update_vectorstore(self,pdfs):
        chunks = self.get_text_chunks(pdfs)
        self.store.add_texts(chunks)
        print("VectorStore updated successfully")
        

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
            print(f"An unexpected error occurred: {e}")
        
        return text

    def get_text_chunks(self,pdfs=None):
        if pdfs is None:
            pdfs = self.pdf_docs
        self.text = self.get_pdf_text(pdfs)

        text_splitter = CharacterTextSplitter(
            separator="\n",
            chunk_size=2000,
            chunk_overlap=500,
            length_function=len
        )
        chunks = text_splitter.split_text(self.text)
        return chunks
    
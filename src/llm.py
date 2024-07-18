
# import google.generativeai as genai
from langchain_google_genai import GoogleGenerativeAI,GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
import os

from dotenv import load_dotenv

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableParallel, RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

import cassio
from langchain.vectorstores.cassandra import Cassandra



class llm:
    def __init__(self, model=None,temperature=0.0):
        if not model:
            model = "gemini-pro"
        
        load_dotenv()
        # ASTRA_DB_ID=os.getenv("ASTRA_DB_ID")
        # ASTRA_DB_APPLICATION_TOKEN=os.getenv("ASTRA_DB_APPLICATION_TOKEN")

        # ASTRA_DB_APPLICATION_TOKEN = "AstraCS:ZjAlBBhppaDpnwwytTluLfWu:b9c64128087ecbce6fd41221da84f2f966640fe2621d7b0824435bc31a1fe454"
        # ASTRA_DB_ID="73a41af9-ca46-4f34-b58c-49442121ba07"

        GOOGLE_API_KEY= os.getenv("GOOGLE_API_KEY")
        self.llm = GoogleGenerativeAI(model=model, temperature=temperature,api_key=GOOGLE_API_KEY)
        self.embedding = GoogleGenerativeAIEmbeddings(model = "models/embedding-001",api_key=GOOGLE_API_KEY)

        
        self.prompt_template = """
            You are a researcher who knows how to write scientific papers on topics related to STEM. 
            I will share related texts from previous documents with you, and you will rewrite the provided texts in an academic language.

            Below is the text I want to rewrite:
            {question}

            Here is a list of previous documents:
            {context}

            1. The generated texts should be very similar in style to the documents, 
            in terms of tone of voice, logical arguments, and other details.

            2. If the past texts contain no information related to {context}, then try to mimic the style of the documents to rewrite the paragraph.

            Please rewrite the paragraph without numbered citations or references:
        """
        
    def get_llm_response(self,vecstore=None):


        if vecstore is None:
            local_db = FAISS.load_local("segregation_base", self.embedding, allow_dangerous_deserialization=True)
            retriever = local_db.as_retriever(search_kwargs={'lambda_mult': 0.5, 'fetch_k': 20})
        else:
            retriever = vecstore.as_retriever()

        prompt=ChatPromptTemplate.from_template(self.prompt_template)

        # retriever = new_db.similarity_search(query_text, k=5)
        
        # Define the output parser
        output_parser = StrOutputParser()
        chain = (
                {"context": retriever, "question": RunnablePassthrough()}
                | prompt
                | self.llm
                | StrOutputParser()
            )
        # response=chain.invoke(question)
        return chain.invoke


if __name__ == "__main__":

    load_dotenv()
    ASTRA_DB_ID=os.getenv("ASTRA_DB_ID")
    ASTRA_DB_APPLICATION_TOKEN=os.getenv("ASTRA_DB_APPLICATION_TOKEN")
    GOOGLE_API_KEY= os.getenv("GOOGLE_API_KEY")
    embedding = GoogleGenerativeAIEmbeddings(model = "models/embedding-001",api_key=GOOGLE_API_KEY)
    cassio.init(token=ASTRA_DB_APPLICATION_TOKEN,database_id=ASTRA_DB_ID)
    store =Cassandra(
        embedding=embedding,
        table_name="demo",
        session=None,
        keyspace=None,
    )


    llm = llm()
    reply = llm.get_llm_response(vecstore=store)
    question = "What is granular segregation?"
    print(reply(question))
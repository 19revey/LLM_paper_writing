
# import google.generativeai as genai
from langchain_google_genai import GoogleGenerativeAI,GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
import os

from dotenv import load_dotenv

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableParallel, RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser



class llm:
    def __init__(self, model=None):
        if not model:
            model = "gemini-pro"
            load_dotenv()
            GOOGLE_API_KEY= os.getenv("GOOGLE_API_KEY")
            self.llm = GoogleGenerativeAI(model=model, temperature=0.0,api_key=GOOGLE_API_KEY)
            self.embedding = GoogleGenerativeAIEmbeddings(model = "models/embedding-001",api_key=GOOGLE_API_KEY)

        else:
            raise TypeError("Model not found")  
        
        self.prompt_template = """
            You are a researcher know how to write scientific paper on topics related to STEM. 
            I will share related texts from previous documents with you and you will rewrite the provided texts in an academic language.

            Below is the texts I want to rewrite:
            {question}

            Here is a list of previous documents:
            {context}

            1/ the generated texts should be very similar to the style of the documents, 
            in terms of ton of voice, logical arguments and other details

            2/ If the past texts contain no inform related to {context}, then try to mimic the style of the documents to rewrite the paragraph


            Please rewrite the paragraph and show the source document in the format of author and year.: 
                    """
        
    def get_llm_response(self):

        prompt=ChatPromptTemplate.from_template(self.prompt_template)

        new_db = FAISS.load_local("faiss_index", self.embedding, allow_dangerous_deserialization=True)

        # retriever = new_db.similarity_search(query_text, k=5)
        retriever = new_db.as_retriever()


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
    llm = llm()
    reply = llm.get_llm_response()
    question = "What is the impact of climate change on the environment?"
    print(reply(question))
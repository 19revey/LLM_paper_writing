
# import google.generativeai as genai
from langchain_google_genai import GoogleGenerativeAI,GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
import os

from dotenv import load_dotenv

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableParallel, RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser



class llm:
    def __init__(self, model=None,temperature=0.0,vecstore="segregation_base"):
        if not model:
            model = "gemini-pro"
        
        load_dotenv()
        GOOGLE_API_KEY= os.getenv("GOOGLE_API_KEY")
        self.llm = GoogleGenerativeAI(model=model, temperature=temperature,api_key=GOOGLE_API_KEY)
        self.embedding = GoogleGenerativeAIEmbeddings(model = "models/embedding-001",api_key=GOOGLE_API_KEY)
        self.new_db = FAISS.load_local(vecstore, self.embedding, allow_dangerous_deserialization=True)
        
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

            Please rewrite the paragraph and show the source document in the format of author and year:
        """
        
    def get_llm_response(self):

        prompt=ChatPromptTemplate.from_template(self.prompt_template)

        # retriever = new_db.similarity_search(query_text, k=5)
        retriever = self.new_db.as_retriever()
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
    question = "What is granular segregation?"
    print(reply(question))
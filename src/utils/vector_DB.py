from openai import AzureOpenAI
import os
from dotenv import load_dotenv

load_dotenv()

from pinecone import Pinecone

class VectorDB:
    def __init__(self):
        self.vectorDB = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
        self.index = self.vectorDB.Index(os.getenv("PINECONE_INDEX"))
        self.client = AzureOpenAI(
            api_key=os.getenv("AZURE_OPENAI_KEY"), 
            api_version=os.getenv("AZURE_OPENAI_API_VERSION"),  
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
        )

    def embed(self, texts):
        embeddings = [response["embedding"] for response in self.client.embeddings.create(
            model=os.getenv("AZURE_OPENAI_DEPLOYMENT_ADA"), 
            input=texts
        )["data"]]
        return embeddings

    def add_vector(self, vectors):
        self.index.upsert(
            vectors=vectors
        )

    def add(self, texts):
        embeddings = self.embed(texts)
        self.add_vector(embeddings)
    
    def search(self, query, top_k=5):
        query_vector = self.embed(query)
        result = self.index.query(
            vector=query_vector, 
            top_k=top_k, 
            include_metadata=True, 
            include_values=True
        )
        return result

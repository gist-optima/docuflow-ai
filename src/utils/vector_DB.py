# %%
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
        response = self.client.embeddings.create(
            model=os.getenv("AZURE_OPENAI_DEPLOYMENT_ADA"), 
            input=texts
        )
        embeddings = [embedding_data["embedding"] for embedding_data in response.model_dump()["data"]]
        return embeddings

    def add(self, texts):
        vectors = self.embed(texts)
        self.index.upsert(
            vectors=[{"id": text, "values": vector} for text, vector in zip(texts, vectors)]
        )
    
    def search(self, query, top_k=5):
        query_vector = self.embed(query)
        result = self.index.query(
            vector=query_vector, 
            top_k=top_k, 
            include_metadata=True, 
            include_values=True
        )["matches"]
        return result

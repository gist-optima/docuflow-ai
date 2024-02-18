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
            input=list(texts.values())
        )
        embeddings = dict((id, embedding_data["embedding"]) for id, embedding_data in zip(texts.keys(), response.model_dump()["data"]))
        return embeddings

    def add(self, texts):
        vectors = self.embed(texts)
        self.index.upsert(
            vectors=[{"id": id, "values": vector} for id, vector in vectors.items()]
        )
    
    def search(self, query, top_k=5, threshold=0.95):
        query_vector = self.embed({"query": query})["query"]
        results = self.index.query(
            vector=query_vector, 
            top_k=top_k, 
            include_metadata=False, 
            include_values=False
        )["matches"]
        results = filter(lambda result: result["score"] > threshold, results)
        return [result["id"] for result in results]

# %%
from openai import AzureOpenAI
import os
from dotenv import load_dotenv

load_dotenv()

class Embed:
    def __init__(self):
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
    
# %%
Embeder = Embed()
Embeder.embed("Hello")

# %% splitter
search_results_splits=[]

for doc_text in doc_texts:
  splits=doc_text.split('다.')
  results=[]
  cur_len=0
  start=0
  for i in range(len(splits)):
    cur_len+=len(splits[i])
    if cur_len>200:
        if start!=i:
          result="다.".join(splits[j] for j in range(start, i))+"다."
          results.append(result)
        start=i
    if i==len(splits)-1:
        result="다.".join(splits[j] for j in range(start, i))
        if result!="":
          results.append(result)
  search_results_splits.append(results)

# %% embedding and store in DB
from pinecone import Pinecone

pc=Pinecone(api_key="566b0c6b-52c7-4468-8cd7-a17c9c6f6560")
index=pc.Index('optima')

# %%
from openai import AzureOpenAI
from dotenv import load_dotenv

load_dotenv()
gpt=AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_KEY"), 
    api_version="2023-07-01-preview", 
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
)

# %%
def embed(input):
  embed=gpt.embeddings.create(
    input=input,
    model=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME_EMBEDDING")
  )
  return embed

print(embed([search_results_splits[0]]))

# %% tmp: origin → search_results_splits, vec → OpenAI embed
import datetime as dt
import pytz
import random

def embed_post(texts):
   pass

KST=pytz.timezone("Asia/Seoul")
random_vec=[]
for _ in range(1536):
   random_vec.append(random.randrange(10**3, 10**4))

names=["Inseon", "Jumyeong", "Ikjun", "Siwon", "Dohyeon"]
verbs=["studies", "works on", "is enjoying", "focuses"]
nouns=["linear algebra", "programming", "English", "data engineering"]   

vec_id=str(random.randrange(10**6, 10**7))
query="Show the person working hardest"
query=list(query.split())
metadata={
   "created_at": str(dt.datetime.now().astimezone(KST)),
   "origin": names[random.randint(0, len(names)-1)]+" "+verbs[random.randint(0, len(verbs)-1)]+" "+nouns[random.randint(0, len(nouns)-1)],
   "query": "Show the person working hardest"
}
vec={
   "id": vec_id,
   "values": random_vec,
   "metadata": metadata,
}
index.upsert(vectors=[vec], namespace="-".join(query))

# %% reset index
# index.delete(delete_all=True, namespace="-".join(query))

# %% query for ref
query="Show the person working hardest"
query=list(query.split())

random_vec_query=[]
for _ in range(1536):
   random_vec_query.append((random.randrange(1000, 10000)))

query_result=index.query(
   vector=random_vec_query,
   top_k=3,
   namespace="-".join(query),
   include_metadata=True
   )

print(query_result)
# %%
for i in range(5):
   for j in range(len(search_results_splits[i])):
      embed(search_results_splits[i][j]) 
      #table append

# %% make prompt using query result
refers=[]
top_k=3
for i in range(top_k):
  refers.append(query_result["matches"][i]["metadata"]["origin"])

doc_title=""
prev_content=""
nxt_content=""
for i in range(top_k):
  prompt=f"""
  보고서의 제목: {doc_title}
  사용자의 guiding vector: {" ".join(query)}
  답변 참고자료: {refers[i]}
  보고서의 전후 맥락: {prev_content} <GPT_ANSWER/> {nxt_content}
  위의 정보를 바탕으로, GPT_ANSWER을 작성해줘. JSON 형식으로 답변해줘.
  """

ex_QA={}

# %% ask GPT

# %% format the output

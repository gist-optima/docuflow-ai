# %% search result define
search_results=[{'title': '[아이디어톤] 주제 선정 및 제출 (1)',
  'link': 'https://velog.io/@heokyeongju/%EC%95%84%EC%9D%B4%EB%94%94%EC%96%B4%ED%86%A4-%EC%A3%BC%EC%A0%9C-%EC%84%A0%EC%A0%95-1',
  'snippet': '2022. 8. 6. ... ... 사자처럼 BE 1기의 아이디어톤이 끝나고 해커톤으로 이어 진행되고 있다 ... 이에 따라 각각의 교육 방식이 적절한 방식으로 발전해왔다고 생각했다.'},
 {'title': '제2회 계명 아이디어톤 대회 세부 계획 안내',
  'link': 'https://lis.kmu.ac.kr/bbs/pakmu/2701/66360/download.do',
  'snippet': '2021. 1. 14. ... 아이디어 최종안 제출 방법. 가. 본선 참가팀으로 선발된 8개 내외의 팀은 ... 위한 회의 등을 진행하며, 전문 역량 제고와 원활한 회의 진행을 위한 각종\xa0...'},
 {'title': '시스코 플랫폼으로 만드는 지속 가능한 미래 Cisco Innovation ...',
  'link': 'https://www.cisco.com/c/m/ko_kr/innovation-challenge.html',
  'snippet': '우리는 더 스마트하게 일하고, 지속 가능한 방식으로 일하고, 책임감을 갖고, 변화에 ... 아이디어로 팀을 구성하여 해커톤 진행; 해커톤 우승팀 발표 : 4월 30일(화)\xa0...'},
 {'title': 'https://ibus.hanyang.ac.kr/front/community/notice/...',
  'link': 'https://ibus.hanyang.ac.kr/front/community/notice/file-load?id=3204&fileId=4840',
  'snippet': '진행방식 : 오프라인 (대면형) 워크숍 진행; 대상 : ESG 아이디어톤 참가자 50명 ... ② 아이디어톤 진행 ③ 최종발표 및 시상. ※ 참가신청 링크. https://mobisthon.com.'},
 {'title': '2023 현대모비스 ESG 아이디어톤 공고문',
  'link': 'https://www.uos.ac.kr/common/board-download.do?listId=20049D144&seq=283&fSeq=1',
  'snippet': '2023. 6. 9. ... 1. 사전워크숍 진행 일시 : 2023년 7월 14일 (금) 10:00~14:30. 2. 진행방식 : 오프라인 (대면형) 워크숍 진행. 3. 대상 : ESG 아이디어톤 참가자 60명. *\xa0...'}]

# %% file download
from urllib.request import urlretrieve
import string
import random
import os
import ssl

# %%
def download_file(url='https://ibus.hanyang.ac.kr/front/community/notice/file-load?id=3204&fileId=4840'
):
  letters=string.ascii_letters
  random_string=random.sample(letters, 10)
  path=os.path.abspath(os.getcwd()) + "/downloads/" + "".join(random_string)
  ssl._create_default_https_context = ssl._create_unverified_context
  url_file=urlretrieve(url, path)
  return path

# %% scrape word file
import zipfile 
import xml.etree.ElementTree 
 
def scrape_docx(path):
  doc_text=[]
  WORD_NAMESPACE = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}' 
  PARA = WORD_NAMESPACE + 'p' 
  TEXT = WORD_NAMESPACE + 't' 
  TABLE = WORD_NAMESPACE + 'tbl' 
  ROW = WORD_NAMESPACE + 'tr' 
  CELL = WORD_NAMESPACE + 'tc' 
  
  with zipfile.ZipFile(path) as docx: 
      tree = xml.etree.ElementTree.XML(docx.read('word/document.xml')) 
  
  for table in tree.iter(TABLE): 
      for row in table.iter(ROW): 
          for cell in row.iter(CELL): 
              doc_text.append(''.join(node.text for node in cell.iter(TEXT)))

  return "".join(doc_text)

# %% scrape pdf file
import fitz

def scrape_pdf(path):
  doc=fitz.open(path)
  doc_text=[]
  for page in doc:
      text=page.get_text()
      doc_text.append(text)
  return "".join(doc_text)

# %% scrape web
import requests
from requests.exceptions import HTTPError

def request_web(url):
  try:
    resp=requests.get(url)
    resp.raise_for_status()
    
  except HTTPError as Err:
    print("HTTP Error occurred")
  except Exception as Err:
    print("Unknown Error occurred")

  else:
    print('Success')
  return resp

# %%
from bs4 import BeautifulSoup

def scrape_web(url):
  doc_texts=[]
  resp=request_web(url)
  html=resp.content
  parse=BeautifulSoup(html, "html.parser")
  print(parse.title.string)

  tags=parse.find_all(["p", "h1", "h2", "h3"])
  for tag in tags:
    doc_text=tag.get_text().strip()
    doc_texts.append(doc_text)

  return "".join(doc_texts)

# %% scrap website, file
import magic

doc_texts=[]
for result in search_results:
    doc_text=""
    url=result["link"] 
    if ("file-load" in url) or ("download" in url):
        path=download_file(url)       
        mine_type=magic.Magic()
        file_signature=mine_type.from_file(path)
        print(file_signature)

        if "Microsoft Word" in file_signature:
           doc_text=scrape_docx(path)
        elif "PDF" in file_signature:
           doc_text=scrape_pdf(path)
    else:
       doc_text=scrape_web(url)
    doc_texts.append(doc_text)
  
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

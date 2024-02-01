# %% import modules & libraries
import magic

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
import urllib.request
import string
import random

def download_file(url='https://ibus.hanyang.ac.kr/front/community/notice/file-load?id=3204&fileId=4840'
):
  letters=string.ascii_letters
  random_string=random.sample(letters, 10)
  path='C:\\Users\\user\\AppData\\Local\\Temp\\'+"optima-"+"".join(random_string)
  url_file=urllib.request.urlretrieve(url, path)
  return path

# %% scrap word file
import zipfile 
import xml.etree.ElementTree 
 
def scrap_docx(path):
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

  return doc_text

# %% scrap pdf file
import fitz
def scrap_pdf(path):
  doc=fitz.open(path)
  doc_text=[]
  for page in doc:
      text=page.get_text()
      doc_text.append(text)
  return doc_text

# %% scrap website, file
for result in search_results:
    doc_texts=[]
    doc_text=""
    url=result["link"] 
    if ("file-load" in url) or ("download" in url):
        path=download_file(url)       
        mine_type=magic.Magic()
        file_signature=mine_type.from_file(path)
        print(file_signature)

        if "Microsoft Word" in file_signature:
           doc_text=scrap_docx(path)
        elif "PDF" in file_signature:
           doc_text=scrap_pdf(path)
        
        doc_texts.append(doc_text)
    else:
       #web scrap
       pass
  

# %% split

# %% embedding and store in DB

# %% query

# %% make prompt using query result

# %% ask GPT

# %% format the output

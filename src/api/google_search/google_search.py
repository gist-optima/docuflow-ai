import os
import sys
BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_PATH)

# get links
from langchain.tools import Tool
from langchain_community.utilities import GoogleSearchAPIWrapper

# download file from url
from urllib.request import urlretrieve
from uuid import uuid4
import ssl

# parse docx
from zipfile import ZipFile
from xml.etree.ElementTree import XML

# parse pdf
import fitz

# get and parse HTML from url
import requests
from bs4 import BeautifulSoup

# retrieve text from url
from magic import Magic

# multithreading
from threading import Thread

# flask rest api
from flask_restx import Resource, Namespace

namespace = Namespace("google-search")

@namespace.route("/<string:query>/<int:n>")
class GoogleSearch(Resource):
    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)
        self.search = GoogleSearchAPIWrapper()
        self.download_dir_path = os.path.join(os.path.dirname(os.path.abspath(__file__)) ,"downloads")

    def get(self, query, n=5):
        links = self.get_links(query, n)

        texts = dict((link, "") for link in links)
        def worker(link):
            text = self.retrieve_text_from_url(link)
            texts[link] = text
        threads = []
        for link in links:
            thread = Thread(target=worker, args=[link, ])
            threads.append(thread)
            thread.start()
        for thread in threads:
            thread.join()
        
        self.clear_downloaded_files()

        return texts
        
    def get_links(self, query, n):
        tool = Tool(
            name="Google Search",
            description="Search Google to retrieve useful information",
            func=lambda query: self.search.results(query, n)
        )

        results = tool.run(query)

        return [result["link"] for result in results]
    
    def download_file_from_url(self, url):
        path=os.path.join(self.download_dir_path, str(uuid4()))
        ssl._create_default_https_context = ssl._create_unverified_context
        urlretrieve(url, path)

        return path
    
    def clear_downloaded_files(self):
        file_paths = [os.path.join(self.download_dir_path, filename) for filename in os.listdir(self.download_dir_path)]
        threads = []
        for path in file_paths:
            thread = Thread(target=lambda path: os.remove(path), args=[path, ])
            threads.append(thread)
            thread.start()
        for thread in threads:
            thread.join()
    
    def parse_docx(self, path):
        doc_text = []
        WORD_NAMESPACE = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}' 
        PARA = WORD_NAMESPACE + 'p' # TODO: ???
        TEXT = WORD_NAMESPACE + 't' 
        TABLE = WORD_NAMESPACE + 'tbl' 
        ROW = WORD_NAMESPACE + 'tr' 
        CELL = WORD_NAMESPACE + 'tc' 

        with ZipFile(path) as docx: 
            tree = XML(docx.read('word/document.xml')) 
        
        for table in tree.iter(TABLE): 
            for row in table.iter(ROW): 
                for cell in row.iter(CELL): 
                    doc_text.append(''.join(node.text for node in cell.iter(TEXT)))

        return "".join(doc_text)
    
    def parse_pdf(self, path):
        doc=fitz.open(path)
        doc_text=[]

        for page in doc:
            text=page.get_text()
            doc_text.append(text)

        return "".join(doc_text)
    
    #TODO: parse hwp 
    
    def get_and_parse_HTML(self, url):
        doc_text=[]
    
        response = requests.get(url)
        response.raise_for_status()

        #TODO: Improve html parser
        html=response.content
        parse=BeautifulSoup(html, "html.parser")
        tags=parse.find_all(["p", "h1", "h2", "h3"])
        for tag in tags:
            text=tag.get_text().strip()
            doc_text.append(text)

        if len(doc_text) == 0:
            raise Exception("Empty?")
        
        return "".join(doc_text)
    
    def retrieve_text_from_url(self, url):
        doc_text = ""

        try:
            doc_text=self.get_and_parse_HTML(url)
        except:
            print(url)
            path = self.download_file_from_url(url)
            file_signature = Magic().from_file(path)
            if "Microsoft Word" in file_signature:
                doc_text = self.parse_docx(path)
            elif "PDF" in file_signature:
                doc_text = self.parse_pdf(path)
            else:
                doc_text = f"Unsopported file type: {file_signature}"

        return doc_text
# %%

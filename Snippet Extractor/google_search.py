# %%
import os
from langchain.tools import Tool
from langchain_community.utilities import GoogleSearchAPIWrapper

# %%
search = GoogleSearchAPIWrapper()

def search_top5(query):
    return search.results(query, 5)

tool = Tool(
    name="Google Search",
    description="Search Google for recent results to extract useful information and make snippets",
    func=search_top5,
)
# %%
tool.run("아이디어톤 진행 방식")
# %%

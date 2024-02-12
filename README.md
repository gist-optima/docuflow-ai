# docuflow-ai

## API

run api_server.py

### container_generator

title -> container로만 이루어진 글 초안의 배열

### query_regenerator

all contents: JSON형식의 현재 쓰고 있는 보고서 전체\
focused container: 현재 유저의 커서가 있는 snippet 또는 Container의 id\
guiding vector: 검색의 방향성\
previous query: 바로 전 검색어\
shown snippets: 바로 전에 사용자에게 보여줬던 snippet들의 배열\
preffered snippet: shown snippets 중에서 사용자가 선택한 snippet의 id\
-> 새롭게 추천된 query들의 배열

### google_search

query -> 검색 결과 글의 배열

### search_vector_DB

query -> 검색 결과 글의 id의 배열

### snippet_extractor

articles: snippet들을 추출하고자 하는 대상이 되는 글들의 배열\
all contents: 현재 작성하고 있는 보고서 전체의 JSON형식\
focused container: 현재 사용자의 커서가 있는 container나 snippet의 id
guiding vector: 검색의 방향성\
shown snippets: 바로 전에 사용자에게 보여줬던 snippet들의 배열\
preffered snippet: shown snippets 중에서 사용자가 선택한 snippet의 id\
-> 추출된 snippet객체들의 배열

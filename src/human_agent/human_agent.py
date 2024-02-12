# %% import
import requests

# %% make container
# title: ["docuflow가 속한 시장 분석 및 진입 전략", "docuflow의 고객 페르소나 및 시나리오 정의"]
title="docuflow이 속한 시장 분석 및 진입 전략"

response=requests.get("http://localhost:5000/container-generator/{title}")
if response.status_code==200:
    init_container=response.content

# %% generate initial query

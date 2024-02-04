# %% json 정의
json={
  "보고서": {
    "제목": "KPMG 아이디어톤 기안서 - 아이디어톤을 통한 신사업 및 인재 발굴",
    "내용": {
      "1. 배경": "KPMG는 지속적인 혁신과 인재 발굴을 위해 아이디어톤을 개최하고자 합니다.",
      "2. 아이디어톤 목적": [
        "신규 사업 아이디어 도출",
        "창의적이고 혁신적인 아이디어 발굴",
        "다양한 부서 간 협업 강화",
        "인재 발굴 및 역량 검증"
      ],
      "3. 일정 및 참가자": {
        "개최일": "YYYY년 MM월 DD일",
        "참가자": [
          {"부서": "기획팀", "인원": "5명", "담당자": "이름1"},
          {"부서": "개발팀", "인원": "4명", "담당자": "이름2"},
          {"부서": "마케팅팀", "인원": "3명", "담당자": "이름3"}
        ]
      },
      "4. 아이디어톤 진행 방식": [
        "아이스 브레이킹 세션을 통한 팀 구성",
        "주제 발표 및 아이디어 도출 시간",
        "멘토링 세션 및 피드백",
        "최종 발표 및 심사위원 평가"
      ],
      "5. 예상 성과": [
        "신규 사업 아이디어 도출로 기업의 경쟁력 강화",
        "참가자들 간의 네트워킹 증진",
        "우수한 참가자를 통한 인재 발굴"
      ],
      "6. 지원 및 협조 요청": [
        "기획팀은 참가 인원 및 일정 조정이 필요할 경우 해당 내용을 적극 협조해주시기 바랍니다.",
        "기존의 성공적인 아이디어톤 사례를 참고하여 진행 방식을 논의하고자 합니다."
      ],
      "7. 기대 효과": "KPMG 아이디어톤을 통해 다양한 아이디어와 역량 있는 인재를 발굴하고, 이를 토대로 기업의 혁신과 성장을 이끌어 나가기를 기대합니다."
    }
  }
}

# %% json analysis
print(type(json["보고서"])==dict)


# %% parse json
def get_children_id(json):
    ids=[]
    for key in json.keys():
        ids.append(key)
    return ids

def parse_json(arr, json):
    print(json)
    if type(json)==dict:
        for key, value in json.items():
            if type(value)==dict:
                arr.append(
                    {
                        "type": "text",
                        "content": {"plain_text": key},
                        "has_children": True,
                        "children_id": get_children_id(value)

                    }
                )
                arr=(parse_json(arr, value))
            elif type(value)!=dict:
                if type(value)==str:
                    arr.append(
                        {
                            "type": "text",
                            "content": {"plain_text": key},
                            "has_children": True,
                            "children": value,
                        }
                    )
                    arr.append(
                        {
                            "type": "text",
                            "content": {"plain_text": value},
                            "has_children": False,
                        }
                    )
                elif type(value)==list:
                    arr.append(
                        {
                            "type": "text",
                            "content": {"plain_text": key},
                            "has_children": True,
                            "children": value
                        }
                    )
                    for ele in value:
                        if type(ele)==str:
                            arr.append(
                            {
                                "type": "text",
                                "content": {"plain_text": ele},
                                "has_children": False,
                            }
                        )
                        elif type(ele)==dict:
                            arr=parse_json(arr, ele)
    elif type(value)!=dict:
        arr.append("WOW NOT DICT")
        if type(value)==str:
            arr.append((
                {
                    "type": "text",
                    "content": {"plain_text": key},
                    "has_children": True,
                    "children": value,
                },
                {
                    "type": "text",
                    "content": {"plain_text": value},
                    "has_children": False,
                }
            ))
        elif type(value)==list:
            arr.append(
                {
                    "type": "text",
                    "content": {"plain_text": key},
                    "has_children": True,
                    "children": value
                }
            )
            for ele in value:
                if type(ele)==str:
                    arr.append(
                    {
                        "type": "text",
                        "content": {"plain_text": ele},
                        "has_children": True,
                        "children": value
                    },
                    {
                        "type": "text",
                        "content": {"plain_text": ele},
                        "has_children": False,
                    }
                )
                elif type(ele)==dict:
                    arr=parse_json(arr, ele)
            
    return arr
# %%
result=[]
result=parse_json(result, json)
print(result)

# %%
for block in result:
    print(block)

# %%

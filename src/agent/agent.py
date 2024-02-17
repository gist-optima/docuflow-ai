# %%
import os
import sys
BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_PATH)

import subprocess
import time

from utils.gpt import GPT
import json
from pprint import pprint
from inspect import cleandoc
from jsonschema import validate
from requests import request
from threading import Thread

current_directory = BASE_PATH + "\\agent"

prompt_file_path = os.path.join(current_directory, "prompt.json")
fewshot_examples_file_path = os.path.join(current_directory, "examples.json")

prompt = {}
with open(prompt_file_path, "r", encoding="UTF8") as f:
    prompt = json.load(f)
    prompt_params = prompt["params"]
    for (key, value) in prompt_params.items():
        prompt["content"] = prompt["content"].replace(f"<{key}/>", value)
    prompt = prompt["content"]

fewshot_examples = []
with open(fewshot_examples_file_path, "r", encoding="UTF-8") as f:
    fewshot_examples = json.load(f)
    for example in fewshot_examples:
        example["input"] = json.dumps(example["input"], ensure_ascii=False, indent=4)
        example["output"] = json.dumps(example["output"], ensure_ascii=False, indent=4)

class Agent:
    def __init__(self, prompt, fewshot_examples=[]):
        self.gpt = GPT(prompt, fewshot_examples)

        print("Opening API server...")
        self.server = subprocess.Popen(["python", BASE_PATH+"\\api\\api_server.py"], shell=True)
        print("Waiting for the server to fully start...")
        time.sleep(5)

        self.max_retry = 3

    def simulate(self, title="생성형 AI를 활용한 기업 생산성 향상 도구 아이디어톤 기획서"):
        try: 
            self.log = []
            self.doc_log = []

            # 1 =================================================
            # 당신은 주어진 제목을 가지는 보고서나 기획서를 작성합니다. 제목은 다음과 같이 주어집니다:
            # {
            #     "title" : string
            # }

            # 당신은 주어진 제목을 가지고 다음의 단계를 거쳐 보고서나 기획서를 작성합니다. 

            # 1. 제목을 template-generator에 입력하여 보고서의 기본적인 틀을 잡습니다. 시스템에 제목을 입력하기 위해서는 다음의 JSON형식으로 응답하면 됩니다. 
            #     {
            #         "system": "template-generator", 
            #         "parameter": {
            #             "title" : string
            #         }
            #     }
            message = json.dumps({
                "title": title
            }, ensure_ascii=False, indent=2)
            schema = {
                "type": "object",
                "properties": {
                    "system": {
                        "type": "string",
                        "const": "template-generator"
                    },
                    "parameter": {
                        "type": "object",
                        "properties": {
                            "title": {
                                "type": "string"
                            }
                        },
                        "required": ["title"]
                    }
                },
                "required": ["system", "parameter"]
            }
            for i in range(self.max_retry):
                print(cleandoc(
                    """
                    Agent에게 보고서의 제목을 보냅니다. 
                    message: 
                    """))
                print(message)
                print()

                print("Agent의 응답을 기다리는 중...")
                print()

                self.log.append(
                    self.gpt.get_response(message)
                )
                try:
                    validate(self.log[-1], schema)
                except:
                    pass
                else:
                    break
                print(cleandoc(
                    """
                    Agent가 올바르지 않은 형식으로 응답했습니다. 
                    response: 
                    """
                ))
                print(json.dumps(self.log[-1], ensure_ascii=False, indent=2))
                print("expected schema: ")
                print(json.dumps(schema, ensure_ascii=False, indent=2))
                print()

                print(f"올바른 형식으로 응답하도록 다시 Agent에게 묻습니다. (Trial: {i+1} / {self.max_retry})")
                print()

                message = "응답 형식이 잘못되었습니다. 다음과 같은 형식으로 응답해야 합니다." \
                    + json.dumps(schema, ensure_ascii=False, indent=2) \
                    + "\n다시 입력을 주겠습니다: \n" \
                    + message
            else:
                print()
                print(cleandoc(
                    f"""
                    Agent가 올바르지 않은 응답을 하여 재시도하였지만, 최대 재시도 횟수 {self.max_retry}에 도달하여 simulation을 중단합니다. 
                    다음의 대화 기록을 참고하여 디버깅해주세요. 
                    """
                ))
                for log in self.log:
                    print(json.dumps(log, ensure_ascii=False, indent=2))
                print()
                raise Exception("Simulation Failed")
            
            # ======================================================
            # 그러면 사용자(template-generator)은 주어진 제목을 분석하여 보고서의 기본적인 틀을 다음과 예시와 같은 JSON형식으로 제시합니다:
            # {
            #     "system": "template-generator", 
            #     "response" : [
            #         {
            #             "최근 AI모델 시장 분석": {
            #                 "시장 변화": null,
            #                 "시장 점유율": null,
            #                 "시장 가치": null
            #             },
            #             "사내 경쟁 우위 요소 분석": {
            #                 "SWOT 분석": {
            #                     "Strength": null,
            #                     "Weakness": null,
            #                     "Opportunity": null,
            #                     "Threat": null
            #                 }
            #             },
            #             "구체적인 개발 계획": null,
            #             "기대 효과": null
            #         }, 
            #         ...
            #     ]
            # }
            # response로 주어지는 배열의 각 요소인 객체들은 각각 하나의 보고서를 의미합니다. 
            # 당신은 이 보고서 객체들을 보고 분석하여 가장 의도에 부합하는 객체를 선택합니다. 
            # 선택한 객체는 보고서의 기본적인 틀이 되고, 당신은 null에 해당하는 부분을 구체적인 내용으로 채워 보고서를 완성하게 될 것입니다. 
            print(cleandoc(
                """
                Agent가 성공적으로 다음과 같이 system에 요청했습니다. 
                """
            ))
            print(json.dumps(self.log[-1], ensure_ascii=False, indent=2))
            print()

            print("Agent의 요청을 처리합니다.")
            title = self.log[-1]["parameter"]["title"]
            print(cleandoc(
                f"""
                container-generator에 

                [GET]
                http://localhost:5000/container-generator/{title}

                의 요청을 보냅니다...
                """
            ))
            print()
            response = request("GET", f"http://localhost:5000/container-generator/{title}")
            response = json.dumps(json.loads(response.content), ensure_ascii=False, indent=2)
            print("response: ")
            print(response)
            print()
            self.log.append(response)

            # ============================================================

            # 2 =========================================================
            # 사용자(template-generator)가 제시한 보고서 객체들 중 선택하고자 하는 객체의 index를 system에 다음과 같이 JSON형식으로 응답하여 선택할 수 있습니다:
            # {
            #     "system": "template-selector", 
            #     "parameter": {
            #         "template-selection" : int
            #     }
            # }
            # 선택한 보고서 객체는 이제 당신이 작업하는 보고서가 됩니다. 
            message = self.log[-1]
            schema = {
                "type": "object",
                "properties": {
                    "system": {
                        "type": "string",
                        "const": "template-selector"
                    },
                    "parameter": {
                        "type": "object",
                        "properties": {
                            "template-selection": {
                                "type": "number"
                            }
                        },
                        "required": ["template-selection"]
                    }
                },
                "required": ["system", "parameter"]
            }

            for i in range(self.max_retry):
                print(cleandoc(
                    """
                    Agent에게 templates를 보내고 선택을 기다립니다. 
                    message: 
                    """))
                print(message)
                print()

                print("Agent의 응답을 기다리는 중...")
                print()

                self.log.append(
                    self.gpt.get_response(message)
                )
                try:
                    validate(self.log[-1], schema)
                except:
                    pass
                else:
                    break
                print(cleandoc(
                    """
                    Agent가 올바르지 않은 형식으로 응답했습니다. 
                    response: 
                    """
                ))
                print(json.dumps(self.log[-1], ensure_ascii=False, indent=2))
                print("expected schema: ")
                print(json.dumps(schema, ensure_ascii=False, indent=2))
                print()

                print(f"올바른 형식으로 응답하도록 다시 Agent에게 묻습니다. (Trial: {i+1} / {self.max_retry})")
                print()

                message = "응답 형식이 잘못되었습니다. 다음과 같은 형식으로 응답해야 합니다." \
                    + json.dumps(schema, ensure_ascii=False, indent=2) \
                    + "\n다시 입력을 주겠습니다: \n" \
                    + message
            else:
                print()
                print(cleandoc(
                    f"""
                    Agent가 올바르지 않은 응답을 하여 재시도하였지만, 최대 재시도 횟수 {self.max_retry}에 도달하여 simulation을 중단합니다. 
                    다음의 대화 기록을 참고하여 디버깅해주세요. 
                    """
                ))
                for log in self.log:
                    print(json.dumps(log, ensure_ascii=False, indent=2))
                print()
                raise Exception("Simulation Failed")

            # =============================================================
            # 2. 당신은 현재 작업하고 있는 보고서의 null에 해당하는 부분을 구체적인 내용으로 채우기 위해 유용한 snippet들을 수집하게 됩니다. 
            #     당신을 보조하고 있는 최첨단 보고서 작성 시스템은 당신이 작업하고 있는 보고서의 내용을 분석하여 당신에게 유용할 만한 정보를 검색하여 snippet들을 다음과 같이 추천해줍니다:
            #     {
            #         "system": "search-engine", 
            #         "response": [
            #             {
            #                 "snippet-id": int, 
            #                 "snippet-type": "text" | "data" | "image", 
            #                 "content": string
            #             }, 
            #             ...
            #         ]
            #     }
            print(cleandoc(
                """
                Agent가 성공적으로 다음과 같이 system에 요청했습니다. 
                """
            ))
            print(json.dumps(self.log[-1], ensure_ascii=False, indent=2))
            print()

            print("Agent의 요청을 처리합니다.")
            template_selection = self.log[-1]["parameter"]["template-selection"]
            print(cleandoc(
                f"""
                template {template_selection}번을 선택했습니다. 
                template {template_selection}번이 현재 작업하고 있는 보고서의 전체 내용이 됩니다. 
                """
            ))
            print()
            # =================================================================

            # 3 ===============================================================
            # 2. 당신은 현재 작업하고 있는 보고서가 system에 의해 주어집니다. 
            #     당신은 현재 작업하고 있는 보고서의 null에 해당하는 부분을 구체적인 내용으로 채우기 위해 유용한 snippet들을 수집하게 됩니다. 
            #     당신이 현재 작업하고 있는 보고서에서 내용을 추가하거나 수정해야 할 부분의 가장 가까운 부모의 key를 focused container로 하고, 
            #     탐색하고자 하는 내용의 방향성을 guiding vector로 하여 다음과 같이 search-engine에 요청합니다. 
            #     {
            #         "system": "search-engine", 
            #         "parameter": {
            #             "focused container": string, 
            #             "guiding vector": string
            #         }
            #     }
            self.doc_log.append(json.loads(self.log[-2])[template_selection])
            message = """당신이 현재 작업하고 있는 보고서의 내용은 다음과 같습니다: \n""" \
                + json.dumps(self.doc_log[-1], ensure_ascii=False, indent=2) \
                + cleandoc("""
                           
                           당신이 현재 작업하는 보고서의 null에 해당하는 부분을 구체적인 내용으로 채우기 위해 유용한 snippet들을 수집하게 됩니다. 
                           당신이 현재 작업하고 있는 보고서에서 내용을 추가하거나 수정해야 할 부분의 가장 가까운 부모의 key를 focused container로 하고, 
                           하고자 하는 내용의 방향성을 guiding vector로 하여 다음과 같이 search-engine에 요청하십시오... \n
                           """)
            schema = {
                "type": "object",
                "properties": {
                    "system": {
                        "type": "string",
                        "const": "search-engine"
                    },
                    "parameter": {
                        "type": "object",
                        "properties": {
                            "focused container": {
                                "type": "string"
                            }, 
                            "guiding vector": {
                                "type": "string"
                            }
                        },
                        "required": ["focused container", "guiding vector"]
                    }
                },
                "required": ["system", "parameter"]
            }

            for i in range(self.max_retry):
                print(cleandoc(
                    """
                    Agent에게 선택된 template(현재 작업하고 있는 보고서 객체)를 보내고 검색 변수를 묻습니다. 
                    message: 
                    """))
                print(message)
                print()

                print("Agent의 응답을 기다리는 중...")
                print()

                self.log.append(
                    json.dumps(self.gpt.get_response(message), ensure_ascii=False, indent=2)
                )
                try:
                    validate(json.loads(self.log[-1]), schema)
                except:
                    pass
                else:
                    break
                print(cleandoc(
                    """
                    Agent가 올바르지 않은 형식으로 응답했습니다. 
                    response: 
                    """
                ))
                print(self.log[-1])
                print("expected schema: ")
                print(json.dumps(schema, ensure_ascii=False, indent=2))
                print()

                print(f"올바른 형식으로 응답하도록 다시 Agent에게 묻습니다. (Trial: {i+1} / {self.max_retry})")
                print()

                message = "응답 형식이 잘못되었습니다. 다음과 같은 형식으로 응답해야 합니다." \
                    + json.dumps(schema, ensure_ascii=False, indent=2) \
                    + "\n다시 입력을 주겠습니다: \n" \
                    + message
            else:
                print()
                print(cleandoc(
                    f"""
                    Agent가 올바르지 않은 응답을 하여 재시도하였지만, 최대 재시도 횟수 {self.max_retry}에 도달하여 simulation을 중단합니다. 
                    다음의 대화 기록을 참고하여 디버깅해주세요. 
                    """
                ))
                for log in self.log:
                    print(json.dumps(log, ensure_ascii=False, indent=2))
                print()
                raise Exception("Simulation Failed")

            # =====================================================================
            print(cleandoc(
                """
                Agent가 성공적으로 다음과 같이 system에 요청했습니다. 
                """
            ))
            print(self.log[-1])
            print()

            print("Agent의 요청을 처리합니다.")
            print()

            # =====================================================================
            # 3. 당신을 보조하고 있는 최첨단 보고서 작성 시스템은 당신이 제시한 focused container와 guiding vector를 고려하여 당신에게 유용할 만한 정보를 검색하여 snippet들을 다음과 같이 추천해줍니다:
            #     {
            #         "system": "search-engine", 
            #         "response": [
            #             {
            #                 "snippet-id": int, 
            #                 "snippet-type": "text" | "data" | "image", 
            #                 "content": string
            #             }, 
            #             ...
            #         ]
            #     }
            print("현재 작업하고 있는 보고서의 내용과 focused container, guiding vector를 토대로 검색어를 생성합니다.")
            focused_container = json.loads(self.log[-1])["parameter"]["focused container"]
            guiding_vector = json.loads(self.log[-1])["parameter"]["guiding vector"]
            headers = {
                "all contents": self.doc_log[-1], 
                "focused container": focused_container, 
                "guiding vector": guiding_vector
            }
            print(cleandoc(
                f"""
                query-generator에 

                [POST]
                http://localhost:5000/query-generator
                header: 
                """
            ))
            print(json.dumps(headers, ensure_ascii=False, indent=2))
            print()
            print("의 요청을 보냅니다...")
            print()

            response = request("POST", f"http://localhost:5000/query-generator", json=headers)
            response = json.dumps(json.loads(response.content), ensure_ascii=False, indent=2)
            print("response: ")
            print(response)
            print()
            self.log.append(response)

            print("각 query에 대한 google search를 수행합니다. ")
            queries = json.loads(self.log[-1])
            print(cleandoc(
                f"""
                google-search에 

                [GET]
                """
            ))
            n = 3
            print("\n".join([f"http://localhost:5000/google-search/{query}/{n}" for query in queries]))
            print()
            print("의 요청을 동기적으로 보냅니다...")
            print()

            responses = []
            def worker(query):
                responses.append(
                    request("GET", f"http://localhost:5000/google-search/{query}/{n}").content
                )
            threads = []
            for query in queries:
                thread = Thread(target=worker, args=[query, ])
                threads.append(thread)
                thread.start()
            for thread in threads:
                thread.join()

            print("response: ")
            self.log.append(responses)
            for response in self.log[-1]:
                print(json.dumps(json.loads(response), ensure_ascii=False, indent=2))
            
            print("검색 결과에서 잠재적 snippet들을 추출합니다. ")
            print(cleandoc(
                f"""
                snippet-extractor에 

                [POST]
                http://localhost:5000/snippet-extractor
                header: 
                """
            ))
            print()
            articles = [value for a in self.log[-1] for value in json.loads(a).values()]
            headers = {
                "articles": articles, 
                "all contents": self.doc_log[-1], 
                "focused container": focused_container, 
                "guiding vector": guiding_vector, 
                "shown snippets": [], 
                "preffered snippet": ""
            }
            print(
                json.dumps(
                    headers, 
                    ensure_ascii=False, 
                    indent=2
                )
            )
            print("의 요청을 보냅니다...")
            print()

            response = request("POST", "http://localhost:5000/snippet-extractor", json=headers)
            print("response: ")
            print(response)

            return response
        
            # ================================================================
                
            # 3 ==============================================================
            
            # message = "현재 작성하고 있는 보고서의 내용은 다음과 같습니다. \n" \
            #     + json.dumps(json.loads(self.log[-2])[template_selection], ensure_ascii=False, indent=2)
            # schema = {
            #     "type": "object",
            #     "properties": {
            #         "system": {
            #             "type": "string",
            #             "const": "snippet-selector"
            #         },
            #         "parameter": {
            #             "type": "object",
            #             "properties": {
            #                 "target-id": {
            #                     "type": "string"
            #                 }, 
            #                 "snippet-id": "string"
            #             },
            #             "required": ["target-id", "snippet-id"]
            #         }
            #     },
            #     "required": ["system", "parameter"]
            # }

            # for i in range(self.max_retry):
            #     print(cleandoc(
            #         """
            #         Agent에게 templates를 보내고 선택을 기다립니다. 
            #         message: 
            #         """))
            #     print(message)
            #     print()

            #     print("Agent의 응답을 기다리는 중...")
            #     print()

            #     self.log.append(
            #         self.gpt.get_response(message)
            #     )
            #     try:
            #         validate(self.log[-1], schema)
            #     except:
            #         pass
            #     else:
            #         break
            #     print(cleandoc(
            #         """
            #         Agent가 올바르지 않은 형식으로 응답했습니다. 
            #         response: 
            #         """
            #     ))
            #     print(json.dumps(self.log[-1], ensure_ascii=False, indent=2))
            #     print("expected schema: ")
            #     print(json.dumps(schema, ensure_ascii=False, indent=2))
            #     print()

            #     print(f"올바른 형식으로 응답하도록 다시 Agent에게 묻습니다. (Trial: {i+1} / {self.max_retry})")
            #     print()

            #     message = "응답 형식이 잘못되었습니다. 다음과 같은 형식으로 응답해야 합니다." \
            #         + json.dumps(schema, ensure_ascii=False, indent=2) \
            #         + "\n다시 입력을 주겠습니다: \n" \
            #         + message
            # else:
            #     print()
            #     print(cleandoc(
            #         f"""
            #         Agent가 올바르지 않은 응답을 하여 재시도하였지만, 최대 재시도 횟수 {self.max_retry}에 도달하여 simulation을 중단합니다. 
            #         다음의 대화 기록을 참고하여 디버깅해주세요. 
            #         """
            #     ))
            #     for log in self.log:
            #         print(json.dumps(log, ensure_ascii=False, indent=2))
            #     print()
            #     raise Exception("Simulation Failed")

            # # =============================================================
            # print(cleandoc(
            #     """
            #     Agent가 성공적으로 다음과 같이 system에 요청했습니다. 
            #     """
            # ))
            # print(json.dumps(self.log[-1], ensure_ascii=False, indent=2))
            # print()

            # print("Agent의 요청을 처리합니다.")
            # template_selection = self.log[-1]["parameter"]["template-selection"]
            # print(cleandoc(
            #     f"""
            #     template {template_selection}번을 선택했습니다. 
            #     """
            # ))
            # print()
        
        finally:
            self.server.kill()
        
            
        
        
# %%
agent = Agent(prompt, fewshot_examples)
# %%
result = agent.simulate() 

# %%
result

# %%

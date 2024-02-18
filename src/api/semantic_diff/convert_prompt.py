# %%
import json

with open('prompt.txt', 'r') as f:
    content=f.read()

content=json.dumps(content, ensure_ascii=False, indent=4)
prompt={"content": content}
print(prompt)

with open('prompt.json', 'w') as f:
    f.write(json.dumps(prompt, ensure_ascii=False, indent=4).replace('\\\\n', " "))

# %% convert json-string format
text='''
제목: 학교 생활에 대한 학생 만족도 조사 및 분석

서론

학교 생활은 학생들이 지식을 습득하고 사회적 기술을 개발하는 곳이며, 그들의 성취와 만족도에 직결된다. 이 보고서는 저희 학교의 학생들이 학교 생활에 대해 얼마나 만족하고 있는지를 조사하고 분석한 결과를 제시한다. 이를 통해 학교의 강점을 확립하고 개선할 부분을 도출할 것이다.

조사 방법

본 조사는 2023년 10월에 학교 내 전 과정 학생 500명을 대상으로 실시되었다. 설문지는 학교 생활의 다양한 측면을 포괄하도록 구성되었으며, 만족도를 측정하기 위한 Likert 형식의 척도를 사용하였다. 또한, 개방형 질문을 통해 학생들의 의견과 제안을 수렴하였다.

결과

조사 결과, 학생들의 전반적인 학교 만족도는 높은 편이었다. 만족도 평균 점수는 4.3로, 5점 만점 기준으로 높은 수준이었다. 특히, 교사의 열정과 가르침에 대한 만족도가 높았으며, 학교 시설과 자원에 대한 만족도도 양호한 편이었다.

그러나, 일부 학생들은 학교 내의 대외 활동 및 동아리 활동에 대한 지원이 부족하다고 지적했다. 또한, 학교의 학습 환경과 관련하여 기술적 시설 및 자료의 부족을 언급하는 응답도 있었다.

토론

이러한 결과는 학교가 학생들에게 다양한 활동 및 자원을 제공함으로써 학생 만족도를 높일 수 있다는 점을 시사한다. 특히, 학교는 학생들의 다양한 관심과 필요에 부합하는 동아리 및 대외 활동을 지원하는데 노력해야 할 것이다. 또한, 학습 환경을 개선하기 위해 기술적 시설과 자료의 향상이 필요하다.

결론

이 보고서를 통해 학교는 자체적인 강점을 인식하고 발전시키는 데 중점을 둘 수 있을 것이다. 학생들의 의견을 수렴하고, 그들의 요구를 충족시키는 노력은 학교의 발전과 성공에 더할 나위 없다.

참고문헌

Smith, J. (2020). Enhancing Student Satisfaction in Higher Education: A Review of Best Practices. Journal of Higher Education Management, 15(2), 45-60.
Brown, A., & Lee, C. (2019). Student Engagement and Success: Strategies for Improving Retention Rates. Educational Leadership Quarterly, 25(4), 112-125.
'''

print(json.dumps(text, ensure_ascii=False, indent=4))

# %%

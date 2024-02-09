# %% import
import requests

# %% make container
# title: ["docuflow가 속한 시장 분석 및 진입 전략", "docuflow의 고객 페르소나 및 시나리오 정의"]
title="docuflow이 속한 시장 분석 및 진입 전략"

response=requests.get("http://localhost:5000/container-generator/{title}")
if response.status_code==200:
    init_container=response.content

# %% init_container result
init_container='''
[
  {
    "시장 분석": {
      "산업 개요": null,
      "시장 규모 및 성장률": null,
      "경쟁 구도": null,
      "고객 분석": null,
      "기술 트렌드": null,
      "규제 환경": null
    },
    "경쟁사 분석": {
      "주요 경쟁사": null,
      "시장 점유율": null,
      "경쟁사 전략": null,
      "강점 및 약점 분석": null
    },
    "진입 전략": {
      "목표 시장 선정": null,
      "제품/서비스 포지셔닝": null,
      "가격 전략": null,
      "유통 및 영업 전략": null,
      "파트너십 및 협력 전략": null,
      "리스크 관리": null
    },
    "실행 계획": {
      "마케팅 계획": null,
      "판매 전략": null,
      "법적/규제 준수": null,
      "기술적 실행": null,
      "재무 예측": null
    },
    "성과 측정": {
      "성과 지표 (KPIs)": null,
      "성과 관리 계획": null
    },
    "타임라인 및 이정표": null
  },
  {
    "시장 분석": {
      "시장 규모": null,
      "성장 동력": null,
      "주요 경쟁사 분석": null,
      "고객 분석": null,
      "용도 및 수요": null,
      "트렌드 및 기술 발전": null
    },
    "시장 진입 전략": {
      "목표 시장 선정": null,
      "시장 진입 모델": null,
      "경쟁 우위 전략": null,
      "가격 전략": null,
      "유통 및 홍보 전략": null,
      "파트너십 및 제휴 전략": null
    },
    "위험 요소 및 완화 전략": {
      "시장 위험": null,
      "기술 위험": null,
      "운영 위험": null,
      "재무 위험": null
    },
    "구현 로드맵": {
      "단기 목표": null,
      "중기 목표": null,
      "장기 목표": null
    }
  },
  {
    "시장 개요": {
      "시장 규모": null,
      "시장 성장률": null,
      "주요 플레이어": null,
      "시장 성숙도": null
    },
    "대상 고객 분석": {
      "고객 요구사항": null,
      "고객 세분화": null
    },
    "경쟁자 분석": {
      "직접 경쟁자": null,
      "간접 경쟁자": null,
      "경쟁자 제품/서비스 비교": null
    },
    "진입 장벽 분석": {
      "기술적 장벽": null,
      "경제적 장벽": null,
      "규제 및 법적 장벽": null,
      "시장 접근 장벽": null
    },
    "진입 전략": {
      "제품/서비스 차별화": null,
      "가격 전략": null,
      "유통 전략": null,
      "프로모션 전략": null
    },
    "위험 관리 및 완화 전략": {
      "시장 위험": null,
      "운영 위험": null,
      "기술 위험": null,
      "정책 및 규제 위험": null
    },
    "사업 실행 로드맵": {
      "단기 목표": null,
      "중기 목표": null,
      "장기 목표": null
    }
  },
  {
    "시장 분석": {
      "시장 규모": null,
      "성장률": null,
      "동향 분석": null,
      "경쟁사 분석": {
        "주요 경쟁사": null,
        "시장 점유율": null,
        "경쟁사 전략": null
      },
      "고객 세분화": null,
      "수요 요인": null,
      "공급 사슬": null,
      "규제 환경": null
    },
    "진입 전략": {
      "시장 세분화 목표 설정": null,
      "가치 제안": null,
      "차별화 전략": null,
      "파트너십 및 협력": null,
      "가격 전략": null,
      "마케팅 및 판매 전략": null,
      "진입 장벽 극복 전략": null
    },
    "리스크 평가 및 대응 전략": {
      "리스크 식별": null,
      "영향 평가": null,
      "우선 순위화": null,
      "대응 계획": null
    },
    "가능성 및 실행성 분석": {
      "다짐 가능성 분석": null,
      "자원 요건 분석": null,
      "실행 계획": null
    }
  },
  {
    "시장 개요": {
      "시장 규모": null,
      "성장률": null,
      "주요 플레이어": null,
      "시장 동향": null
    },
    "타깃 고객 분석": {
      "고객 세분화": null,
      "고객 요구사항": null,
      "구매 결정요인": null
    },
    "경쟁자 분석": {
      "경쟁자 목록": null,
      "경쟁자 전략": null,
      "시장 점유율": null,
      "경쟁자 강점과 약점": null
    },
    "진입 전략": {
      "제품 차별화": null,
      "가격 경쟁력": null,
      "파트너십 전략": null
    },
    "SWOT 분석": {
      "Strength": null,
      "Weakness": null,
      "Opportunity": null,
      "Threat": null
    },
    "진입 장벽": null,
    "위험 관리 계획": null
  },
  {
    "시장 개요": {
      "현재 시장 상황": null,
      "주요 경쟁자 분석": null,
      "시장 동향 및 예측": null,
      "고객 요구 사항": null
    },
    "경쟁자 비교": {
      "제공하는 기능 비교": null,
      "가격 정책 비교": null,
      "시장 점유율 분석": null,
      "고객 만족도 평가": null
    },
    "docuflow의 경쟁력": {
      "독창적 기능": null,
      "기술적 우위": null,
      "비용 대비 이점": null,
      "고객 지원 및 서비스": null
    },
    "진입 전략": {
      "목표 시장 선정": null,
      "분석 기반 전략 개발": null,
      "다른 기능과의 통합": null,
      "마케팅 및 홍보 전략": null
    },
    "리스크 평가 및 관리 계획": {
      "시장 리스크": null,
      "기술 리스크": null,
      "운영 리스크": null,
      "금융 리스크": null
    },
    "프로젝트 일정 및 예산": {
      "전체 프로젝트 일정": null,
      "예산 배분": null,
      "마일스톤": null
    },
    "성과 측정 및 평가 기준": {
      "시장 진입 성공 평가": null,
      "매출 및 이익 측정": null,
      "고객 획득 및 유지": null
    }
  }
]
'''

select_container='''
  {
    "시장 개요": {
      "현재 시장 상황": null,
      "주요 경쟁자 분석": null,
      "시장 동향 및 예측": null,
      "고객 요구 사항": null
    },
    "경쟁자 비교": {
      "제공하는 기능 비교": null,
      "가격 정책 비교": null,
      "시장 점유율 분석": null,
      "고객 만족도 평가": null
    },
    "docuflow의 경쟁력": {
      "독창적 기능": null,
      "기술적 우위": null,
      "비용 대비 이점": null,
      "고객 지원 및 서비스": null
    },
    "진입 전략": {
      "목표 시장 선정": null,
      "분석 기반 전략 개발": null,
      "다른 기능과의 통합": null,
      "마케팅 및 홍보 전략": null
    },
    "리스크 평가 및 관리 계획": {
      "시장 리스크": null,
      "기술 리스크": null,
      "운영 리스크": null,
      "금융 리스크": null
    },
    "프로젝트 일정 및 예산": {
      "전체 프로젝트 일정": null,
      "예산 배분": null,
      "마일스톤": null
    },
    "성과 측정 및 평가 기준": {
      "시장 진입 성공 평가": null,
      "매출 및 이익 측정": null,
      "고객 획득 및 유지": null
    }
  }
'''
# %% 

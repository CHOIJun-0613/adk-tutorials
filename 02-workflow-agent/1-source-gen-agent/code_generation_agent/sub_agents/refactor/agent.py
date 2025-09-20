from re import A
import warnings
from google.adk.agents import LlmAgent
# Non-Google LLM을 연결하기 위한 LiteLLM 래퍼
# Ollama, LMStudio, OpenAI 등 다양한 LLM 제공업체를 지원합니다.
from google.adk.models.lite_llm import LiteLlm
from code_generation_agent.ai_providers import ai_provider_manager

# Google ADK의 실험적 기능 경고 숨기기
warnings.filterwarnings("ignore", message=".*BaseAuthenticatedTool.*", category=UserWarning)
warnings.filterwarnings("ignore", message=".*EXPERIMENTAL.*", category=UserWarning)
warnings.filterwarnings("ignore", message=".*Field name.*shadows an attribute.*", category=UserWarning)

AGENT_NAME = "code_refactor_agent"
DESCRIPTION = "리뷰 코멘트를 기반으로 코드를 리팩토링합니다."
INSTRUCTION = """
    당신은 Spring Boot 기반 java 소스 코드 리팩토링 인공지능입니다.
    당신의 목표는 제공된 코드 리뷰 코멘트를 바탕으로 주어진 Spring Boot 기반 java 소스 코드를 개선하는 것입니다.
    
    **원본 코드(Original Code):**
    ```java
    {generated_code}
    ```
    
    **리뷰 코멘트(Review Comments):**
    {review_comments}
    
    **작업 지침(Task):**
    리뷰 코멘트의 제안을 신중하게 반영하여 원본 코드를 리팩토링하세요.
    리뷰 코멘트에 "큰 문제 없음"이라고 명시되어 있다면, 코드를 수정하지 말고 원본 코드를 그대로 반환하세요.
    최종 코드는 전체적으로 완성되어 있어야 하며, 필요한 import문과 docstring도 포함해야 합니다.
    
    **출력형식(Output):**
    최종 리팩토링된 Java 코드 블록만 출력하세요.
    코멘트는 한국어로 작성하세요.
    코드는 반드시 세 개의 백틱(java ... )으로 감싸야 하며,
    그 외 다른 텍스트는 출력하지 마세요.
"""
OUTPUT_KEY = "refactored_code"


try:
    llm = ai_provider_manager.create_llm(provider_name="google", model_name="gemini-2.0-flash")
    provider_info = ai_provider_manager.get_provider_info()
    print(f"\n🤖 Agent Name : {AGENT_NAME}")
    print(f"\n🤖 AI Provider: {provider_info['provider']}")
    print(f"📱 모델: {provider_info['model']}")
    
    # 로드된 도구세트로 ADK LLM Agent 구성
    code_refactor_agent = LlmAgent(
        model=llm,  # AI Provider Manager에서 생성한 LLM 사용
        name=AGENT_NAME,
        description=DESCRIPTION,
        instruction=INSTRUCTION,
        output_key=OUTPUT_KEY
    )
except Exception as e:
    print(f"⚠️ AI Provider 초기화 실패: {e}")
    print("Google Gemini로 폴백합니다.")
    
    # 폴백: Google Gemini 사용
    code_refactor_agent = LlmAgent(
        model="gemini-1.5-flash",  # 기본 Google Gemini 모델
        name=AGENT_NAME,
        description=DESCRIPTION,
        instruction=INSTRUCTION,
        output_key=OUTPUT_KEY
    )
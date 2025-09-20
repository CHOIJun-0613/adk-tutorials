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

AGENT_NAME = "code_reviewer_agent"
DESCRIPTION = "코드를 검토하는 에이전트 입니다."
INSTRUCTION = """
    당신은 숙련된 Sprong Boot 기반 java 소스 코드 리뷰어입니다.
    제공된 코드를 기반으로 건설적인 피드백을 제공하는 것이 당신의 역할입니다.
    
    **리뷰 대상 코드(Code to Review):**
    ```java
    {generated_code}
    ```
    
    **리뷰 기준(Review Criteria):**
    1.  **정확성:** 코드가 의도한 대로 작동하나요? 논리적 오류는 없나요?
    2.  **가독성:** 코드는 명확하고 이해하기 쉬운가요? PEP 8 스타일 가이드라인을 따르고 있나요?
    3.  **효율성:** 코드가 적절히 효율적인가요? 명백한 성능 병목은 없나요?
    4.  **엣지 케이스:** 잠재적인 엣지 케이스나 잘못된 입력을 잘 처리하고 있나요?
    5.  **베스트 프랙티스:** 일반적인 Spring Boot 기반 java 소스 베스트 프랙티스를 따르고 있나요?
    
    **출력(Output):**
    피드백은 코드를 제외하고 가능하면 한국어로 작성하세요.
    피드백은 간결한 핵심 항목 위주의 불릿 리스트로 작성하세요.
    코드가 매우 우수하여 수정할 사항이 없다면, 단순히 다음과 같이 작성하세요: "큰 문제 없음"
    출력은 *피드백 목록 또는 해당 문장만* 포함해야 하며, 그 외의 텍스트는 포함하지 마세요.
"""
OUTPUT_KEY = "review_comments"

try:
    llm = ai_provider_manager.create_llm(provider_name="google", model_name="gemini-2.0-flash")
    provider_info = ai_provider_manager.get_provider_info()
    print(f"\n🤖 Agent Name : {AGENT_NAME}")
    print(f"\n🤖 AI Provider: {provider_info['provider']}")
    print(f"📱 모델: {provider_info['model']}")
    
    # 로드된 도구세트로 ADK LLM Agent 구성
    code_reviewer_agent = LlmAgent(
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
    code_reviewer_agent = LlmAgent(
        model="gemini-1.5-flash",  # 기본 Google Gemini 모델
        name=AGENT_NAME,
        description=DESCRIPTION,
        instruction=INSTRUCTION,
        output_key=OUTPUT_KEY
    )
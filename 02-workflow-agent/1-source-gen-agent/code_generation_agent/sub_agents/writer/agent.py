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

INSTRUCTION = """
        당신은 Spring Boot 기반 Java 소스스 코드 생성기입니다.
        사용자의 요청 *내용만을 기반으로* 요구사항을 충족하는 Java 코드를 작성하세요.
        결과는 *오직* 전체 Java 코드 블럭만을 출력하며, 세개의 백틱(```java ... ```)으로 감싸야 합니다.
        코드 블럭 전후에는 그 외의 어떤 텍스트도 추가하지 마세요.    
        """

 # AI Provider Manager를 사용하여 현재 설정된 Provider에 맞는 LLM 생성
try:
    llm = ai_provider_manager.create_llm(provider_name="lmstudio", model_name="lm_studio/qwen/qwen3-8b")
    provider_info = ai_provider_manager.get_provider_info()
    print(f"\n[bold blue]🤖 AI Provider: {provider_info['provider']}[/bold blue]")
    print(f"[bold blue]📱 모델: {provider_info['model']}[/bold blue]")
    
    # 로드된 도구세트로 ADK LLM Agent 구성
    code_writer_agent = LlmAgent(
        model=llm,  # AI Provider Manager에서 생성한 LLM 사용
        name="code_writer_agent",
        description="코드를 작성하는 에이전트 입니다.",
        instruction=INSTRUCTION,
        output_key="generated_code"
    )
except Exception as e:
    print(f"[bold red]⚠️ AI Provider 초기화 실패: {e}[/bold red]")
    print("[bold yellow]Google Gemini로 폴백합니다.[/bold yellow]")
    
    # 폴백: Google Gemini 사용
    code_writer_agent = LlmAgent(
        model="gemini-1.5-flash",  # 기본 Google Gemini 모델
        name="code_writer_agent",
        description="코드를 작성하는 에이전트 입니다.",
        instruction=INSTRUCTION,
        output_key="generated_code"
    )


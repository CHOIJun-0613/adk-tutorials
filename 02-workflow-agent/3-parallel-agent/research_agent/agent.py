from google.adk.agents import ParallelAgent, SequentialAgent
from .sub_agents.renewable_energy import renewable_energy_agent
from .sub_agents.ev_technology import ev_technology_agent
from .sub_agents.carbon_capture import carbon_capture_agent
from .sub_agents.synthersizer import synthersis_agent

parallel_research_agent = ParallelAgent(
    name="parallel_research_agent",
    description="여러 연구 에이전트를 병렬로 실행하여 정보를 수집하는 에이전트트",
    sub_agents=[renewable_energy_agent, ev_technology_agent, carbon_capture_agent]
)

sequential_pipeline_agent = SequentialAgent(
    name="sequential_pipeline_agent",
    description="병렬 연구 결과를 기반으로 구조화된 리포트를 생성하는 시퀀셜 에이전트",
    sub_agents=[parallel_research_agent, synthersis_agent]
)
root_agent = sequential_pipeline_agent

if __name__ == "__main__":
    root_agent.run(
        "재생 에너지, 전기차 기술, 탄소 포집 방법에 대한 최근 동향을 연구해주세요."
    )
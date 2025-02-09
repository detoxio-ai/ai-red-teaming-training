# pip install -U autogen-agentchat autogen-ext[openai,web-surfer]
# playwright install
import asyncio
from autogen_agentchat.agents import AssistantAgent, UserProxyAgent
from autogen_agentchat.conditions import TextMentionTermination
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_ext.agents.web_surfer import MultimodalWebSurfer
from autoattack.ext.amass_agent import AmassToolAgent
from autogen_ext.teams.magentic_one import MagenticOne

async def main() -> None:
    model_client = OpenAIChatCompletionClient(model="gpt-4o")
    assistant = AssistantAgent("assistant", model_client)
    web_surfer = MultimodalWebSurfer("web_surfer", model_client)
    m1 = MagenticOne(client=model_client)
    amass_tool = AmassToolAgent("amass_tool", model_client)
    termination = TextMentionTermination("TERMINATE") # Type 'exit' to end the conversation.
    team = RoundRobinGroupChat([amass_tool, assistant, m1], termination_condition=termination)
    await Console(team.run_stream(task="Find the subdomains of prismforce company"))

asyncio.run(main())

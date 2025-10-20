from langchain.agents import initialize_agent, load_tools
from langchain.llms import OpenAI
from langchain.memory import ConversationBufferMemory
from dotenv import load_dotenv
import os

# Load API key
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Initialize model and tools
llm = OpenAI(temperature=0.7)
tools = load_tools(["serpapi", "llm-math"], llm=llm)

# Add conversational memory
memory = ConversationBufferMemory(memory_key="chat_history")

# Initialize agent
agent = initialize_agent(
    tools, llm,
    agent_type="conversational-react-description",
    memory=memory,
    verbose=True
)

# Run agent
print("🤖 Research Assistant Agent Ready!")
response = agent.run("Summarize the impact of AI in scientific research.")
print(response)

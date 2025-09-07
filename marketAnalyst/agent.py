from langchain_google_genai import ChatGoogleGenerativeAI
from typing import TypedDict,Annotated,Sequence
from langgraph.graph.message import add_messages
from langgraph.graph import START,StateGraph,END
from langchain_core.messages import SystemMessage,HumanMessage,BaseMessage,AIMessage
from langgraph.prebuilt import ToolNode 
from marketAnalyst.scraper import getLinks
import os
from dotenv import load_dotenv
load_dotenv()

tools=[getLinks]

model=ChatGoogleGenerativeAI(
    model="gemini-1.5-pro",
    api_key=os.getenv("GEMINI_API")
).bind_tools(tools)


class node(TypedDict):
    messages: Annotated[Sequence[BaseMessage],add_messages]
    plan:str
    
def marketAnalyst(state:node)->node:
    print('Thinking Market..')
    system=SystemMessage(content="""You are a Market analyst that searhes for market trends based on the plan given to you
                         STRICT RULE: Before generating any output, you MUST call the tool to fetch up-to-date financial or industry data about the company in question. 
                         . Perform only the tasks of the market analyst and ignore others talk about the following
                         - Market Size and Growth
                         - Trends
                         - Target audience analysis
    You have been provided a tool which can help you search for the latest information make use of that whenever necessary
    The output should just be a json and nothing else, the json should include market size, trends and targetAudience""")
    
    plan=HumanMessage(content="Plan : "+state['plan'])
    message=[system,plan]+state['messages']
    
    results=model.invoke(message)
    # print(results.content)
    return {
        "messages":state["messages"]+[results],
        "plan":state['plan']
    }

def checkCondition(state: node) -> str:
    print('checking Market..')
    lastMessage = state["messages"][-1]
    if isinstance(lastMessage, AIMessage) and getattr(lastMessage, "tool_calls", None):
        return "continue"
    return "end"


graph=StateGraph(node)
graph.add_node("market",marketAnalyst)
graph.add_node("tool",ToolNode(tools))
graph.add_edge(START,"market")
graph.add_conditional_edges(
    "market",
    checkCondition,
    {
        "continue":"tool",
        "end":END
    }
)
graph.add_edge("tool","market")

app=graph.compile()

def start(plan:str)->str:
    # plan=""
    # with open("plan.txt",'r') as f:
    #     plan+=f.read()

    input={"messages":[],"plan":plan}
    results=app.invoke(input)
    # print("*"*40)
    # print(results['messages'][-1].content)
    # print("*"*40)
    print("Market ENDED")
    return results['messages'][-1].content


from langchain_google_genai import ChatGoogleGenerativeAI
from typing import TypedDict,Annotated,Sequence
from langgraph.graph.message import add_messages
from langgraph.graph import START,StateGraph,END
from langchain_core.messages import SystemMessage,HumanMessage,BaseMessage,AIMessage
from langgraph.prebuilt import ToolNode 
from scraper import getLinks
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
    
def finance(state:node)->node:
    print('Thinking..')
    system=SystemMessage(content="""You are a Financial Modeler Agent that does the work based on the plan given, dont do the work of others just focus on yours
                         - You have been given tools which can be used to access the internet, make use of it whenever needed
                         - Return the answer in json with no extra information
                         - Make sure to include numbers in the answer
                         - Research the internet about other companies get some figures and then estimate
                         - The json should contain revenue model, cost structure, funding requirements and key metrics""")
    
    plan=HumanMessage(content="Plan : "+state['plan'])
    message=[system,plan]+state['messages']
    
    results=model.invoke(message)
    # print(results.content)
    return {
        "messages":state["messages"]+[results],
        "plan":state['plan']
    }

def checkCondition(state: node) -> str:
    print('checking..')
    lastMessage = state["messages"][-1]
    if isinstance(lastMessage, AIMessage) and getattr(lastMessage, "tool_calls", None):
        return "continue"
    return "end"


graph=StateGraph(node)
graph.add_node("market",finance)
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

plan=""
with open("plan.txt",'r') as f:
    plan+=f.read()

input={"messages":[],"plan":plan}
results=app.invoke(input)
print("*"*40)
print(results['messages'][-1].content)
print("*"*40)

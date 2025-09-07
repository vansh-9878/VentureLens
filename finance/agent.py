from langchain_google_genai import ChatGoogleGenerativeAI
from typing import TypedDict,Annotated,Sequence
from langgraph.graph.message import add_messages
from langgraph.graph import START,StateGraph,END
from langchain_core.messages import SystemMessage,HumanMessage,BaseMessage,AIMessage
from langgraph.prebuilt import ToolNode 
from finance.scraper import getLinks
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
    print('Thinking Finance.. ')
    system=SystemMessage(content="""You are a Financial Modeler Agent that does the work based on the plan given, dont do the work of others just focus on yours
                         STRICT RULE: Before generating any output, you MUST call the tool to fetch up-to-date financial or industry data about the company in question. 
                         - Use the tool to search about other companies get some figures and then estimate
                         - Return the answer in json with no extra information
                         - Make sure to include numbers in the answer and that should be in rupees
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
    print('checking Finance..')
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

def start(plan:str)->str:
    input={"messages":[],"plan":plan}
    results=app.invoke(input)
    # print("*"*40)
    # print(results['messages'][-1].content)
    # print("*"*40)
    print("Finance ENDED")
    return results['messages'][-1].content


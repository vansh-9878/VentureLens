from langchain_google_genai import ChatGoogleGenerativeAI
from typing import TypedDict
from langgraph.graph import START,StateGraph,END
from langchain_core.messages import SystemMessage,HumanMessage
import os;
from dotenv import load_dotenv
load_dotenv()

model=ChatGoogleGenerativeAI(
    model="gemini-1.5-pro",
    api_key=os.getenv("GEMINI_API")
)

class node(TypedDict):
    title: str
    description:str
    plan:str
    

def marketAnalyst(state:node)->node:
    system=SystemMessage(content="""You are a Market analyst that searhes for market trends based on the plan given to you
                         . Perform only the tasks of the market analyst and ignore others talk about the following
                         - Market Size and Growth
                         - Trends
                         - Target audience analysis""")
    
    plan="Plan : "+state['plan']
    message=[system]+[plan]
    
    results=model.invoke(message)
    print(results.content)
    return state


graph=StateGraph(node)
graph.add_node("market",marketAnalyst)
graph.add_edge(START,"market")
graph.add_edge("market",END)

app=graph.compile()

plan=""
with open("plan.txt",'r') as f:
    plan+=f.read()

input={"title":"MindCares","description":"A chatbot that takes care of your mental health, knows everythin about you and becomes you best friends","plan":plan}
results=app.invoke(input)

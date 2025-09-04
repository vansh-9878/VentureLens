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
    
    
def agent(state:node)->node:
    system=SystemMessage(content="""You are a AI planner that takes in user's starup information and creates a detailed plan for 
    other assistants to work on.
    1) Market Analyst that analyzes the trends
    2) Competitor Searcher that searches for similar companies
    3) Merits and demerits provider
    4) Financial Modeler that creates the estimated financial requirements
    These are the agents and their tasks. Your plan should include details that will help them in doing their tasks based on the user's input
    """)
    
    input=f"Title : {state['title']} , Description : {state['description']}"
    message=[system]+[input]
    
    result=model.invoke(message)
    # print(result.content)
    return {
        "title":state['title'],
        "description":state["description"],
        "plan":result.content
    }

graph=StateGraph(node)
graph.add_node("agent",agent)
graph.add_edge(START,"agent")
graph.add_edge("agent",END)


app=graph.compile()


input={"title":"MindCares","description":"A chatbot that takes care of your mental health, knows everythin about you and becomes you best friends","plan":""}
results=app.invoke(input)

with open("plan.txt","w") as f:
    f.write(results['plan'])


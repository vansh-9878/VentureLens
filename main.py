from langchain_google_genai import ChatGoogleGenerativeAI
from typing import TypedDict,Annotated,List
from langgraph.graph import START,StateGraph,END
from langchain_core.messages import SystemMessage,HumanMessage
from competitorScout.agent import start as startCompetitor
from finance.agent import start as startFinance
from marketAnalyst.agent import start as startMarket
from swotAgent.agent import start as startSwot 
from operator import add
import re
import json
import os;
from dotenv import load_dotenv
load_dotenv()


def safe_json_loads(text: str):
    """
    Try to clean and parse JSON safely from LLM output.
    """
    # Remove code fences like ```json ... ```
    cleaned = re.sub(r"```(?:json)?", "", text).strip()

    try:
        return json.loads(cleaned)
    except json.JSONDecodeError as e:
        print("JSON decode error:", e)
        # Attempt to fix bad escape sequences
        cleaned = cleaned.replace("\\", "\\\\")
        try:
            return json.loads(cleaned)
        except:
            return {"error": "Invalid JSON", "raw": cleaned}


model=ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    api_key=os.getenv("GEMINI_API")
)

class node(TypedDict):
    title: str
    description:str
    plan:str
    output: Annotated[List[str],add]
    final: List
    
def planner(state:node)->node:
    system=SystemMessage(content="""You are a AI planner that takes in user's starup information and creates a detailed plan for 
    other assistants to work on.
    1) Market Analyst that analyzes the trends
    2) Competitor Searcher that searches for similar companies
    3) Merits and demerits provider
    4) Financial Modeler that creates the estimated financial requirements
    These are the agents and their tasks. Your plan should include details that will help them in doing their tasks based on the user's input and specify them to use Rupees as the currency
    """)
    
    input=f"Title : {state['title']} , Description : {state['description']}"
    message=[system]+[input]
    
    result=model.invoke(message)
    # print(result.content)
    return{
        "title": state['title'],
        "description": state['description'],
        "plan":result.content,
        "final": state['final'],
        "output":state['output']
    }

def market(state:node)->node:
    ans=startMarket(state['plan'])
    return{
        "output":state['output']+[ans]
    }
def competitor(state:node)->node:
    ans=startCompetitor(state['plan'])
    return{
        "output":state['output']+[ans]
    }

def finance(state:node)->node:
    ans=startFinance(state['plan'])
    return{
        "output":state['output']+[ans]
    }

def swot(state:node)->node:
    ans=startSwot(state['plan'])
    return{
        "output":state['output']+[ans]
    }

def merger(state:node)->node:
    print("merging..")
    system="""You are an assistant that takes in multiple different jsons and return feasibility score in percentage for each
    - return a json with the feasibility scores of each json and one overall score
    the output should be in the following format:
        {
      scores: {
        competitor_analysis: ,
        business_model: ,
        market_analysis: ,
        risk_mitigation:
      },
      overallScore: ,
      explanation: {
        competitor_analysis: "",
        business_model: "",
        market_analysis: "",
        risk_mitigation: "",
        overallScore:""
      }
    }"""
    messages=[system]+state['output']
    results=model.invoke(messages)
    # print(results.content)
    # print(state['output'])
    
    state['output']+=[results.content]
    
    results=[safe_json_loads(i) for i in state['output']]
    # print(results)
    # if(results[-1].error):
    #     match = re.search(r'\{.*\}', results[-1]["raw"], re.DOTALL)
    #     if match:
    #         json_str = match.group(0)  # this is the valid JSON portion
    #         ans = json.loads(json_str)
    #         results[-1]=ans
            
    return{
        "title": state['title'],
        "description": state['description'],
        "plan":state['plan'],
        "output":state['output'],
        "final": results
    }


graph=StateGraph(node)
graph.add_node("planner",planner)
graph.add_node("market",market)
graph.add_node('finance',finance)
graph.add_node("swot",swot)
graph.add_node("competitor",competitor)
graph.add_node("merger",merger)

graph.add_edge(START,"planner")
graph.add_edge("planner","market")
graph.add_edge("planner","finance")
graph.add_edge("planner","swot")
graph.add_edge("planner","competitor")
graph.add_edge("market","merger")
graph.add_edge("competitor","merger")
graph.add_edge("swot","merger")
graph.add_edge("finance","merger")
graph.add_edge("merger",END)


app=graph.compile()


def startSearching(title:str,description:str)->List:
    input={"title":title,"description":description,"plan":"","final":[],"output":[]}
    results=app.invoke(input)
    return results['final']
    
    

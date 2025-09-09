from serpapi import GoogleSearch
import os
from dotenv import load_dotenv
from ddgs import DDGS
import requests
from bs4 import BeautifulSoup
from langchain_core.tools import tool
load_dotenv()


def getText(results)->str:
  answer=""
  for i in results:
    print(i)
    # link="https://www.grandviewresearch.com/industry-analysis/ai-mental-health-market-report"
    link=i
    response=requests.get(link)
    sp=BeautifulSoup(response.text,'html.parser')
    texts=sp.find_all('p')
    with open('data.txt','a',encoding='utf-8') as f:
      for i in texts:
        f.write(i.text)
        answer+=i.text
  return answer

@tool
def getLinks(question:str)->str:
    """Searches the internet for relevant content based on the question"""
    # print("question : ",question)
    # params = {
    #   "engine": "google_light",
    #   "q": question,
    #   "hl": "en",
    #   "gl": "in",
    #   "api_key": os.getenv('SERP')
    # }
    # search = GoogleSearch(params)
    # results = search.get_dict()
    arr=[]
    with DDGS() as ddgs:
      results = ddgs.text(question, max_results=3)
      for r in results:
          arr.append(r['href'])

    # # print(results)
    # with open('sampleLinks.txt','w') as f:
    #   f.write(str(results['organic_results']))
    return getText(arr)
      
      
# question="companies that are related to ai in mental health"
# print(getLinks(question))


# from duckduckgo_search import DDGS

# create a search client


from serpapi import GoogleSearch
import os
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup
from langchain_core.tools import tool
load_dotenv()


def getText(results)->str:
  answer=""
  count=0
  for i in results:
    if count==3:
      break
    count+=1
    # link="https://www.grandviewresearch.com/industry-analysis/ai-mental-health-market-report"
    link=i['link']
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
    """Searches the internet for relevant financial content based on the question"""
    print("question : ",question)
    params = {
      "engine": "google_light",
      "q": question,
      "hl": "en",
      "gl": "in",
      "api_key": os.getenv('SERP')
    }
    search = GoogleSearch(params)
    results = search.get_dict()

    # # print(results)
    # with open('sampleLinks.txt','w') as f:
    #   f.write(str(results['organic_results']))
    return getText(results['organic_results'])
      
      
# question="companies that are related to ai in mental health"
# getLinks(question)
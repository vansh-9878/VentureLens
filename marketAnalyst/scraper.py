from serpapi import GoogleSearch
import os
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup
load_dotenv()

def getLinks():
    question="market trends of ai in mental health"

    params = {
  "engine": "google_light",
  "q": question,
  "hl": "en",
  "gl": "in",
  "api_key": os.getenv('SERP')
}

    search = GoogleSearch(params)
    results = search.get_dict()

# print(results)

    with open('sampleLinks.txt','w') as f:
      f.write(str(results['organic_results']))


link="https://www.grandviewresearch.com/industry-analysis/ai-mental-health-market-report"
response=requests.get(link)
sp=BeautifulSoup(response.text,'html.parser')
texts=sp.find_all('p')

# for i in texts:
#   print(i.text)
  
with open('data.txt','w') as f:
  for i in texts:
    f.write(i.text)

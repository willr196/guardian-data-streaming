import os
import requests
from typing import List, Dict, Optional




def get_guardian_article(q:str, date_from: Optional[str] = None, api_key: Optional[str] = None, page_size: int=10) -> List[Dict]:
    URL = "https://content.guardianapis.com/search"
    parameters = {"q": q,
                 "order-by": "newest",
                 "page-size": page_size,
                 "api-key": api_key}
    
    if date_from:
        parameters["from-date"] = date_from

    resp = requests.get(URL, params=parameters)
    if resp.status_code != 200:
        raise Exception
    
    data = resp.json()
    results = data["response"]["results"]

    extracted = []

    for item in results:
        extracted.append({"webPublicationDate": item["webPublicationDate"],
        "webTitle":           item["webTitle"],
        "webUrl":             item["webUrl"]})

    return extracted 

articles = get_guardian_article("cliamte", api_key="")


for article in articles:
    print(f"{article['webTitle']} ({article['webPublicationDate']})")


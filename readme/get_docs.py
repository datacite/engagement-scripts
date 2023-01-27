import requests
import csv
import json
import os
from dotenv import load_dotenv
from datetime import datetime

def get_categories(apikey):
    response = requests.get("https://dash.readme.com/api/v1/categories", auth=(apikey, ""))
    return response.json()

def get_docs_for_category(apikey, slug):
    response = requests.get("https://dash.readme.com/api/v1/categories/{}/docs".format(slug), auth=(apikey, ""))
    return response.json()

def get_doc(apikey, slug):
    response = requests.get("https://dash.readme.com/api/v1/docs/{}".format(slug), auth=(apikey, ""))
    doc = response.json()
    return doc

def get_docs():
    load_dotenv()
    apikey = os.getenv("APIKEY")
    docs_by_category = get_categories(apikey)
    for category in docs_by_category:
        print("**** Category: {} ****".format(category["title"]))
        category_docs = get_docs_for_category(apikey, category["slug"])
        category["docs"] = category_docs
        for doc in category_docs:
            print("Doc: {}".format(doc["title"]))
            doc_details = get_doc(apikey, doc["slug"])
            doc["details"] = doc_details
            if "children" in doc and len(doc["children"]) > 0:
                for child_doc in doc["children"]:
                    print("Child doc: {}".format(child_doc["title"]))
                    child_doc_details =  get_doc(apikey, child_doc["slug"])
                    child_doc["details"] = child_doc_details

    # write json data to file
    # current time
    ct = datetime.now().strftime("%Y%m%d%H%M%S")
    f = open("{}_readme_docs.json".format(ct), "w")
    f.write(json.dumps(docs_by_category))
    f.close()

if __name__ == '__main__':
    get_docs()

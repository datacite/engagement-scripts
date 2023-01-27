import requests
import csv
import json
import os
from dotenv import load_dotenv
from datetime import datetime


def get_categories(apikey):
    response = requests.get("https://dash.readme.com/api/v1/categories?perPage=100", auth=(apikey, ""))
    return response.json()


def get_docs_for_category(apikey, slug):
    response = requests.get("https://dash.readme.com/api/v1/categories/{}/docs".format(slug), auth=(apikey, ""))
    return response.json()


def get_doc(apikey, slug):
    response = requests.get("https://dash.readme.com/api/v1/docs/{}".format(slug), auth=(apikey, ""))
    doc = response.json()
    return doc


def get_docs():
    """Get docs from the ReadMe API"""

    load_dotenv()
    apikey = os.getenv("APIKEY")
    unsorted_docs_by_category = get_categories(apikey)

    # Sort the list of categories by order
    docs_by_category = []
    i = 0
    while i < len(unsorted_docs_by_category):
        for j in unsorted_docs_by_category:
            if j["order"] == i:
                docs_by_category.append(j)
                break
        i += 1

    # For each category, get docs and child docs
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
                    child_doc_details = get_doc(apikey, child_doc["slug"])
                    child_doc["details"] = child_doc_details

    # current time
    ct = datetime.now().strftime("%Y%m%d%H%M%S")

    # write json data to file
    f = open("{}_readme_docs.json".format(ct), "w")
    f.write(json.dumps(docs_by_category))
    f.close()

    return docs_by_category


def get_doc_row(doc, category, parent_doc=""):
    """Structure doc information for single row"""
    doc_row = {i: doc[i] for i in doc if i != "details" and i != "children"}
    doc_row["categoryName"] = category["title"]
    if parent_doc:
        doc_row["parentDocName"] = parent_doc["title"]

    # Add sortIds
    if parent_doc:
        doc_row["sortId"] = "#{:02d}.{:02d}.{:02d}".format(category["order"], parent_doc["order"], doc["order"])
    else:
        doc_row["sortId"] = "#{:02d}.{:02d}".format(category["order"], doc["order"])

    # Add sub-properties of details to row
    for i in doc["details"]:
        if i not in ["body", "body_html"]:
            doc_row[i] = doc["details"][i]
    return doc_row


def output_docs_csv(docs_by_category):
    """Output docs as CSV file"""
    with open("readme_docs.csv", "w") as csvout:
        header = ['type', 'sortId', 'title', 'categoryName', 'parentDocName', 'slug', 'hidden', 'isReference', 'order',
                  'createdAt', 'updatedAt', 'link_external', 'link_url', 'reference', '_id', 'category', 'parentDoc',
                  '__v', 'from_sync', 'sync', 'version', 'deprecated', 'project', 'id', 'details',
                  'metadata', 'next', 'algolia', 'icon', 'updates', 'excerpt', 'sync_unique',
                  'previousSlug', 'slugUpdatedAt', 'revision', 'pendingAlgoliaPublish',
                  'user', 'isApi', 'githubsync', 'swagger',
                  'isAPI', 'apiSetting', 'api']
        writer = csv.DictWriter(csvout, fieldnames=header)
        writer.writeheader()

        for category in docs_by_category:
            category_row = {i: category[i] for i in category if i != "docs"}
            category_row["categoryName"] = category["title"]
            category_row["sortId"] = "#{:02d}".format(category["order"])
            writer.writerow(category_row)

            for doc in category["docs"]:
                doc_row = get_doc_row(doc, category)
                writer.writerow(doc_row)

                for child_doc in doc["children"]:
                    child_doc_row = get_doc_row(child_doc, category, doc)
                    writer.writerow(child_doc_row)


if __name__ == '__main__':
    load_dotenv()
    json_docs_file = os.getenv("JSON_DOCS")

    if json_docs_file:
        # If a JSON file from a previous run is specified, don't make new calls to ReadMe API
        with open(json_docs_file, 'r') as f:
            docs_by_category = json.load(f)
    else:
        # Fetch docs from ReadMe API and write to JSON file
        docs_by_category = get_docs()

    # Output docs as CSV file
    output_docs_csv(docs_by_category)

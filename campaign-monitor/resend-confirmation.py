import argparse
import json
from os import path
import requests
from requests.auth import HTTPBasicAuth

CM_API_ENDPOINT = "https://api.createsend.com/api/v3.2/"
SUBSCRIBERS_PATH = "subscribers/"
OUTPUT_DIR = "tmp/"

## Iterate over file containing unconfirmed users and re-add subscribers to list, triggering confirmation email
def add_subscribers(list_id, api_key, user, filename):
    url = CM_API_ENDPOINT + SUBSCRIBERS_PATH + list_id + ".json"
    with open(filename) as f:
        unconfirmed_subscribers = json.load(f)
        for item in unconfirmed_subscribers["Results"]:
            print("Resending to " + item['EmailAddress'])
            subscriber_dict= {
                "EmailAddress": (item['EmailAddress']),
                "ConsentToTrack":"Unchanged",
                "Resubscribe": True,
                "RestartSubscriptionBasedAutoresponders": True
            }
            subscriber_as_json_string = json.dumps(subscriber_dict)

            headers = {
                "accept": "application/json",
                "content-type": "application/json"
            }
            response = requests.request("POST", url, auth = HTTPBasicAuth(api_key, user), headers=headers, data=subscriber_as_json_string)
            response_json = response.json()
            print(response_json)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--list_id', type=str)
    parser.add_argument('-k', '--api_key', type=str)
    parser.add_argument('-u', '--user', type=str)
    parser.add_argument('-f', '--filename', type=str)
    args = parser.parse_args()
    file_path = OUTPUT_DIR + args.filename
    if path.exists(file_path):
        add_unconfirmed_subscribers = add_subscribers(args.list_id, args.api_key, args.user, file_path)
    else:
        print("File " + file_path + " does not exist. Cannot add subscribers.")

if __name__ == '__main__':
  main()
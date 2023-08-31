import argparse
import json
import math
import os.path
from os import path
import requests
from requests.auth import HTTPBasicAuth

CM_API_ENDPOINT = "https://api.createsend.com/api/v3.2/"
LISTS_PATH = "lists/"
BATCH_SIZE = 100.0
TECHNICAL = "Technical"
SERVICE = "Service"
OUTPUT_DIR = "tmp/"

## Get unconfirmed subscribers for a given Campaign Monitor list and save as file
def get_subscribers(list_id, api_key, user, filename, subscriber_type):
    url = CM_API_ENDPOINT + LISTS_PATH + list_id + "/" + subscriber_type + ".json"
    try:
        with open(filename, 'w') as f:
            headers = {
                "accept": "application/json",

            }
            response = requests.request("GET", url, auth = HTTPBasicAuth(api_key, user), headers=headers)
            response_json = response.json()
            json.dump(response_json, f)
    except:
        print("Error fetching subscribers")

## Process unconfirmed subscribers file into batches of 100
def process_file(filename, excludeBillingVoting, memberType, email):
     with open(filename) as f:
        json_data = json.load(f)
        unconfirmed_subscribers = json_data['Results']

        filtered_subscribers = []

        for subscriber in unconfirmed_subscribers:
            subscriber_roles = []
            subscriber_member_type = ""
            include_subscriber = True
            for field in subscriber['CustomFields']:
                if field['Key'] == '[Type]':
                    subscriber_roles.append(field['Value'])
                if field['Key'] == '[MemberType]':
                    subscriber_member_type = field['Value']
                    
            if excludeBillingVoting == True:
                # Exclude subscribers with only billing or voting roles if arg is set
                if len(subscriber_roles)==0 or any(TECHNICAL in s for s in subscriber_roles) or any(SERVICE in s for s in subscriber_roles):
                    include_subscriber = True
                else:
                    include_subscriber = False
            if memberType:
                # Exclude subscribers that are not the requested member type
                if include_subscriber == True and subscriber_member_type != memberType:
                    include_subscriber = False
            if email and subscriber["EmailAddress"] != email:
                # Exclude subscribers other than the specific email address requested
                include_subscriber = False

            if include_subscriber == True:
                filtered_subscribers.append(subscriber)
                
        if not excludeBillingVoting and not memberType and not email:
            filtered_subscribers = unconfirmed_subscribers

        filtered_subscribers_len = len(filtered_subscribers)

        # determine number of files necessary
        num_files = int(math.ceil(filtered_subscribers_len/BATCH_SIZE))
        print(str(filtered_subscribers_len) + ' subscriber(s) retrieved')
        print('File will be split into ' + str(num_files) + ' equal parts')

        split_data = [[] for i in range(0,num_files)]
        starts = [int(math.floor(i * filtered_subscribers_len /num_files)) for i in range(0,num_files)]
        starts.append(filtered_subscribers_len)

       # Build and save each file
        for i in range(0,num_files):
            for n in range(starts[i],starts[i+1]):
               split_data[i].append(filtered_subscribers[n])
            name = OUTPUT_DIR + os.path.basename(filename).split('.')[0] + '_' + str(i+1) + '.json'
            with open(name, 'w') as outfile:
               json.dump(split_data[i], outfile)
            print('Part ' + str(i+1) + ' completed')

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--list_id', type=str)
    parser.add_argument('-k', '--api_key', type=str)
    parser.add_argument('-u', '--user', type=str)
    parser.add_argument('-f', '--filename', type=str)
    parser.add_argument('-s', '--subscriber_type', type=str, choices=['active', 'unconfirmed', 'unsubscribed', 'bounced', 'deleted'])
    parser.add_argument('-x', '--exclude_billing_voting', action='store_true')
    parser.add_argument('-m', '--member_type', type=str)
    parser.add_argument('-e', '--email', type=str)
    args = parser.parse_args()
    file_path = OUTPUT_DIR + args.filename
    subscribers = get_subscribers(args.list_id, args.api_key, args.user, file_path, args.subscriber_type)
    if path.exists(file_path):
        process_file(file_path, args.exclude_billing_voting, args.member_type, args.email)
    else:
        print("File " + file_path + " does not exist. Cannot process subscribers.")

if __name__ == '__main__':
  main()
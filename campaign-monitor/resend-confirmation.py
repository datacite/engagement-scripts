import argparse
import pycurl
import json
from cStringIO import StringIO
import os.path
from os import path

CM_API_ENDPOINT = "https://api.createsend.com/api/v3.2/"
SUBSCRIBERS_PATH = "subscribers/"
LISTS_PATH = "lists/"

def get_subscribers(list_id, api_key, filename):
    url = CM_API_ENDPOINT + LISTS_PATH + list_id + "/unconfirmed.json"
    try:
        with open(filename, 'w') as f:
            c = pycurl.Curl()
            c.setopt(pycurl.URL, url)
            c.setopt(pycurl.HTTPHEADER, ['Accept: application/json'])
            c.setopt(pycurl.USERPWD, '%s:%s' %(api_key, 'x'))
            c.setopt(c.WRITEDATA, f)
            c.perform()
            c.close()
    except:
        print "Error fetching subscribers"

def add_subscribers(list_id, api_key, filename):
    url = CM_API_ENDPOINT + SUBSCRIBERS_PATH + list_id + ".json"
    with open(filename) as f:
        unconfirmed_subscribers = json.load(f)
        for item in unconfirmed_subscribers['Results']:
            print("Resending to " + item['EmailAddress'])
            subscriber_dict= {
                "EmailAddress": (item['EmailAddress']),
                "ConsentToTrack":"Unchanged",
                "Resubscribe": True,
                "RestartSubscriptionBasedAutoresponders": True
            }
            subscriber_as_json_string = json.dumps(subscriber_dict)
            subscriber_as_file_object = StringIO(subscriber_as_json_string)

            c = pycurl.Curl()
            c.setopt(pycurl.URL, url)
            c.setopt(pycurl.HTTPHEADER, ['Accept: application/json',
                                            'Content-Type: application/json'])
            c.setopt(pycurl.USERPWD, '%s:%s' %(api_key, 'x'))
            c.setopt(pycurl.POST, 1)
            c.setopt(pycurl.READDATA, subscriber_as_file_object)
            c.setopt(pycurl.POSTFIELDSIZE, len(subscriber_as_json_string))
            response = c.perform_rs()
            print "Response: " + response
            c.close()

#MAIN FUNCTION
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--list_id', type=str)
    parser.add_argument('-k', '--api_key', type=str)
    parser.add_argument('-u', '--user', type=str)
    parser.add_argument('-f', '--filename', type=str)
    args = parser.parse_args()
    get_unconfirmed_subscribers = get_subscribers(args.list_id, args.api_key, args.filename)
    if path.exists(args.filename):
        add_unconfirmed_subscribers = add_subscribers(args.list_id, args.api_key, args.filename)
    else:
        print "File " + args.filename + " was not created. Cannot add subscribers."

if __name__ == '__main__':
  main()
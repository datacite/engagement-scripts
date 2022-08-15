# Campaign Monitor scripts

## Prerequisites

- [Install and configure Python](https://wiki.python.org/moin/BeginnersGuide/Download) on your machine

## Get subscribers

This script retrieves the list of subscribers in a specified state (unconfirmed, unsubscribed, etc) for a specified Campaign Monitor list and splits it files with max 100 subscribers each. Optionally, it can exclude subscribers with only billing or voting roles.

### Usage

    python get-subscribers.py --list_id "[CAMPAIGN MONITOR LIST ID]" --api_key "[CAMPAIGN MONITOR API KEY]" --user "x"  --filename "unconfirmed.json" --exclude_billing_voting --subscriber_type "unconfirmed"

- **list_id:** Find the Campaign Monitor list ID in the list settings (at the bottom of the page), ex https://lists.datacite.org/audience/5ac63db5700ec107/lists/F8091AA5A2563B31/settings?origin=&originId=
- **api_key:** Find the Campaign Monitor API key in the Campaign Monitor account settings https://lists.datacite.org/account/apikeys
- **user:** Always "x" (Campaign Monitor API does not use different usernames for each account)
- **filename:** Name of the file you'd like to add the list of unconfirmed subscribers to, including .json extension, ex "unconfirmed.json"
- **exclude_billing_voting:** If this argument is present, subscribers with only billing or voting roles are excluded from the resulting files
- **subscriber_type:** Must be one of: active, unconfirmed, unsubscribed, bounced or deleted

## Resend confirmation

This script retrieves the list of unconfirmed subscribers for a specified Campaign Monitor list and re-adds those subscribers, triggering a new confirmation email.

### Usage

    python resend-confirmation.py --list_id "[CAMPAIGN MONITOR LIST ID]" --api_key "[CAMPAIGN MONITOR API KEY]" --user "x"  --filename "unconfirmed.json"

- **list_id:** Find the Campaign Monitor list ID in the list settings (at the bottom of the page), ex https://lists.datacite.org/audience/5ac63db5700ec107/lists/F8091AA5A2563B31/settings?origin=&originId=
- **api_key:** Find the Campaign Monitor API key in the Campaign Monitor account settings https://lists.datacite.org/account/apikeys
- **user:** Always "x" (Campaign Monitor API does not use different usernames for each account)
- **filename:** Name of the file you'd like to add the list of unconfirmed subscribers to, including .json extension, ex "unconfirmed.json"

## Resend confirmation to a single subscriber
To resend a confirmation message to a single user, you can use the Campaign Monitor API directly:

1. Create a JSON file with the following data. See [example_subscriber.json](https://github.com/datacite/engagement-scripts/blob/main/campaign-monitor/example_subscriber.json)

        {
            "EmailAddress": "user@example.org",
            "Resubscribe": true,
            "RestartSubscriptionBasedAutoresponders": true,
            "ConsentToTrack":"No"
        }
        
2. Resend the confirmation email using the file you created.

        curl -X POST -H "Content-Type: application/json" -u "[CAMPAIGN MONITOR API KEY]:x"  -d @/YOUR_FILE_PATH/example_subscriber.json https://api.createsend.com/api/v3.2/subscribers/[CAMPAIGN MONITOR LIST ID].json?pretty=true

- **list_id:** Find the Campaign Monitor list ID in the list settings (at the bottom of the page), ex https://lists.datacite.org/audience/5ac63db5700ec107/lists/F8091AA5A2563B31/settings?origin=&originId=
- **api_key:** Find the Campaign Monitor API key in the Campaign Monitor account settings https://lists.datacite.org/account/apikeys
user: Always "x" (Campaign Monitor API does not use different usernames for each account)


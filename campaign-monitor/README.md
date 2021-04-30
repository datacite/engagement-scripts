# Campaign Monitor scripts

## Prerequisites

- [Install and configure Python](https://wiki.python.org/moin/BeginnersGuide/Download) on your machine

## Get unconfirmed subscribers

This script retrieves the list of unconfirmed subscribers for a specified Campaign Monitor list and splits it files with max 100 subscribers each. Optionally, it can exclude subscribers with only billing or voting roles.

### Usage

    python get-unconfirmed-subscribers.py --list_id "[CAMPAIGN MONITOR LIST ID]" --api_key "[CAMPAIGN MONITOR API KEY]" --user "x"  --filename "unconfirmed.json" -exclude-billing-voting

- **list_id:** Find the Campaign Monitor list ID in the list settings (at the bottom of the page), ex https://lists.datacite.org/audience/5ac63db5700ec107/lists/F8091AA5A2563B31/settings?origin=&originId=
- **api_key:** Find the Campaign Monitor API key in the Campaign Monitor account settings https://lists.datacite.org/account/apikeys
- **user:** Always "x" (Campaign Monitor API does not use different usernames for each account)
- **filename:** Name of the file you'd like to add the list of unconfirmed subscribers to, including .json extension, ex "unconfirmed.json"
- **exclude-billing-voting:** If this argument is present, subscribers with only billing or voting roles are excluded from the resulting files

## Resend confirmation

This script retrieves the list of unconfirmed subscribers for a specified Campaign Monitor list and re-adds those subscribers, triggering a new confirmation email.

### Usage

    python resend-confirmation.py --list_id "[CAMPAIGN MONITOR LIST ID]" --api_key "[CAMPAIGN MONITOR API KEY]" --user "x"  --filename "unconfirmed.json"

- **list_id:** Find the Campaign Monitor list ID in the list settings (at the bottom of the page), ex https://lists.datacite.org/audience/5ac63db5700ec107/lists/F8091AA5A2563B31/settings?origin=&originId=
- **api_key:** Find the Campaign Monitor API key in the Campaign Monitor account settings https://lists.datacite.org/account/apikeys
- **user:** Always "x" (Campaign Monitor API does not use different usernames for each account)
- **filename:** Name of the file you'd like to add the list of unconfirmed subscribers to, including .json extension, ex "unconfirmed.json"

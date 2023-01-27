# ReadMe scripts

## get_docs.py

This script retrieves the categories and docs from ReadMe and outputs the information into JSON and CSV files.

### Set up .env file

Create a `.env` file in this directory 

To retrieve docs from ReadMe, an API is required. Add this line to the .env file:

`APIKEY=<apikey>`

replacing `<apikey>` a key retrieved from https://dash.readme.com/project/datacite/v1.4/api-key.

If you have already run the script and want to re-generate the CSV file, you can also specify a JSON file to be used, for example:

`JSON_DOCS=20230127083848_readme_docs.json`

### Usage
`python get_docs.py`

### Outputs

- `<timestamp>_readme_docs.json`: A JSON file with the compiled results of the API requests
- `readme_docs.csv`: A CSV file containing all info from the JSON file except the body of each document (to save space)

To update the order of the columns in the CSV file, modify the order of the items in the `"header"` list in the `output_docs_csv()` function.

## Import to Google Sheets
### Filters to apply:
- type = basic, guide, link
- hidden = (Blanks), FALSE
- isReference = (Blanks), FALSE
### Conditional formatting custom formulas:
- Highlight category names: =$A2="guide"
- Highlight docs with children: =ISBLANK($E2)
- Highlight docs wtihout children: =NOT(ISBLANK($E2))
import requests
import pprint
import csv

def get_longest_definition(data):
    longest_definition = ""
    for item in data:
        if 'definition' in item:
            definition = item['definition'][0]
            if len(definition) > len(longest_definition):
                longest_definition = definition
    return longest_definition
    
def get_definition(term):
    API_KEY = "ecf5cb86-f81a-4475-bce2-c921ad8e317e"
    API_ENDPOINT = "http://data.bioontology.org/search?q="

    headers = {
        "Authorization": "apikey token=" + API_KEY
    }

    response = requests.get(API_ENDPOINT + term, headers=headers)

    if response.status_code == 200:
        data = response.json()
        results = data.get("collection", [])
        return(get_longest_definition(results))
    else:
        return "An error occurred while trying to retrieve the definition."

'''
# Open the CSV file
with open('data.csv', 'r') as file:
    # Create a DictReader object
    reader = csv.DictReader(file)
    
    # Convert the CSV data into a list of dictionaries
    data = list(reader)
'''

term = ("tt")
definition = get_definition("covid")
pprint.pprint(str(definition))
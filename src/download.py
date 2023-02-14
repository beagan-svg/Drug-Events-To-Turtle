import requests
import os
import json
import pprint
# Define the URL of the JSON file
url = 'https://api.fda.gov/download.json'

# Send a GET request to the URL
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Convert the response to a string
    data = response.text

    # Parse the string into a JSON object
    data = json.loads(data)

    # Extract the links from the JSON object
    links = []
    
    for file_dict in data['results']['drug']['event']['partitions']:
        links.append(file_dict['file'])
    #links.append(data['results']['drug']['event'])

    # Create a directory to store the downloaded files
    directory = 'downloads'
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Loop through the links
    for link in links:
        # Send a GET request to the link
        link_response = requests.get(link)

        # Check if the request was successful
        if link_response.status_code == 200:
            # Extract the filename from the link
            filename = os.path.basename(link)

            # Write the contents of the link to a file in the directory with the extracted filename
            file_path = os.path.join(directory, filename)
            with open(file_path, 'wb') as file:
                file.write(link_response.content)
        else:
            # Print an error message if the request was not successful
            print('Failed to download link:', link)
else:
    # Print an error message if the request was not successful
    print('Failed to retrieve data from URL:', url)

Drug-Events-To-Turtle
=================================================
![cover](Image/network.png)

## About Drug-Events-To-Turtle
OpenFDA is a platform created by the United States Food and Drug Administration (FDA) to make publicly available data more accessible to the public. This includes data on drug adverse events, product recalls, and more. FAERS is a database of adverse event and medication error reports submitted to the FDA. The information in FAERS is used by the FDA to monitor drug safety, and detect and understand new safety concerns. The scripts in this repository will incorporate information from OpenFDA's FAERS API into a turtle file and import it into neo4j.

Table of Contents
-----------------
* [Usage](#usage)
* [Describe Script](#Describe)
* [Authors and history](#authors-and-history)
* [Acknowledgments](#acknowledgments)
* [References](#references)

## Usage
1. Clone the repository
```bash
git clone 'https://github.com/beagan-svg/Drug-Events-To-Turtle'
```
2. Install the necessary Python packages using these commands
```bash
import requests
import os
import json
import pandas as pd
import pprint
import os
import pickle5 as pickle
import string
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import spacy
import numpy as np
from scipy.sparse import hstack
```

3. Run the Script.
```bash
python3 <File Name>
``` 

# Describe
1. src/download.py
This script is a Python program that downloads data from the FDA's open API located at the URL 'https://api.fda.gov/download.json'. The program uses the requests library to send a GET request to the URL and retrieve the data. It then parses the data into a JSON object and extracts the links to the desired data files. The program then creates a directory named 'downloads' to store the downloaded files, if the directory doesn't already exist. The program then loops through the links and sends a GET request to each link to retrieve the data. If the request is successful, the data is saved to a file in the 'downloads' directory with the name extracted from the link. If the request is unsuccessful, an error message is printed.

2. src/gen_ttl.py
This script creates a Turtle RDF file for a specific drug, in this case, "clonidine", with information about its pharmacological class (EPC), categories of benefits, and terms indicating the drug's indications. The data is stored in a dictionary "result_dict" with categories as keys and lists of terms as values. The script creates the prefixes for the file and then writes the information about the drug, EPC, categories, and terms to the file, using Turtle RDF syntax. It replaces spaces in the names with underscores and removes apostrophes from the terms. The file is saved with the name of the drug and the ".ttl" extension.

3. src/parse_json.py
This script performs pre-processing on a dataset containing information about adverse reactions to drugs. The data is stored in multiple .json files located in the "downloads" directory. The script first reads all .json files in the directory and stores the information into a dictionary called "active_dict."

Each entry in the "active_dict" dictionary consists of the active substance of a drug and a list of three items: reactionmeddrapt, pharm_class_epc, and drugindication. Reactionmeddrapt is a list of adverse reactions to the drug, pharm_class_epc is a list of its pharmacological class, and drugindication is a list of the indications for which the drug is used.

The script performs some pre-processing on the drugindication field, including converting the text to lowercase, removing punctuation, and removing stop words. This pre-processed text is then stored in the "active_dict" dictionary.

Finally, the script converts the "active_dict" dictionary into a pandas dataframe and saves it as a .csv file. The resulting dataframe has three columns, corresponding to the three items stored in each entry of the "active_dict" dictionary.

4. src/Predict Category # Folders containing scripts to build the categorization model
A. get_definition.py 
This script retrieves the definition of a term from the BioPortal API using the requests library in Python.

The get_longest_definition function takes in a list of dictionaries, each representing a search result from the API, and returns the definition with the longest length. The get_definition function takes in a term as an argument, makes a GET request to the BioPortal API with the given term as the query, and returns the longest definition returned from the API.
B. predict_categorize.py
This script is a machine learning model that categorizes medical terms into different categories. The model uses a combination of term and definition vectors to predict the category of a medical term. The data used to train and test the model is loaded from a CSV file "medical_terms.csv", which contains the medical terms, definitions, and categories. The data is split into training and test sets using the train_test_split function from the scikit-learn library.

The definitions are converted into vector representations using the spaCy library and the en_core_sci_sm model. The term and definition vectors are concatenated and used as input features for the categorization model. The model is implemented using a pipeline consisting of a TfidfVectorizer and a LinearSVC classifier. The model is trained on the training data and evaluated on the test data using the classification_report function from the scikit-learn library.

Finally, the script demonstrates how to use the trained model to categorize a new medical term and definition. The new term and definition are converted into vectors and passed as input to the trained model, which outputs the predicted category of the new term.

## Authors and History

* Beagan Nguy - Algorithm Design

## Acknowledgments

BrightSeed



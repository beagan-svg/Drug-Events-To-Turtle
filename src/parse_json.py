import json
import pandas as pd
import pprint
import os
import pickle5 as pickle
import string
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

def preprocess(text):
    # Convert text to lowercase
    text = text.lower()
    # Remove punctuation
    text = text.translate(str.maketrans("", "", string.punctuation))
    # Tokenize the text
    tokens = word_tokenize(text)
    # Remove stop words
    stop_words = set(stopwords.words("english"))
    tokens = [token for token in tokens if not token in stop_words]
    # Join the tokens back into a single string
    text = " ".join(tokens)
    return text

directory = '/allen/programs/celltypes/workgroups/rnaseqanalysis/bnguy/Projects/FAERS/downloads'
json_files = []

for filename in os.listdir(directory):
    if filename.endswith(".json"):
        json_files.append(os.path.join(directory, filename))

# List to string function
def list_to_string(lst):
    if isinstance(lst, list):
        return ", ".join(lst)
    return lst

# Dictionary: Key = Active Compound, Value = [reaction_list, mechanism_list, target_list] ('reactionmeddrapt', "pharm_class_epc", 'drugindication')
active_dict = dict()

for files in json_files: 
    # Load the JSON data from the file into a Python object
    with open(files, 'r') as file:
        data = json.load(file)

    # Use the data in your Python code
    for result_data in data['results']:
        for result_key, result_value in result_data.items(): 
            if result_key == 'patient':
                for patient_key, patient_list in result_value.items():
                    if patient_key == "drug":
                        for patient_dict in patient_list:
                            for drug_key, drug_value in patient_dict.items():
                                if drug_key == "activesubstance":
                                    compound = drug_value["activesubstancename"]
                                    reactionmeddrapt = result_value['reaction'][0]['reactionmeddrapt']
                                    print(reactionmeddrapt)
                                    print(compound)
                                    print("====")
                                    
                                    if compound not in active_dict:
                                        active_dict[list_to_string(compound)] = [list(), list(), list()]
                                    
                                    if list_to_string(reactionmeddrapt) not in active_dict[list_to_string(compound)][0]:
                                        active_dict[list_to_string(compound)][0].append(list_to_string(reactionmeddrapt))
                                    
                                    if 'drugindication' in patient_dict.keys():
                                        if patient_dict['drugindication'] != "Product used for unknown indication":
                                            druguse = list_to_string(patient_dict['drugindication'])
                                            tkndruguse = preprocess(druguse)
                                            if tkndruguse not in active_dict[list_to_string(compound)][2]:
                                                active_dict[compound][2].append(list_to_string(tkndruguse))

                                    if "openfda" in patient_dict:
                                        if "pharm_class_epc" in patient_dict["openfda"]:
                                            #print(patient_dict["openfda"]["pharm_class_epc"])
                                            if list_to_string(patient_dict["openfda"]["pharm_class_epc"]) not in active_dict[list_to_string(compound)][1]:
                                                active_dict[compound][1].append(list_to_string(patient_dict["openfda"]["pharm_class_epc"]))
                                

def dict_to_df(d):
    unlisted = {key: [','.join(map(str, inner_list)) for inner_list in value] for key, value in d.items()}
    df = pd.DataFrame.from_dict(unlisted, orient='index')
    df.columns = [f'column{i+1}' for i in range(df.shape[1])]
    return df

df = dict_to_df(active_dict)
df.columns = ['reactionmeddrapt', "pharm_class_epc", 'drugindication']

# Save the data frame as a pickle object
#df.to_pickle('faers_df.pkl')

#df.to_csv('data.csv', index=True)


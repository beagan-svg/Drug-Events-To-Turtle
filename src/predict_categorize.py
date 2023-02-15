import nltk
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import spacy
import numpy as np
from scipy.sparse import hstack

# Load the medical terms, definitions, and their categories
data = pd.read_csv("medical_terms.csv")
print(data)

# Split the data into training and test sets
X_train_terms, X_test_terms, X_train_defs, X_test_defs, y_train, y_test = train_test_split(data["term"], data["definition"], data["category"], test_size=0.2, random_state=42)
print("---------")
print(X_train_defs)
print("====")
print(X_test_defs)
print("---------")
# Use the en_core_sci_sm model to obtain vector representations of the definitions
def get_definition_vectors(definitions):
    nlp = spacy.load('en_core_sci_sm')
    vectors = []
    for definition in definitions:
        doc = nlp(definition)
        vector = doc.vector
        vectors.append(vector)
    return vectors

X_train_def_vectors = get_definition_vectors(X_train_defs)
X_test_def_vectors = get_definition_vectors(X_test_defs)

# Concatenate the term and definition vectors as input features
X_train = [f"{term} {def_vec}" for term, def_vec in zip(X_train_terms, X_train_def_vectors)]
X_test = [f"{term} {def_vec}" for term, def_vec in zip(X_test_terms, X_test_def_vectors)]

print(X_train)

# Define the pipeline for the categorization model
pipeline = Pipeline([
    ('vectorizer', TfidfVectorizer(stop_words='english')),
    ('classifier', LinearSVC())
])

# Train the model on the training data
pipeline.fit(X_train, y_train)

# Evaluate the model on the test data
y_pred = pipeline.predict(X_test)
print(classification_report(y_test, y_pred))

# Categorize a new medical term and definition
new_term = ["Blood cholesterol"]
new_def = "A type of fat that is found in the blood"
new_term_vector = pipeline.named_steps['vectorizer'].transform(new_term)
new_def_vector = get_definition_vectors([new_def])[0]
new_input = [f"{new_term[0]} {new_def_vector}"]
new_category = pipeline.predict(new_input)[0]
print("The new term is categorized as:", new_category)

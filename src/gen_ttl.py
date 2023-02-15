import pprint

# Edit Here
string = "Hypertension and Blood Pressure Abnormalities:sleep disorder,dystonia,labile blood pressure,blood pressure abnormal,hypertension,prophylaxis,epilepsy,flushing,tourettes disorder,drug use disorder,anaesthesia,psychomotor hyperactivity,posterior reversible encephalopathy syndrome,Generalised anxiety disorder,alcohol withdrawal syndrome,drug withdrawal syndrome,postural orthostatic tachycardia syndrome,somatotropin stimulation test,iron deficiency,sedation,eczema,tachycardia,disturbance attention,withdrawal syndrome,pain management,proctalgia,sedative therapy,behaviour disorder,analgesic therapy,attention deficit hyperactivity disorder,complex regional pain syndrome,pain,orthostatic intolerance,blood pressure systolic increased,paroxysmal sympathetic hyperactivity,hot flush,charge syndrome,blood pressure measurement,anxiety,induction anaesthesia,intellectual disability,autism spectrum disorder,panic attack,aggression,agitation,depressive symptom,blood pressure management,insomnia,depression,blood pressure systolic,alcohol abuse,pulmonary arterial hypertension,nervous system disorder,autonomic nervous system imbalance,surgery,dyskinesia,hypertensive urgency,seizure,child abuse,pruritus,cerebellar ataxia,confusional state,irritable bowel syndrome,blood pressure increased,covid19 pneumonia,migraine,drug dependence,tic,product use unapproved indication,neck pain,back pain,musculoskeletal chest pain,erythromelalgia,drug abuse,dementia,evidence based treatment,cancer pain,heart rate increased/Therapy and Management:sleep disorder,anaesthesia,sedation,pain management,sedative therapy,behaviour disorder,analgesic therapy,pain,induction anaesthesia,surgery,anxiety,depression,alcohol abuse,drug dependence,product use unapproved indication,drug abuse,evidence based treatment,cancer pain/Cardiovascular Disorders:labile blood pressure,blood pressure abnormal,hypertension,epilepsy,flushing,tachycardia,withdrawal syndrome,proctalgia,hot flush,charge syndrome,blood pressure measurement,anxiety,intellectual disability,autism spectrum disorder,panic attack,aggression,agitation,depressive symptom,blood pressure management,alcohol abuse,pulmonary arterial hypertension,nervous system disorder,autonomic nervous system imbalance,seizure,cerebellar ataxia,confusional state,irritable bowel syndrome,blood pressure increased,covid19 pneumonia,migraine,tic,neck pain,back pain,musculoskeletal chest pain,erythromelalgia,dementia,heart rate increased/Blood Abnormalities:iron deficiency/Diabetes and Endocrine Disorders:somatotropin stimulation test/Respiratory Disorders:covid19 pneumonia/Arthritis and Joint Disorders:neck pain,back pain,musculoskeletal chest pain/Autoimmune Disorders:/Gastrointestinal Disorders:irritable bowel syndrome/Infections:covid19 pneumonia/Eye and Visual Disorders:/Neurological Disorders:epilepsy,tourettes disorder,psychomotor hyperactivity,posterior reversible encephalopathy syndrome,Generalised anxiety disorder,attention deficit hyperactivity disorder,nervous system disorder,cerebellar ataxia,confusional state,dementia/Skin Disorders:eczema,pruritus"
generic_term_list = ["Adverse Event", "Disease Complication", "product use unapproved indication", "drug abuse", "alcohol abuse"]


def parse_string_to_dict(string):
    categories_dict = {}
    categories = string.split("/")
    for category in categories:
        key_value = category.split(":")
        key = key_value[0].strip()
        value = key_value[1].strip().split(",")
        categories_dict[key] = value
    return categories_dict

'''
def parse_string(string):
    data = string.split("/")
    medical_conditions = {}
    for condition in data:
        if ":" in condition:
            key, values = condition.split(":")
            medical_conditions[key] = values.split(",")
    return medical_conditions
'''

#result_dict = parse_string(string)
result_dict = parse_string_to_dict(string)

# Edit Here 
drug_name = "clonidine"
epc_list = ["Central alpha-2 Adrenergic Agonist [EPC]"]

# Open a text file in write mode
file = open("{}.ttl".format(drug_name), "w")
'''
category_list = ["Therapy_and_Management", "Hypertension_and_Blood_Pressure_Abnormalities", 
                "Cardiovascular_Disorders", "Blood_Abnormalities", "Diabetes_and_Endocrine_Disorders",
                "Respiratory_Disorders", "Autoimmune_Disorders", "Gastrointestinal_Disorders",
                "Infections", "Neurological_Disorders", "Cancer", "Renal_Disorders",
                "Pain_and_Discomfort", "Immune_System_Disorders", "Vitamin_and_Nutritional_Disorders",
                "Blood_Cholesterol_and_Lipid_Disorders", "Adverse_Reactions_to_Drugs",
                "Miscellaneous_Disorders", "Pregnancy_and_Reproductive_Disorders"
                ]
'''
category_list = list(result_dict.keys())

# Prefix
file.write("@prefix {}: <http://neo4j.com/voc/{}#> .\n".format(drug_name, drug_name))
file.write("@prefix subs: <http://neo4j.com/voc/substance#> .\n")
file.write("@prefix term: <http://neo4j.com/voc/term#> .\n")
file.write("\n")

for epc in epc_list:
    file.write("{}:{} a {}:EPC ;\n".format(drug_name, epc.replace(" ", "_").replace('[', '').replace(']', ''), drug_name))
    file.write('\t{}:name "{}" ;\n'.format(drug_name, epc))
    file.write('\tsubs:is_an_attribute_of subs:{} .\n'.format(drug_name.title()))
    file.write("\n")

file.write("subs:{} a {}:Drug;\n".format(drug_name.title(), drug_name))
file.write('\t{}:name "{}" ;\n'.format(drug_name, drug_name.title()))
for index, category in enumerate(category_list):
    if index == len(category_list) -1:
        file.write("\t{}:benefit {}:{} .\n".format(drug_name, drug_name, category.replace(" ", "_")))
    else: 
        file.write("\t{}:benefit {}:{} ;\n".format(drug_name, drug_name, category.replace(" ", "_")))
file.write("\n")

for category in category_list:
    file.write("{}:{} a {}:Category ;\n".format(drug_name, category.replace(" ", "_"), drug_name))
    file.write('\t{}:name "{}" .\n'.format(drug_name, category.replace("_", " ")))
    file.write("\n")

for category, term_list in result_dict.items():
    for term in term_list:
        if term not in generic_term_list:
            term = term.replace("'", "")
            file.write('term:{} a {}:DrugIndication ;\n'.format(term.replace(" ", "_"), drug_name))
            file.write('\t term:name "{}" ;\n'.format(term))
            file.write('\t term:belonds_to_category {}:{} .\n'.format(drug_name, category.replace(" ", "_")))
            file.write("\n")
file.close()
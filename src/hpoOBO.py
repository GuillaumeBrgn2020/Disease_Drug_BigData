import obonet

def read_obo():
    """Reads hpo.obo
    """
    
    file = obonet.read_obo("bd/hpo.obo")
    c = 1
    cap = 10
    for node in file.nodes(data=True):
        if c > cap:
            break
        c = c + 1
        
#read_obo()

def get_synonyms(symptoms):
    """Reads hpo.obo. Gets the list of synonyms for symptoms.

    Args:
        symptoms : list of symptoms
        
    Returns:
        synonyms : list of synonyms for all the symptoms
    """
    graph = obonet.read_obo("bd/hpo.obo")

    symptoms = [symptoms]
    # Synonyms of all the symptoms in the input
    synonyms = [('', symptom) for symptom in symptoms]
    
    for id, data in graph.nodes(data=True):
        # Check for all the symptoms and get their synonyms
        if data["name"] in symptoms and "synonym" in data.keys():
            synonyms[0] = (id, symptoms[0])
            for synonym in data["synonym"]:
                # Get synonyms delimited by "
                s = synonym.split('"')[1]
                if s not in synonyms:
                    synonyms.append((id, s))

    return synonyms

# def extract_synonyms(syn_l):
#     """
#     Cleans the list of synonyms returned by HPO.
#     :param syn_l: List of synonyms as returned by HPO. Form : '"label" EXACT[]'
#     :return: List of synonyms with only the labels
#     """
#     # Creates a new list of synonyms with only the labels
#     syn_l_clean = []

#     for syn in syn_l:
#         # Looks for the limits of the synonym name (without 'EXACT', etc...) which are the double quotes
#         i = syn.index('"')
#         syn = syn[i + 1:]

#         i = syn.index('"')
#         syn_l_clean.append(syn[:i])

#     return syn_l_clean


# def get_synonyms(symptom_l):
#     """
#     Based on HPO. Gets the list of synonyms.
#     :param symptom_l: list of symptoms
#     :return: List of synonyms
#     """
#     HPO = obonet.read_obo("bd/hpo.obo")

#     # Initialize the list of synonyms with the symptoms themselves.
#     syn_l = []
#     for symptom in symptom_l:
#         syn_l = [[symptom], '0']

#     # Add synonyms in syn_l
#     for id, dict in HPO.nodes(data=True):
#         if dict["name"] in symptom_l:
#             syn_l[1] = id
#             if "synonym" in dict.keys():
#                 for syn in extract_synonyms(dict["synonym"]):
#                     if syn not in syn_l[0]:
#                         syn_l[0].append(syn)

#     return syn_l

            
#print(get_synonyms(["Bladder diverticulum"]))

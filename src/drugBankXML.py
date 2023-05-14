from xml.etree import ElementTree

from whoosh import index
from whoosh.fields import *
from whoosh.qparser import QueryParser
import os, os.path

def read_xml_file(file_path):
    """Reads xml file

    Args:
        file_path : path of xml file
    """
    xml = ElementTree.parse(file_path)
    root = xml.getroot()
    c = 1
    cap = 10

    for element in root.findall('{http://www.drugbank.ca}drug'):
        idDrug = element[0].text
        indication = element[11].text
        toxicity = element[14].text
        data = {"idDrug" : idDrug, "indication" : indication, "toxicity" : toxicity}
        
        
        if c > cap :
            break
        c = c + 1
        

#read_xml_file("bd/drugbank.xml")

def parse_xml_file(file_path):
    """Reads xml file

    Args:
        file_path : path of xml file to read

    Returns:
        list of dict : list of the drugs' id, indication and toxicity
    """
    # Parsing XML file
    xml = ElementTree.parse(file_path)
    
    # Getting the first element of the tree, eg the root
    root = xml.getroot()
    
    # Contains the list of all the drugs
    # Each element of the list is a dictionnary with the drug's data,
    # eg id, indication and toxicity
    Drugs = []

    # For each element of the tree, get id, indication and toxicity
    for element in root.findall('{http://www.drugbank.ca}drug'):
        idDrug = element[0].text
        indication = element[11].text
        toxicity = element[14].text

        data = {"idDrug" : idDrug, "indication" : indication, "toxicity" : toxicity}

        Drugs.append(data)

    return Drugs

def create_index_xml(file_path):
    """Read xml files. Creates an index (id, indication, toxicity) and only stores id.

    Args:
        file_path : path of xml file to read
    """
    
    # The directory that contains the index
    indexdir = "bd/drugBankIndex"
    
    # The schema of the index
    schema = Schema(id=ID(stored=True), indication=TEXT(), toxicity=TEXT(), atc=TEXT(stored=True))
    
    # if the directory does not exist, we create it
    if not os.path.exists(indexdir):
        os.mkdir(indexdir)
    
    # Creating the index in the directory "bd/indexdir"
    ix = index.create_in(indexdir, schema)
    
    # Opening the index
    ix = index.open_dir(indexdir)
    
    # Creating a writer to add documents
    writer = ix.writer()
    
    
    xml = ElementTree.parse(file_path)
    root = xml.getroot()
    for element in root.findall('{http://www.drugbank.ca}drug'):
        idDrug = element[0].text
        indication = element[11].text
        toxicity = element[14].text
        
        res = []
        for e in element.findall('{http://www.drugbank.ca}atc-codes'):
            for e2 in e.findall('{http://www.drugbank.ca}atc-code'):
                res.append(e2.attrib["code"])
                for e3 in e2.findall('{http://www.drugbank.ca}level'):
                    res.append(e3.attrib["code"])
        res = ';'.join(res)
        # Adding a document
        writer.add_document(id=idDrug, indication=indication, toxicity=toxicity, atc=res)

    # Closing and the writer
    writer.commit()

#create_index_xml("bd/drugbank.xml")

def search_index_xml(symptom):
    """Reads xml files. Search through the index for symptom in indication and toxicity

    Args:
        symptom : symptom input

    Returns:
        list: 
    """
    
    # The directory that contains the index
    indexdir = "bd/drugBankIndex"
        
    # Opening the index
    ix = index.open_dir(indexdir)
    
    # Creating parser for query
    parserIndication = QueryParser("indication", schema=ix.schema)
    parserToxicity = QueryParser("toxicity", schema=ix.schema)
    
    # Creating query
    queryIndication = parserIndication.parse(symptom)
    queryToxicity = parserToxicity.parse(symptom)
    
    I = []
    T = []
    
    # Searching content corresponding to the query
    with ix.searcher() as searcher:
        
        # Getting results for indication
        resultsIndication = searcher.search(queryIndication, limit=None)
        
        for result in resultsIndication:
            if result.get('atc'):
                I.append((result["id"], result["atc"].split(";")))
            else:
                I.append((result["id"], None))
                
        
        # Getting results for toxicity
        resultsToxicity = searcher.search(queryToxicity, limit=None)
        
        for result in resultsToxicity:
            if result.get('atc'):
                T.append((result["id"], result["atc"].split(";")))
            else:
                T.append((result["id"], None))

    return I, T

def get_atc_from_drug_id(drug_id):
    """Reads xml files. Search through the index for symptom in indication and toxicity

    Args:
        drug_id : id of the drug

    Returns:
        list: 
    """
    xml = ElementTree.parse("bd/drugbank.xml")
    root = xml.getroot()
    for element in root.findall('{http://www.drugbank.ca}drug'):
        idDrug = element[0].text
        if idDrug == drug_id:
            res = []
            for e in element.findall('{http://www.drugbank.ca}atc-codes'):
                for e2 in e.findall('{http://www.drugbank.ca}atc-code'):
                    res.append(e2.attrib["code"])
                    for e3 in e2.findall('{http://www.drugbank.ca}level'):
                        res.append(e3.attrib["code"])
                    return res
    return None

#res = get_atc_from_drug_id("DB00053")
#print(res)

#print(search_index_xml("Pulmonary"))

from whoosh import index
from whoosh.fields import *
from whoosh.qparser import QueryParser
import os, os.path

def get_all_drug_id_stitch_ATC():
    """Gets all the drug id in the chemical.sources.v5.0_short.tsv database

    Returns:
        list: list of all the drug id in the chemical.sources.v5.0_short.tsv database
    """
    list = []

    with open("bd/chemical.sources.v5.0_short.tsv") as file:
        l = file.readline()
        
        while l:
            
            l = l.split()
            if 3 <= len(l):
                if l[2] == "ATC":
                    list.append(l[3])
            l = file.readline()

    return list


def get_label_by_drug_id_stitchATC(drug_id):
    """Gets the label of a drug by its id

    Args:
        drug_id (str): drug id

    Returns:
        label: label of the drug
    """
    label = ""

    with open("bd/br08303.keg") as file:
        l = file.readline()
        while l:
            l = l.split()
            if len(l[0]) == 'E' or l[0] == 'F':
                if(l[1] == drug_id):
                    i=2
                    while i < len(l):
                        label = label + l[i] + " "
                        i = i + 1
                    return label
            l = file.readline()

    return label

#print(get_label_by_drug_id_stitchATC("D00943"))


def get_ATC_id(CID_l):
    """
    :param CID_l: List of Stitch ids got from Sider
    :return: List of ATC ids
    """
    ATC_id_l = []

    with open("bd/chemical.sources.v5.0_short.tsv") as f:
        line = f.readline()
        while line:
            line = line.split()
            if line[0] in CID_l:
                if line[2] == "ATC":
                    break
                ATC_id_l.append(line[3])
            line = f.readline()

    return ATC_id_l

#print(get_ATC_id(["CID100000085"]))


def convert_id_stitch_atc_to_if_stitch_sider(id_stitch_atc_list):
    res = []
    for i in id_stitch_atc_list:
        temp = i[0:3] + i[4:]
        res.append(temp)
    return res


def create_index(file_path):
    """Read xml files. Creates an index (stitch and atc) and only stores id.

    Args:
        file_path : path of xml file to read
    """
    
    # The directory that contains the index
    indexdir = "bd/stitchAtcIndex"
    
    # The schema of the index
    schema = Schema(stitch=ID(stored=True), atc=TEXT(stored=True))
    
    # if the directory does not exist, we create it
    if not os.path.exists(indexdir):
        os.mkdir(indexdir)
    
    # Creating the index in the directory "bd/indexdir"
    ix = index.create_in(indexdir, schema)
    
    # Opening the index
    ix = index.open_dir(indexdir)
    
    # Creating a writer to add documents
    writer = ix.writer()

    # Indexing the file
    with open(file_path) as f:
        line = f.readline()
        while line:
            line = line.split()
            try :
                if line[2] == "ATC":
                    writer.add_document(stitch=line[0][0:3]+line[0][4:], atc=line[3])
            except:
                pass
            line = f.readline()
    writer.commit()

#create_index("bd/chemical.sources.v5.0_short.tsv")

def search_index_tsv(stitch_id):
    """Reads tsv files. Search through the index for symptom in indication and toxicity

    Args:
        symptom : symptom input

    Returns:
        list: 
    """
    
    # The directory that contains the index
    indexdir = "bd/stitchAtcIndex"
    
    # Opening the index
    ix = index.open_dir(indexdir)
    
    # Creating a QueryParser object for the "stitch" field
    parser = QueryParser("stitch", ix.schema)
    
    # Parsing the query for the given stitch_id
    query = parser.parse(stitch_id)
    
    # Searching the index for the query
    with ix.searcher() as searcher:
        results = searcher.search(query)

        res = []
        
        # If the search returned at least one result, return the atc value of the first result
        if len(results) > 0:
            for i in results:
                res.append(i['atc'])
        return res

#print(search_index_tsv("CID00028871"))
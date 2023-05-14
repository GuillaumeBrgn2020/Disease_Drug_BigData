from whoosh import index
from whoosh.fields import *
from whoosh.qparser import QueryParser
import os, os.path


def get_file_text():
    """ get file text

    Returns:
        str : file text
    """
    
    file = open("bd/omim.txt")
    
    alltxt = file.read()
    file.close()
    return alltxt




def split_by_record(default=""):
    """ split by record

    Args:
       default: default value (Default value = "")

    Returns:
        str : list of records
    """
    
    if default == "":
        return list(get_file_text().split("*RECORD*"))
    
    else:
        return list(default.split("*RECORD*"))


def split_fields(record):
    """ split by field

    Args:
         record: record to split

    Returns:
        str : list of fields
    """
    return list(record.split("*FIELD*"))



def get_diseases_names(idOmim, synonym):
    """Reads omim.txt. Returns the names of diseases matching with idOmim and synonym

    Args:
        idOmim : idOmim of the disease
        symptoms : input synonym

    Returns:
        diseases_names : 
    """
    
    records = split_by_record()
    diseases_names = []
    
    name = ""
    id=0
    ### pour toute maladie dans le txt :
    for i in range(len(records)):
        record = split_fields(records[i])
        n = len(record) - 1
        j = 0
        while j <= n:
        ###     si idOmim = *FIELD* NO :
            if record[j][:3] == " NO":
                if int(record[j][4:][:-1]) == idOmim:
                    id = int(record[j][4:][:-1])
            if record[j][:3] == " TI":
                name = record[j][4:][:-1]
            if record[j][:3] == " CS":
                if synonym in record[j][4:][:-1] and id==idOmim:
                    diseases_names.append(name)
            j += 1
        ###         si *FIELD* CS contient syn :
        
        ###             ajouter le nom de la maladie (*FIELD* TI ?) dans diseases_names
        
    return diseases_names

# if __name__ == '__main__':
#     disease = get_diseases_names(100050,"Mild to moderate short stature")
#     #print(disease)


def create_index_txt(file_path):
    """Read txt files. Creates an index ().

    Args:
        file_path : path of txt file to read
    """
    
    # The directory that contains the index
    indexdir = "bd/omimTxtIndex"
    
    # The schema of the index
    schema = Schema(name=TEXT(stored=True), idOmim = TEXT(), FieldCS = TEXT(stored=True))
    
    # if the directory does not exist, we create it
    if not os.path.exists(indexdir):
        os.mkdir(indexdir)
    
    # Creating the index in the directory "bd/indexdir"
    ix = index.create_in(indexdir, schema)
    
    # Opening the index
    ix = index.open_dir(indexdir)
    
    # Creating a writer to add documents
    writer = ix.writer()
    
    records = split_by_record()
    for i in range(len(records)):
        record = split_fields(records[i])
        n = len(record) - 1
        j = 0
        idOmim = ""
        name = ""
        FieldCS = ""
        while j <= n:
            if record[j][:3] == " NO":
                idOmim = record[j][4:][:-1]
            if record[j][:3] == " TI":
                name = record[j][4:][:-1]
            if record[j][:3] == " CS":
                FieldCS = record[j][4:][:-1]
            j += 1
            
        # Adding a document
        writer.add_document(name=name, idOmim=idOmim, FieldCS=FieldCS)

    # Closing and the writer
    writer.commit()

#create_index_txt("bd/omim.txt")

def search_index_txt(idOmim, syn):
    """Reads txt files. Search through idOmim, disease matching with the syn

    Args:
        idOmim
        syn

    Returns:
        list: 
    """
    
    # The directory that contains the index
    indexdir = "bd/omimTxtIndex"
        
    # Opening the index
    ix = index.open_dir(indexdir)
    
    # Creating parser for query
    parser = QueryParser("idOmim", schema=ix.schema)
    
    # Creating query
    query = parser.parse(idOmim)
    
    names = []
    
    # Searching content corresponding to the query
    with ix.searcher() as searcher:
        
        # Getting results for indication
        results = searcher.search(query, limit=None)
        
        for result in results:
            if syn in result["FieldCS"]:
                names.append(result["name"])
    return names

#print(search_index_txt("100050", "Broad nasal bridge"))
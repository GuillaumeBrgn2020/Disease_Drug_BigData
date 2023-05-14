
import sqlite3


def get_disease_id_hpo_annotation():
    """Gets all the disease id in the hpo_annotations.sqlite database

    Returns:
        disease_id_list: list of all the disease id in the hpo_annotations.sqlite database
    """
    con = sqlite3.connect("bd/hpo_annotations.sqlite")
    cursor = con.cursor()
    disease_id_list = cursor.execute("SELECT disease_id FROM phenotype_annotation").fetchall()
    cursor.close()
    
    for i in range(len(list)):
        disease_id_list[i] = disease_id_list[i][0]
    return disease_id_list
  
  
def get_sign_id_hpo_annotation():
    """Gets all the sign id in the hpo_annotations.sqlite database

    Returns:
        sign_id_list: list of all the sign id in the hpo_annotations.sqlite database
    """
    con = sqlite3.connect("bd/hpo_annotations.sqlite")
    cursor = con.cursor()
    sign_id_list = cursor.execute("SELECT sign_id FROM phenotype_annotation").fetchall()
    cursor.close()
    
    for i in range(len(list)):
        sign_id_list[i] = sign_id_list[i][0]
    return sign_id_list
  
  
def get_disease_id_by_sign_id(sign_id):
    """Gets tuples of disease label and disease id for a given symptom

    Args:
        sign_id (string): symptom id

    Returns:
        disease_id: list of disease id
        disease_label : list of disease label
    """
    con = sqlite3.connect("bd/hpo_annotations.sqlite")
    cursor = con.cursor()
    disease_id = []

    cursor.execute("SELECT disease_id, disease_label FROM phenotype_annotation WHERE sign_id = '"+sign_id+"' AND disease_db LIKE 'OMIM'")
    results = cursor.fetchall()
    
    for elt in results:
        disease_id.append(elt[0])

    cursor.close()

    return disease_id

#print(get_disease_id_by_sign_id("HP:0000463"))